<template>
  <div class="hotel-map-container">
    <div class="hotel-form">
      <h3>Add Hotel Reservation</h3>
      
      <!-- Import Options -->
      <div class="import-options mb-3">
        <h4>Import Booking</h4>
        <input 
          type="file" 
          @change="handleEmailImport" 
          accept=".eml,.msg"
          class="file-input mb-2"
          ref="emailInput"
        >
        <small class="text-muted d-block mb-3">Upload your Booking.com confirmation email (.eml or .msg file)</small>
      </div>

      <div class="manual-entry">
        <h4>Manual Entry</h4>
        <form @submit.prevent="addHotelReservation" class="form-group">
          <input v-model="newHotel.hotel_name" placeholder="Hotel Name" required>
          <input v-model="newHotel.address" placeholder="Address" required>
          <input v-model="newHotel.city" placeholder="City" required>
          <div class="coordinates-group">
            <input v-model.number="newHotel.latitude" type="number" step="any" placeholder="Latitude" required>
            <input v-model.number="newHotel.longitude" type="number" step="any" placeholder="Longitude" required>
            <button type="button" @click="pickLocationOnMap" class="btn btn-secondary">Pick on Map</button>
          </div>
          <input v-model="newHotel.check_in" type="date" required>
          <input v-model="newHotel.check_out" type="date" required>
          <input v-model="newHotel.room_type" placeholder="Room Type" required>
          <input v-model.number="newHotel.price_per_night" type="number" step="any" placeholder="Price per Night" required>
          <input v-model.number="newHotel.number_of_guests" type="number" placeholder="Number of Guests" required>
          <input v-model="newHotel.guest_name" placeholder="Guest Name" required>
          <input v-model="newHotel.booking_reference" placeholder="Booking Reference (Optional)">
          <textarea v-model="newHotel.special_requests" placeholder="Special Requests"></textarea>
          <button type="submit" class="btn btn-primary">Add Reservation</button>
        </form>
      </div>
    </div>

    <div class="map-wrapper">
      <div class="map-container" ref="mapContainer">
        <!-- Loading overlay -->
        <div v-if="loading" class="map-overlay">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <!-- Error overlay -->
        <div v-if="error" class="map-overlay error">
          <div class="alert alert-danger" role="alert">
            {{ error }}
            <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
              Retry
            </button>
          </div>
        </div>
      </div>
      
      <!-- View All Hotels button -->
      <button @click="viewAllHotels" class="view-all-btn">
        <i class="fas fa-globe-americas me-2"></i>
        View All Hotels
      </button>
    </div>

    <div class="hotel-list">
      <h3>Hotel Reservations</h3>
      
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
        <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
          Retry
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="hotels.length === 0" class="text-center py-4 text-muted">
        No hotel reservations found
      </div>

      <!-- Hotel cards -->
      <div v-else class="accordion" id="hotelAccordion">
        <div v-for="(hotel, index) in hotels" 
             :key="hotel._id" 
             class="accordion-item hotel-card">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed"
                    type="button"
                    :data-bs-target="'#collapse' + index"
                    data-bs-toggle="collapse"
                    @click="handleAccordionClick(hotel)">
              <div>
                <strong>{{ hotel.hotel_name }}</strong>
                <div class="text-muted">{{ hotel.city }}</div>
              </div>
            </button>
          </h2>
          <div :id="'collapse' + index" 
               class="accordion-collapse collapse"
               data-bs-parent="#hotelAccordion">
            <div class="accordion-body">
              <p><i class="fas fa-map-marker-alt me-2"></i>{{ hotel.address }}</p>
              <p><i class="fas fa-calendar-check me-2"></i>Check-in: {{ formatDate(hotel.check_in) }}</p>
              <p><i class="fas fa-calendar-times me-2"></i>Check-out: {{ formatDate(hotel.check_out) }}</p>
              <p><i class="fas fa-user me-2"></i>Guest: {{ hotel.guest_name }}</p>
              <p><i class="fas fa-euro-sign me-2"></i>Price per night: {{ formatPrice(hotel.price_per_night) }}</p>
              <p v-if="hotel.booking_reference">
                <i class="fas fa-bookmark me-2"></i>Ref: {{ hotel.booking_reference }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick, reactive } from 'vue'
