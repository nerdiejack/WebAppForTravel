<template>
  <div class="hotel-view-container">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
      <div class="container-fluid">
        <span class="navbar-brand">Hotel Bookings</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item dropdown position-relative">
              <button class="nav-link" @click="toggleHotelList">
                Hotel Bookings <i class="fas fa-chevron-down" :class="{ 'rotate-180': !isHotelListCollapsed }"></i>
              </button>
              <div v-show="!isHotelListCollapsed" class="hotel-list">
                <div v-if="loading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading bookings...</span>
                  </div>
                </div>

                <div v-else-if="error" class="alert alert-danger" role="alert">
                  {{ error }}
                  <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
                    Retry
                  </button>
                </div>

                <div v-else-if="hotels.length === 0" class="text-center py-4 text-muted">
                  <i class="fas fa-hotel fa-3x mb-3"></i>
                  <p>No hotel bookings yet. Start planning your stay!</p>
                </div>

                <div v-else class="hotel-entries">
                  <div v-for="hotel in hotels" 
                       :key="hotel._id" 
                       class="hotel-card" 
                       @click="zoomToHotel(hotel)">
                    <div class="hotel-card-content">
                      <div class="hotel-card-left">
                        <div class="preview-image">
                          <i class="fas fa-hotel"></i>
                        </div>
                      </div>
                      <div class="hotel-card-middle">
                        <h5>{{ hotel.hotel_name }}</h5>
                        <div class="text-muted">
                          <small>
                            <i class="fas fa-map-marker-alt me-1"></i>{{ hotel.city }}
                            <span class="ms-2"><i class="fas fa-calendar me-1"></i>{{ formatDate(hotel.check_in) }}</span>
                          </small>
                        </div>
                      </div>
                      <div class="hotel-card-right">
                        <span class="price">{{ formatPrice(hotel.price_per_night) }}/night</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </li>
            <li class="nav-item dropdown">
              <button type="button" class="nav-link" @click="toggleDropdown">
                <i class="fas fa-cog"></i> Options <i class="fas fa-chevron-down ms-1" :class="{ 'rotate-180': isDropdownOpen }"></i>
              </button>
              <div class="dropdown-menu dropdown-menu-end" :class="{ 'show': isDropdownOpen }">
                <a class="dropdown-item" href="#" @click.prevent="openEditor">
                  <i class="fas fa-plus me-2"></i>New Booking
                </a>
                <a class="dropdown-item" href="#" @click.prevent="openEmailImport">
                  <i class="fas fa-envelope me-2"></i>Import from Email
                </a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
      <div class="map-wrapper">
        <div id="map-container" ref="mapContainer" class="map-container">
          <!-- Loading overlay -->
          <div v-if="loading" class="map-overlay">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading map...</span>
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

          <div id="map" ref="mapElement" class="map-element">
            <div class="map-controls">
              <button class="map-btn" @click="viewAllHotels">
                <i class="fas fa-globe-americas me-2"></i>View All Hotels
              </button>
            </div>
          </div>
        </div>
        <hotel-details
          v-if="selectedHotel"
          :hotel="selectedHotel"
          @back-to-map="closeSelectedHotel"
          @edit="editHotel"
          @hotel-deleted="loadHotels"
          class="hotel-details"
        />
      </div>

      <div class="hotel-list" :class="{ collapsed: isHotelListCollapsed }">
        <div 
          class="hotel-list-handle" 
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Hover to see hotel bookings"
        >
          <span class="handle-text">Hotel Bookings</span>
        </div>
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading bookings...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
          <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
            Retry
          </button>
        </div>

        <div v-else-if="hotels.length === 0" class="text-center py-4 text-muted">
          <i class="fas fa-hotel fa-3x mb-3"></i>
          <p>No hotel bookings yet. Start planning your stay!</p>
        </div>

        <div v-else class="hotel-entries">
          <div v-for="hotel in hotels" 
               :key="hotel._id" 
               class="hotel-card" 
               @click="zoomToHotel(hotel)">
            <div class="hotel-card-content">
              <div class="hotel-card-left">
                <div class="preview-image">
                  <i class="fas fa-hotel"></i>
                </div>
              </div>
              <div class="hotel-card-middle">
                <h5>{{ hotel.hotel_name }}</h5>
                <div class="text-muted">
                  <small>
                    <i class="fas fa-map-marker-alt me-1"></i>{{ hotel.city }}
                    <span class="ms-2"><i class="fas fa-calendar me-1"></i>{{ formatDate(hotel.check_in) }}</span>
                  </small>
                </div>
              </div>
              <div class="hotel-card-right">
                <span class="price">{{ formatPrice(hotel.price_per_night) }}/night</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Editor Modal -->
    <div class="modal fade" id="editorModal" tabindex="-1" ref="editorModal" aria-labelledby="editorModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered" style="max-width: 85%; width: 85%;">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editorModalLabel">{{ isEditing ? 'Edit Booking' : 'New Booking' }}</h5>
            <button type="button" class="btn-close" @click="closeEditor" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveHotelBooking">
              <!-- Hotel Information -->
              <div class="form-floating mb-3">
                <input 
                  id="hotelName"
                  v-model="newHotel.hotel_name" 
                  class="form-control form-control-lg" 
                  placeholder="Hotel Name"
                  required
                >
                <label for="hotelName">Hotel Name</label>
              </div>

              <div class="form-floating mb-3">
                <input 
                  id="city"
                  v-model="newHotel.city" 
                  class="form-control" 
                  placeholder="City"
                  required
                >
                <label for="city">City</label>
              </div>

              <div class="form-floating mb-3">
                <input 
                  id="address"
                  v-model="newHotel.address" 
                  class="form-control" 
                  placeholder="Address"
                  required
                >
                <label for="address">Address</label>
              </div>

              <!-- Dates -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="checkIn"
                      v-model="newHotel.check_in" 
                      type="date" 
                      class="form-control" 
                      required
                    >
                    <label for="checkIn">Check-in Date</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="checkOut"
                      v-model="newHotel.check_out" 
                      type="date" 
                      class="form-control" 
                      required
                    >
                    <label for="checkOut">Check-out Date</label>
                  </div>
                </div>
              </div>

              <!-- Room and Guest Information -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="roomType"
                      v-model="newHotel.room_type" 
                      class="form-control" 
                      placeholder="Room Type"
                      required
                    >
                    <label for="roomType">Room Type</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="guests"
                      v-model.number="newHotel.number_of_guests" 
                      type="number" 
                      class="form-control" 
                      required
                    >
                    <label for="guests">Number of Guests</label>
                  </div>
                </div>
              </div>

              <!-- Price Information -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="pricePerNight"
                      v-model.number="newHotel.price_per_night" 
                      type="number" 
                      step="any" 
                      class="form-control" 
                      required
                    >
                    <label for="pricePerNight">Price per Night</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      id="guestName"
                      v-model="newHotel.guest_name" 
                      class="form-control" 
                      placeholder="Guest Name"
                      required
                    >
                    <label for="guestName">Guest Name</label>
                  </div>
                </div>
              </div>

              <!-- Additional Information -->
              <div class="form-floating mb-3">
                <input 
                  id="bookingRef"
                  v-model="newHotel.booking_reference" 
                  class="form-control" 
                  placeholder="Booking Reference"
                >
                <label for="bookingRef">Booking Reference (Optional)</label>
              </div>

              <div class="form-floating mb-3">
                <textarea 
                  id="specialRequests"
                  v-model="newHotel.special_requests" 
                  class="form-control" 
                  placeholder="Special Requests"
                  style="height: 100px"
                ></textarea>
                <label for="specialRequests">Special Requests</label>
              </div>

              <!-- Location Selection -->
              <div class="mb-3">
                <label class="form-label">Location</label>
                <div class="input-group">
                  <input 
                    v-model.number="newHotel.latitude" 
                    type="number" 
                    step="any" 
                    class="form-control" 
                    placeholder="Latitude"
                    required
                  >
                  <input 
                    v-model.number="newHotel.longitude" 
                    type="number" 
                    step="any" 
                    class="form-control" 
                    placeholder="Longitude"
                    required
                  >
                  <button 
                    type="button" 
                    class="btn btn-secondary" 
                    @click="pickLocationOnMap"
                  >
                    Pick on Map
                  </button>
                </div>
              </div>

              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="closeEditor">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  {{ isEditing ? 'Update Booking' : 'Add Booking' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Email Import Modal -->
    <div class="modal fade" id="emailImportModal" tabindex="-1" ref="emailImportModal" aria-labelledby="emailImportModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="emailImportModalLabel">Import Booking from Email</h5>
            <button type="button" class="btn-close" @click="closeEmailImport" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Upload Email File</label>
              <input 
                type="file" 
                @change="handleEmailImport" 
                accept=".eml,.msg"
                class="form-control"
                ref="emailInput"
                :disabled="importLoading"
              >
              <small class="text-muted">Upload your Booking.com confirmation email (.eml or .msg file)</small>
            </div>
            <div v-if="importLoading" class="text-center py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Importing...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick, reactive } from 'vue'
import { Modal } from 'bootstrap'
import api from '../utils/axios'
import { loadGoogleMaps, cleanupGoogleMaps } from '../utils/mapLoader'
import { getWeatherData } from '../utils/weatherApi'
import HotelDetails from './HotelDetails.vue'

export default {
  name: 'HotelView',
  components: {
    HotelDetails
  },
  setup() {
    const mapContainer = ref(null)
    const mapElement = ref(null)
    const hotels = ref([])
    const map = ref(null)
    const markers = ref([])
    const selectedHotel = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const isHotelListCollapsed = ref(false)
    const isDropdownOpen = ref(false)
    const isEditing = ref(false)
    const importLoading = ref(false)
    const editorModal = ref(null)
    const emailImportModal = ref(null)
    const emailInput = ref(null)
    const geocoder = ref(null)
    const google = ref(null)
    let mapInitialized = false
    const activeInfoWindow = ref(null)

    const newHotel = reactive({
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
        if (mapInitialized) {
          console.log('Map already initialized')
          return
        }
        
        loading.value = true
        error.value = null
        
        await nextTick()
        
        const mapDiv = document.getElementById('map')
        if (!mapDiv) {
          console.error('Map container element not found')
          throw new Error('Map container not found')
        }

        console.log('Loading Google Maps...')
        google.value = await loadGoogleMaps()
        
        if (!google.value) {
          throw new Error('Failed to load Google Maps')
        }

        console.log('Creating map instance...')
        map.value = new google.value.maps.Map(mapDiv, {
          center: { lat: 13.7563, lng: 100.5018 }, // Bangkok
          zoom: 6,
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: true,
          zoomControl: true,
          gestureHandling: 'greedy',
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }]
            }
          ]
        })

        // Add map click handler
        map.value.addListener('click', () => {
          if (activeInfoWindow.value) {
            activeInfoWindow.value.close()
            activeInfoWindow.value = null
          }
        })

        geocoder.value = new google.value.maps.Geocoder()
        
        if (!geocoder.value) {
          throw new Error('Failed to initialize geocoder')
        }

        console.log('Map initialization complete')
        mapInitialized = true
        await loadHotels()
        
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
        loading.value = true
        error.value = null
        
        const response = await api.get('/api/hotels')
        hotels.value = response.data.map(hotel => ({
          ...hotel,
          check_in: new Date(hotel.check_in).toISOString().split('T')[0],
          check_out: new Date(hotel.check_out).toISOString().split('T')[0]
        }))
        
        await displayHotelsOnMap()
        
      } catch (err) {
        console.error('Error loading hotels:', err)
        error.value = 'Failed to load hotel bookings. Please try again later.'
      } finally {
        loading.value = false
      }
    }

    const displayHotelsOnMap = async () => {
      if (!map.value || !google.value) {
        console.error('Map or Google not initialized')
        return
      }
      
      // Clear existing markers
      markers.value.forEach(marker => marker.setMap(null))
      markers.value = []
      
      if (activeInfoWindow.value) {
        activeInfoWindow.value.close()
        activeInfoWindow.value = null
      }

      for (const hotel of hotels.value) {
        try {
          const position = {
            lat: parseFloat(hotel.latitude),
            lng: parseFloat(hotel.longitude)
          }

          if (isNaN(position.lat) || isNaN(position.lng)) {
            console.error('Invalid coordinates for hotel:', hotel)
            continue
          }

          const marker = new google.value.maps.Marker({
            position,
            map: map.value,
            title: hotel.hotel_name,
            icon: {
              url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
            }
          })

          markers.value.push(marker)

          let weatherData = null
          try {
            weatherData = await getWeatherData(position.lat, position.lng)
          } catch (weatherErr) {
            console.error('Error fetching weather data:', weatherErr)
          }
          
          marker.addListener('click', () => {
            if (activeInfoWindow.value) {
              activeInfoWindow.value.close()
            }

            const formatTimeFromUnix = (unixTimestamp, timezone) => {
              const date = new Date(unixTimestamp * 1000);
              return date.toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit', 
                hour12: false,
                timeZone: timezone
              });
            };

            const contentString = `
              <div class="info-window">
                <div class="info-window-header">
                  <h5><strong>${hotel.city}</strong><br><em>${hotel.hotel_name}</em></h5>
                  <button class="close-btn" onclick="this.closest('.gm-style-iw-c').querySelector('.gm-ui-hover-effect').click()">&times;</button>
                </div>
                <div class="info-window-content">
                  ${weatherData ? `
                    <div class="weather-info">
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M12 0C5.383 0 0 5.383 0 12s5.383 12 12 12 12-5.383 12-12S18.617 0 12 0zm0 22C6.486 22 2 17.514 2 12S6.486 2 12 2s10 4.486 10 10-4.486 10-10 10zm.5-17v6.5H17v1h-5.5V19h-1V6z"/></svg>
                        <span>${new Date().toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit',
                          hour12: false,
                          timeZone: weatherData.timezone
                        })}</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M12 3a9 9 0 1 0 9 9 9 9 0 0 0-9-9zm0 16a7 7 0 1 1 7-7 7 7 0 0 1-7 7zm3.5-6H13V7h-2v6H8.5l3.5 3.5z"/></svg>
                        <span>${Math.round(weatherData.current.temp)}°C</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/></svg>
                        <span>${weatherData.current.weather[0].description}</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm1-13h-2v6l5.25 3.15.75-1.23-4-2.37z"/></svg>
                        <span>${weatherData.current.pressure} hPa</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M12 2c-5.33 4.55-8 8.48-8 11.8 0 4.98 3.8 8.2 8 8.2s8-3.22 8-8.2c0-3.32-2.67-7.25-8-11.8zm0 18c-3.35 0-6-2.57-6-6.2 0-2.34 1.95-5.44 6-9.14 4.05 3.7 6 6.79 6 9.14 0 3.63-2.65 6.2-6 6.2z"/></svg>
                        <span>${weatherData.current.humidity}%</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M14.5 17.97c1.27-1.12 2-2.74 2-4.47 0-3.31-2.69-6-6-6S4.5 10.19 4.5 13.5c0 1.73.73 3.35 2 4.47v-1.23c-.86-.91-1.4-2.14-1.4-3.49 0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.35-.54 2.58-1.4 3.49v1.23z"/></svg>
                        <span>${Math.round(weatherData.current.wind_speed * 3.6)} km/h</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zm0 8c-1.65 0-3-1.35-3-3s1.35-3 3-3 3 1.35 3 3-1.35 3-3 3z"/></svg>
                        <span>${formatTimeFromUnix(weatherData.current.sunrise, weatherData.timezone)}</span>
                      </div>
                      <div class="weather-row">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="#e74c3c"><path d="M10 2c-1.82 0-3.53.5-5 1.35C2.38 4.71 0 7.62 0 11s2.38 6.29 5 7.65c1.47.85 3.18 1.35 5 1.35s3.53-.5 5-1.35C17.62 17.29 20 14.38 20 11s-2.38-6.29-5-7.65C13.53 2.5 11.82 2 10 2zm0 16c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
                        <span>${formatTimeFromUnix(weatherData.current.sunset, weatherData.timezone)}</span>
                      </div>
                    </div>
                  ` : '<p>Weather data unavailable</p>'}
                </div>
              </div>
            `

            const styles = `
              <style>
                .weather-info {
                  margin-top: 12px;
                  display: grid;
                  grid-template-columns: repeat(2, 1fr);
                  gap: 8px;
                }

                .weather-row {
                  display: flex;
                  align-items: center;
                  gap: 10px;
                  padding: 10px;
                  background: #f8f9fa;
                  border-radius: 8px;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                  transition: all 0.2s ease;
                }

                .weather-row:hover {
                  background: #fff;
                  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                  transform: translateY(-1px);
                }

                .weather-row i {
                  font-family: 'Font Awesome 6 Free';
                  font-weight: 900;
                  font-style: normal;
                  font-size: 16px;
                  width: 20px;
                  text-align: center;
                  color: #e74c3c;
                }

                .weather-row span {
                  font-size: 14px;
                  color: #333;
                  font-weight: 500;
                }
              </style>
            `

            const infoWindow = new google.value.maps.InfoWindow({
              content: styles + contentString,
              maxWidth: 320,
              pixelOffset: new google.value.maps.Size(0, -20)
            })

            infoWindow.addListener('closeclick', () => {
              activeInfoWindow.value = null
            })

            infoWindow.open({
              map: map.value,
              anchor: marker
            })

            activeInfoWindow.value = infoWindow

            // Pan to marker without changing zoom
            map.value.panTo(marker.getPosition())
          })
        } catch (err) {
          console.error('Error creating marker for hotel:', hotel, err)
        }
      }

      // After all markers are created, fit bounds
      if (markers.value.length > 0) {
        viewAllHotels()
      }
    }

    const viewAllHotels = () => {
      if (!map.value || !google.value || markers.value.length === 0) {
        console.log('Map not ready or no markers')
        return
      }

      console.log('Viewing all hotels')

      // Close any open info windows
      if (activeInfoWindow.value) {
        activeInfoWindow.value.close()
        activeInfoWindow.value = null
      }

      const bounds = new google.value.maps.LatLngBounds()
      markers.value.forEach(marker => {
        console.log('Adding marker to bounds:', marker.getPosition().toString())
        bounds.extend(marker.getPosition())
      })
      
      map.value.fitBounds(bounds, { padding: 50 })
      
      // Add a small delay to allow bounds to be set
      setTimeout(() => {
        const ne = bounds.getNorthEast()
        const sw = bounds.getSouthWest()
        const distance = google.value.maps.geometry.spherical.computeDistanceBetween(
          new google.value.maps.LatLng(ne.lat(), ne.lng()),
          new google.value.maps.LatLng(sw.lat(), sw.lng())
        )
        
        console.log('Distance between points:', distance)
        
        // Adjust zoom based on distance
        if (distance > 5000000) {
          map.value.setZoom(3)
        } else if (distance > 2000000) {
          map.value.setZoom(4)
        } else if (distance > 1000000) {
          map.value.setZoom(5)
        } else if (distance > 500000) {
          map.value.setZoom(6)
        } else if (distance > 200000) {
          map.value.setZoom(7)
        } else if (distance > 100000) {
          map.value.setZoom(8)
        } else if (distance > 50000) {
          map.value.setZoom(9)
        } else {
          map.value.setZoom(10)
        }
      }, 100)
    }

    const toggleHotelList = () => {
      isHotelListCollapsed.value = !isHotelListCollapsed.value
    }

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    const openEditor = () => {
      isEditing.value = false
      Object.assign(newHotel, {
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
      new Modal(editorModal.value).show()
    }

    const closeEditor = () => {
      new Modal(editorModal.value).hide()
    }

    const openEmailImport = () => {
      new Modal(emailImportModal.value).show()
    }

    const closeEmailImport = () => {
      new Modal(emailImportModal.value).hide()
    }

    const handleEmailImport = async (event) => {
      const file = event.target.files[0]
      if (!file) return

      try {
        importLoading.value = true
        const formData = new FormData()
        formData.append('email', file)

        await api.post('/api/hotels/import', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        await loadHotels()
        closeEmailImport()
        event.target.value = ''
      } catch (err) {
        console.error('Error importing email:', err)
        error.value = 'Failed to import booking from email. Please try again.'
      } finally {
        importLoading.value = false
      }
    }

    const saveHotelBooking = async () => {
      try {
        loading.value = true
        error.value = null

        const hotelData = {
          ...newHotel,
          total_price: calculateTotalPrice()
        }

        if (isEditing.value) {
          await api.put(`/api/hotels/${selectedHotel.value._id}`, hotelData)
        } else {
          await api.post('/api/hotels', hotelData)
        }

        await loadHotels()
        closeEditor()
      } catch (err) {
        console.error('Error saving hotel booking:', err)
        error.value = 'Failed to save hotel booking. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const editHotel = (hotel) => {
      isEditing.value = true
      Object.assign(newHotel, hotel)
      new Modal(editorModal.value).show()
    }

    const closeSelectedHotel = () => {
      selectedHotel.value = null
    }

    const pickLocationOnMap = () => {
      if (!map.value) return

      const picker = new google.value.maps.Marker({
        map: map.value,
        draggable: true
      })

      map.value.addListener('click', (event) => {
        picker.setPosition(event.latLng)
        newHotel.latitude = event.latLng.lat()
        newHotel.longitude = event.latLng.lng()

        geocoder.value.geocode({ location: event.latLng }, (results, status) => {
          if (status === 'OK' && results[0]) {
            const addressComponents = results[0].address_components
            const cityComponent = addressComponents.find(component => 
              component.types.includes('locality') || component.types.includes('administrative_area_level_1')
            )
            if (cityComponent) {
              newHotel.city = cityComponent.long_name
            }
            newHotel.address = results[0].formatted_address
          }
        })
      })

      picker.addListener('dragend', (event) => {
        newHotel.latitude = event.latLng.lat()
        newHotel.longitude = event.latLng.lng()

        geocoder.value.geocode({ location: event.latLng }, (results, status) => {
          if (status === 'OK' && results[0]) {
            const addressComponents = results[0].address_components
            const cityComponent = addressComponents.find(component => 
              component.types.includes('locality') || component.types.includes('administrative_area_level_1')
            )
            if (cityComponent) {
              newHotel.city = cityComponent.long_name
            }
            newHotel.address = results[0].formatted_address
          }
        })
      })
    }

    const calculateTotalPrice = () => {
      if (!newHotel.check_in || !newHotel.check_out || !newHotel.price_per_night) return null

      const checkIn = new Date(newHotel.check_in)
      const checkOut = new Date(newHotel.check_out)
      const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24))
      return nights * newHotel.price_per_night
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(price)
    }

    const retryLoading = () => {
      loadHotels()
    }

    const zoomToHotel = (hotel) => {
      if (!map.value) return
      
      const position = {
        lat: parseFloat(hotel.latitude),
        lng: parseFloat(hotel.longitude)
      }
      
      map.value.panTo(position)
      map.value.setZoom(15)
    }

    const resetMapView = () => {
      if (!map.value) return
      
      map.value.setZoom(6)
      map.value.panTo({ lat: 13.7563, lng: 100.5018 })
    }

    onMounted(async () => {
      try {
        console.log('Component mounted, initializing map...')
        await nextTick()
        await initMap()
      } catch (err) {
        console.error('Error in onMounted:', err)
        error.value = 'Failed to initialize the map. Please try refreshing the page.'
      }
    })

    onUnmounted(() => {
      console.log('Component unmounting, cleaning up...')
      if (map.value) {
        google.value?.maps?.event?.clearInstanceListeners(map.value)
        map.value = null
      }
      markers.value.forEach(marker => {
        google.value?.maps?.event?.clearInstanceListeners(marker)
        marker.setMap(null)
      })
      markers.value = []
      mapInitialized = false
      cleanupGoogleMaps()
    })

    return {
      mapContainer,
      mapElement,
      hotels,
      selectedHotel,
      loading,
      error,
      isHotelListCollapsed,
      isDropdownOpen,
      isEditing,
      importLoading,
      editorModal,
      emailImportModal,
      emailInput,
      newHotel,
      toggleHotelList,
      toggleDropdown,
      openEditor,
      closeEditor,
      openEmailImport,
      closeEmailImport,
      handleEmailImport,
      saveHotelBooking,
      editHotel,
      closeSelectedHotel,
      pickLocationOnMap,
      formatDate,
      formatPrice,
      retryLoading,
      viewAllHotels,
      zoomToHotel,
      resetMapView
    }
  }
}
</script>