import api from '../utils/axios'
import { loadGoogleMaps, cleanupGoogleMaps } from '../utils/mapLoader'
import { getWeatherData } from '../utils/weatherApi'

export default {
  name: 'HotelMap',
  setup() {
    const mapContainer = ref(null)
    const hotels = ref([])
    const map = ref(null)
    const markers = ref([])
    const emailInput = ref(null)
    const isPickingLocation = ref(false)
    const selectedHotel = ref(null)
    const activeInfoWindow = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const geocoder = ref(null)
    const google = ref(null)
    let mapInitialized = false

    const newHotel = ref({
      hotel_name: '',
      address: '',
      city: '',
      latitude: null,
      longitude: null,
      check_in: '',
      check_out: '',
      room_type: '',
      price_per_night: null,
      total_price: null,
      guest_name: '',
      number_of_guests: null,
      booking_reference: '',
      special_requests: '',
      status: 'confirmed'
    })

    const initMap = async () => {
      try {
        if (mapInitialized) return
        loading.value = true
        error.value = null
        
        // Wait for the container to be available
        await nextTick()
        
        if (!mapContainer.value) {
          throw new Error('Map container not found')
        }

        // Load Google Maps API
        google.value = await loadGoogleMaps()
        
        // Create a div element for the map
        const mapElement = document.createElement('div')
        mapElement.style.width = '100%'
        mapElement.style.height = '100%'
        mapContainer.value.appendChild(mapElement)

        // Initialize map
        map.value = new google.value.maps.Map(mapElement, {
          center: { lat: 13.7563, lng: 100.5018 }, // Default to Bangkok
          zoom: 6,
          mapTypeControl: true,
          streetViewControl: true,
          fullscreenControl: true,
          zoomControl: true,
          gestureHandling: 'greedy'
        })

        // Initialize geocoder
        geocoder.value = new google.value.maps.Geocoder()
        
        if (!geocoder.value) {
          throw new Error('Failed to initialize geocoder')
        }

        mapInitialized = true
        console.log('Map and geocoder initialized successfully')
        
      } catch (err) {
        console.error('Error initializing map:', err)
        error.value = 'Failed to load Google Maps. Please try again later.'
        mapInitialized = false
      } finally {
        loading.value = false
      }
    }

    const loadHotels = async () => {
      try {
        loading.value = true;
        error.value = null;
        
        // Store current states before refresh
        const mapState = {
          center: map.value ? map.value.getCenter() : null,
          zoom: map.value ? map.value.getZoom() : null
        };

        // Store currently expanded accordion items
        const expandedAccordions = Array.from(document.querySelectorAll('.accordion-collapse.show'))
          .map(item => item.id);

        const response = await api.get('/api/hotels');
        
        if (Array.isArray(response.data)) {
          hotels.value = response.data.map(hotel => ({
            ...hotel,
            check_in: new Date(hotel.check_in).toISOString().split('T')[0],
            check_out: new Date(hotel.check_out).toISOString().split('T')[0]
          }));
          
          // Update markers without changing the view
          await displayHotelsOnMap(false);
          
          // Restore map state
          if (map.value && mapState.center && mapState.zoom) {
            map.value.setCenter(mapState.center);
            map.value.setZoom(mapState.zoom);
          }

          // Wait for the DOM to update with new hotels
          await nextTick();

          // Restore expanded state of accordion items
          expandedAccordions.forEach(id => {
            const accordionItem = document.getElementById(id);
            if (accordionItem) {
              const bsCollapse = new bootstrap.Collapse(accordionItem, {
                toggle: false
              });
              bsCollapse.show();
            }
          });
        } else {
          throw new Error('Unexpected response format');
        }
      } catch (error) {
        console.error('Error loading hotels:', error);
        error.value = 'Failed to load hotel reservations. Please try again later.';
        hotels.value = [];
      } finally {
        loading.value = false;
      }
    }

    const displayHotelsOnMap = async (fitBounds = true) => {
      if (!map.value || !google.value || !geocoder.value) {
        console.warn('Map or geocoder not initialized yet')
        return
      }

      try {
        // Clear existing markers
        markers.value.forEach(marker => marker.setMap(null))
        markers.value = []

        if (!hotels.value || hotels.value.length === 0) {
          return
        }

        const bounds = new google.value.maps.LatLngBounds()
        
        for (const hotel of hotels.value) {
          let position

          if (hotel.latitude && hotel.longitude) {
            position = { lat: parseFloat(hotel.latitude), lng: parseFloat(hotel.longitude) }
          } else if (hotel.address && hotel.city) {
            try {
              console.log('Geocoding address:', `${hotel.address}, ${hotel.city}`)
              const result = await geocodeAddress(`${hotel.address}, ${hotel.city}`)
              position = result.location
              // Update the hotel with the geocoded coordinates
              hotel.latitude = position.lat
              hotel.longitude = position.lng
            } catch (error) {
              console.warn(`Failed to geocode hotel address: ${hotel.hotel_name}`, error)
              continue
            }
          } else {
            console.warn('Hotel missing both coordinates and address:', hotel)
            continue
          }

          if (position && !isNaN(position.lat) && !isNaN(position.lng)) {
            bounds.extend(position)
            const marker = await createMarker(hotel, position)
            if (marker) {
              markers.value.push(marker)
            }
          }
        }

        // Only fit bounds if explicitly requested
        if (fitBounds && markers.value.length > 0) {
          map.value.fitBounds(bounds)
          if (markers.value.length === 1) {
            map.value.setZoom(15)
          }
        }
      } catch (error) {
        console.error('Error displaying hotels on map:', error)
        error.value = 'Failed to display hotels on map. Please try again later.'
      }
    }

    const geocodeAddress = async (address) => {
      return new Promise((resolve, reject) => {
        if (!geocoder.value) {
          console.error('Geocoder not initialized')
          reject(new Error('Geocoder not initialized'))
          return
        }

        geocoder.value.geocode({ address: address }, function(results, status) {
          if (status === google.value.maps.GeocoderStatus.OK && results[0]) {
            const location = {
              lat: results[0].geometry.location.lat(),
              lng: results[0].geometry.location.lng()
            }
            resolve({
              location,
              formattedAddress: results[0].formatted_address
            })
          } else {
            console.error('Geocoding failed:', status)
            reject(new Error(`Geocoding failed: ${status}`))
          }
        })
      })
    }

    const createMarker = async (hotel, position) => {
      if (!map.value || !google.value) return null;

      const marker = new google.value.maps.Marker({
        position,
        map: map.value,
        title: hotel.city,
        animation: google.value.maps.Animation.DROP
      });

      // Create info window with loading state
      const infoWindow = new google.value.maps.InfoWindow({
        content: `
          <div class="info-window">
            <h5>${hotel.city}</h5>
            <div class="hotel-name">${hotel.hotel_name}</div>
            <div class="weather-info">
              <p>Loading weather data...</p>
            </div>
          </div>
        `
      });

      // Add click listener to marker
      marker.addListener('click', async () => {
        if (activeInfoWindow.value) {
          activeInfoWindow.value.close();
        }
        
        infoWindow.open(map.value, marker);
        activeInfoWindow.value = infoWindow;
        selectedHotel.value = hotel;

        // Fetch weather data when marker is clicked
        try {
          const weatherData = await getWeatherData(position.lat, position.lng);
          if (weatherData) {
            const weatherIcon = `https://openweathermap.org/img/w/${weatherData.icon}.png`;
            
            // Calculate local time using timezone offset
            const utcTime = new Date();
            const localTime = new Date(utcTime.getTime() + (weatherData.timezone * 1000));
            const formattedLocalTime = localTime.toLocaleTimeString('de-DE', {
              hour: '2-digit',
              minute: '2-digit',
              timeZone: 'UTC'
            });

            infoWindow.setContent(`
              <div class="info-window">
                <h5>${hotel.city}</h5>
                <div class="hotel-name">${hotel.hotel_name}</div>
                <div class="weather-info">
                  <div class="weather-header">
                    <img src="${weatherIcon}" alt="Weather icon">
                    <div class="weather-main">
                      <span class="temperature">${weatherData.temperature}°C</span>
                      <span class="description">${weatherData.description}</span>
                    </div>
                  </div>
                  <div class="weather-details">
                    <p><i class="fas fa-clock"></i> Local Time: ${formattedLocalTime}</p>
                    <p><i class="fas fa-sun"></i> Sunrise: ${weatherData.sunrise}</p>
                    <p><i class="fas fa-moon"></i> Sunset: ${weatherData.sunset}</p>
                    <p><i class="fas fa-tint"></i> Humidity: ${weatherData.humidity}%</p>
                    <p><i class="fas fa-wind"></i> Wind: ${weatherData.windSpeed} km/h</p>
                  </div>
                </div>
              </div>
            `);
          }
        } catch (error) {
          console.error('Error updating weather info:', error);
          infoWindow.setContent(`
            <div class="info-window">
              <h5>${hotel.city}</h5>
              <div class="hotel-name">${hotel.hotel_name}</div>
              <p class="error-message">Weather data unavailable</p>
            </div>
          `);
        }
      });

      return marker;
    }

    const addHotelReservation = async () => {
      try {
        // Format the data for the backend
        const formattedHotel = {
          ...newHotel.value,
          // Add time to dates to make them proper ISO strings
          check_in: new Date(newHotel.value.check_in + 'T00:00:00').toISOString(),
          check_out: new Date(newHotel.value.check_out + 'T00:00:00').toISOString()
        }

        // Calculate total price
        const checkIn = new Date(formattedHotel.check_in)
        const checkOut = new Date(formattedHotel.check_out)
        const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24))
        formattedHotel.total_price = nights * formattedHotel.price_per_night

        console.log('Sending hotel data:', formattedHotel)
        const response = await api.post('/api/hotels', formattedHotel)
        console.log('Response:', response.data)
        
        if (response.data) {
          hotels.value.push(response.data)
          displayHotelsOnMap()
          alert('Hotel reservation added successfully!')

          // Reset form
          newHotel.value = {
            hotel_name: '',
            address: '',
            city: '',
            latitude: null,
            longitude: null,
            check_in: '',
            check_out: '',
            room_type: '',
            price_per_night: null,
            total_price: null,
            guest_name: '',
            number_of_guests: null,
            booking_reference: '',
            special_requests: '',
            status: 'confirmed'
          }
        }
      } catch (error) {
        console.error('Error adding hotel reservation:', error)
        alert('Failed to add hotel reservation. Please check the console for details.')
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const handleEmailImport = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      const formData = new FormData()
      formData.append('email_file', file)

      try {
        const response = await api.post('import-booking-email', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        if (response.data.message) {
          alert('Successfully imported booking from email')
          await loadHotels()
          // Reset file input
          if (emailInput.value) {
            emailInput.value.value = ''
          }
        }
      } catch (error) {
        console.error('Error importing email:', error)
        alert('Failed to import booking from email. Please check the file format.')
      }
    }

    const pickLocationOnMap = () => {
      if (!map.value || !google.value) {
        console.warn('Map not initialized yet')
        return
      }

      isPickingLocation.value = true
      alert('Click on the map to set the hotel location')

      const clickListener = map.value.addListener('click', (event) => {
        newHotel.value.latitude = event.latLng.lat()
        newHotel.value.longitude = event.latLng.lng()
        isPickingLocation.value = false
        google.value.maps.event.removeListener(clickListener)
        alert('Location set!')
      })
    }

    const formatPrice = (price) => {
      if (!price) return '0.00'
      return Number(price).toLocaleString('de-DE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    const zoomToHotel = async (hotel) => {
      if (!map.value || !hotel.latitude || !hotel.longitude) return;

      selectedHotel.value = hotel;
      const position = { 
        lat: parseFloat(hotel.latitude), 
        lng: parseFloat(hotel.longitude) 
      };
      
      // Close any open info window
      if (activeInfoWindow.value) {
        activeInfoWindow.value.close();
      }

      // Find and trigger the marker for this hotel
      const marker = markers.value.find(m => {
        const markerPos = m.getPosition();
        return Math.abs(markerPos.lat() - parseFloat(hotel.latitude)) < 0.000001 && 
               Math.abs(markerPos.lng() - parseFloat(hotel.longitude)) < 0.000001;
      });

      if (marker) {
        map.value.setZoom(17);
        map.value.panTo(position);
        
        // Create info window with loading state
        const infoWindow = new google.value.maps.InfoWindow({
          content: `
            <div class="info-window">
              <h5>${hotel.city}</h5>
              <div class="hotel-name">${hotel.hotel_name}</div>
              <div class="weather-info">
                <p>Loading weather data...</p>
              </div>
            </div>
          `
        });

        infoWindow.open(map.value, marker);
        activeInfoWindow.value = infoWindow;

        // Add bounce animation to the marker
        marker.setAnimation(google.value.maps.Animation.BOUNCE);
        setTimeout(() => {
          marker.setAnimation(null);
        }, 1500);

        // Fetch and update weather data
        try {
          const weatherData = await getWeatherData(position.lat, position.lng);
          if (weatherData) {
            const weatherIcon = `https://openweathermap.org/img/w/${weatherData.icon}.png`;
            
            // Calculate local time using timezone offset
            const utcTime = new Date();
            const localTime = new Date(utcTime.getTime() + (weatherData.timezone * 1000));
            const formattedLocalTime = localTime.toLocaleTimeString('de-DE', {
              hour: '2-digit',
              minute: '2-digit',
              timeZone: 'UTC'
            });

            infoWindow.setContent(`
              <div class="info-window">
                <h5>${hotel.city}</h5>
                <div class="hotel-name">${hotel.hotel_name}</div>
                <div class="weather-info">
                  <div class="weather-header">
                    <img src="${weatherIcon}" alt="Weather icon">
                    <div class="weather-main">
                      <span class="temperature">${weatherData.temperature}°C</span>
                      <span class="description">${weatherData.description}</span>
                    </div>
                  </div>
                  <div class="weather-details">
                    <p><i class="fas fa-clock"></i> Local Time: ${formattedLocalTime}</p>
                    <p><i class="fas fa-sun"></i> Sunrise: ${weatherData.sunrise}</p>
                    <p><i class="fas fa-moon"></i> Sunset: ${weatherData.sunset}</p>
                    <p><i class="fas fa-tint"></i> Humidity: ${weatherData.humidity}%</p>
                    <p><i class="fas fa-wind"></i> Wind: ${weatherData.windSpeed} km/h</p>
                  </div>
                </div>
              </div>
            `);
          }
        } catch (error) {
          console.error('Error updating weather info:', error);
          infoWindow.setContent(`
            <div class="info-window">
              <h5>${hotel.city}</h5>
              <div class="hotel-name">${hotel.hotel_name}</div>
              <p class="error-message">Weather data unavailable</p>
            </div>
          `);
        }
      }
    };

    const retryLoading = async () => {
      await loadHotels()
    }

    const cleanup = () => {
      if (markers.value) {
        markers.value.forEach(marker => {
          if (marker) marker.setMap(null)
        })
        markers.value = []
      }

      if (activeInfoWindow.value) {
        activeInfoWindow.value.close()
        activeInfoWindow.value = null
      }

      if (map.value) {
        google.value?.maps.event.clearInstanceListeners(map.value)
        map.value = null
      }

      if (geocoder.value) {
        geocoder.value = null
      }

      if (google.value) {
        google.value = null
      }

      if (mapContainer.value) {
        mapContainer.value.innerHTML = ''
      }

      mapInitialized = false
      cleanupGoogleMaps()
    }

    onMounted(async () => {
      try {
        await initMap()
        await loadHotels()
      } catch (err) {
        console.error('Error during component mount:', err)
        error.value = 'Failed to initialize the application. Please refresh the page.'
      }
    })

    onUnmounted(() => {
      cleanup()
    })

    // Add a refresh interval for hotels
    let refreshInterval = null

    onMounted(() => {
      // Refresh hotels every 30 seconds
      refreshInterval = setInterval(async () => {
        await loadHotels()
      }, 30000)
    })

    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
      }
      cleanup()
    })

    const expandedHotelId = ref(null)

    const handleAccordionClick = (hotel) => {
      // Zoom to hotel location when expanding
      nextTick(() => {
        zoomToHotel(hotel)
      })
    }

    const viewAllHotels = () => {
      if (!map.value || !google.value || markers.value.length === 0) return;

      // Close all accordion items
      const accordionItems = document.querySelectorAll('.accordion-collapse.show');
      accordionItems.forEach(item => {
        const bsCollapse = new bootstrap.Collapse(item);
        bsCollapse.hide();
      });

      selectedHotel.value = null;
      if (activeInfoWindow.value) {
        activeInfoWindow.value.close();
      }

      // Create bounds that include all markers
      const bounds = new google.value.maps.LatLngBounds();
      markers.value.forEach(marker => {
        bounds.extend(marker.getPosition());
      });

      // Fit the map to show all markers
      map.value.fitBounds(bounds);

      // If there's only one marker, zoom out a bit
      if (markers.value.length === 1) {
        map.value.setZoom(15);
      }
    }

    return {
      mapContainer,
      hotels,
      newHotel,
      emailInput,
      addHotelReservation,
      handleEmailImport,
      pickLocationOnMap,
      formatDate,
      selectedHotel,
      zoomToHotel,
      formatPrice,
      loading,
      error,
      retryLoading,
      expandedHotelId,
      handleAccordionClick,
      viewAllHotels
    }
  }
}
</script>

<style scoped>
.hotel-map-container {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 1rem;
  height: 100%;
  padding: 1rem;
  background: #f8f9fa;
}

.hotel-form {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow-y: auto;
  max-height: 100%;
}

.map-wrapper {
  position: relative;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #fff;
}

.hotel-list {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow-y: auto;
  max-height: 100%;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

input, textarea {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.hotel-card {
  margin-bottom: 0.5rem;
}

.hotel-card:last-child {
  margin-bottom: 0;
}

.accordion-item {
  border: 1px solid #dee2e6;
  margin-bottom: 0.5rem;
}

.accordion-button {
  padding: 1rem;
  background-color: white;
}

.accordion-button:not(.collapsed) {
  background-color: #f8f9fa;
  color: #0d6efd;
  box-shadow: none;
}

.accordion-button::after {
  margin-left: auto;
}

.accordion-body {
  background-color: #f8f9fa;
  padding: 1rem;
}

.accordion-body p {
  margin-bottom: 0.5rem;
}

.accordion-body p:last-child {
  margin-bottom: 0;
}

.info-window {
  padding: 12px;
  max-width: 300px;
}

.info-window h5 {
  margin: 0 0 12px 0;
  color: #007bff;
  font-size: 16px;
}

.weather-info {
  margin-top: 8px;
}

.weather-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.weather-header img {
  width: 50px;
  height: 50px;
}

.weather-main {
  display: flex;
  flex-direction: column;
}

.temperature {
  font-size: 24px;
  font-weight: bold;
}

.description {
  color: #6c757d;
  text-transform: capitalize;
}

.weather-details {
  border-top: 1px solid #eee;
  padding-top: 8px;
}

.weather-details p {
  margin: 4px 0;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.weather-details i {
  width: 16px;
  color: #6c757d;
}

.error-message {
  color: #dc3545;
  font-size: 14px;
  margin: 0;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 15px;
  width: 100%;
}

.btn-secondary:hover {
  background: #5a6268;
}

.mb-3 {
  margin-bottom: 1rem;
}

.import-options {
  background: white;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.coordinates-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.coordinates-group input {
  width: 100%;
}

.coordinates-group button {
  width: 100%;
  margin-top: 10px;
}

.file-input {
  width: 100%;
  padding: 8px;
  border: 1px dashed #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.text-muted {
  color: #6c757d;
  font-size: 0.875em;
}

.d-block {
  display: block;
}

h4 {
  margin-bottom: 15px;
  color: #343a40;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  z-index: 1000;
}

.map-overlay.error {
  background: rgba(255, 255, 255, 0.95);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.alert {
  margin: 1rem;
  text-align: center;
}

.ms-2 {
  margin-left: 0.5rem;
}

.text-center {
  text-align: center;
}

.py-4 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.text-muted {
  color: #6c757d;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
  background: none;
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.2rem;
  cursor: pointer;
}

.btn-outline-danger:hover {
  color: #fff;
  background-color: #dc3545;
}

.view-all-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-all-btn:hover {
  background: #0056b3;
}

.hotel-name {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 12px;
  font-style: italic;
}
</style> 