<style>
/* Global styles for Google Maps Info Window */
.gm-style .gm-style-iw-c {
  padding: 0 !important;
  border-radius: 8px !important;
  max-width: 300px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.gm-style .gm-style-iw-d {
  overflow: hidden !important;
  padding: 0 !important;
}

.gm-style .gm-style-iw-t::after {
  display: none !important;
}

.gm-style .gm-ui-hover-effect {
  display: none !important;
}

.info-window {
  padding: 16px;
  background: white;
  border-radius: 8px;
}

.info-window-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.info-window-header h5 {
  margin: 0;
  font-size: 16px;
  line-height: 1.4;
}

.info-window-header h5 strong {
  display: block;
  color: #333;
  margin-bottom: 4px;
}

.info-window-header h5 em {
  font-style: italic;
  color: #666;
  font-weight: normal;
}

.info-window-content {
  font-size: 14px;
  color: #666;
}

.weather-info {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.weather-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.weather-row:hover {
  background: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.weather-row i {
  font-size: 16px;
  width: 20px;
  text-align: center;
  color: #e74c3c;
}

.weather-row span {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  line-height: 1;
  padding: 4px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #333;
}
</style>

<style scoped>
.hotel-view-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
  position: relative;
}

.map-wrapper {
  flex: 1;
  position: relative;
  height: calc(100vh - 56px);
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.map-element {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  bottom: 30px;
  right: 10px;
  z-index: 2;
  pointer-events: auto;
}

.map-btn {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.map-btn:hover {
  background-color: #f8f9fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Hotel list styles */
.hotel-list {
  width: 350px;
  background: white;
  border-left: 1px solid #e9ecef;
  overflow-y: auto;
  transition: transform 0.3s ease;
}

.hotel-list.collapsed {
  transform: translateX(350px);
}

.hotel-entries {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.hotel-list-handle {
  position: absolute;
  left: -30px;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  padding: 0.5rem;
  border-radius: 4px 0 0 4px;
  cursor: pointer;
  box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
  writing-mode: vertical-lr;
  text-orientation: mixed;
}

.handle-text {
  font-size: 0.875rem;
  color: var(--secondary-color);
}

.hotel-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #dee2e6;
  cursor: pointer;
  transition: all 0.2s ease;
}

.hotel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hotel-card-content {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.hotel-card-left {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
}

.preview-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  font-size: 1.5rem;
}

.hotel-card-middle {
  flex: 1;
  min-width: 0;
}

.hotel-card-middle h5 {
  margin: 0;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hotel-card-right {
  text-align: right;
}

.price {
  font-weight: 600;
  color: var(--primary-color);
}

.hotel-details {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 400px;
  background: white;
  box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

/* Modal Styles */
.modal-content {
  border-radius: 12px;
  border: none;
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.form-floating {
  margin-bottom: 1rem;
}

.form-floating > .form-control {
  height: calc(3.5rem + 2px);
  padding: 1rem 0.75rem;
}

.form-floating > label {
  padding: 1rem 0.75rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hotel-list {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    max-width: 350px;
    z-index: 1000;
  }

  .hotel-details {
    width: 100%;
    max-width: 400px;
  }
}
</style> 