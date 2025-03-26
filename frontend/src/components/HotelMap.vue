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

    <div class="map-container" ref="mapContainer"></div>

    <div class="hotel-list">
      <h3>Hotel Reservations</h3>
      <div v-for="hotel in hotels" :key="hotel._id" class="hotel-card">
        <h4>{{ hotel.hotel_name }}</h4>
        <p>{{ hotel.address }}, {{ hotel.city }}</p>
        <p>Check-in: {{ formatDate(hotel.check_in) }}</p>
        <p>Check-out: {{ formatDate(hotel.check_out) }}</p>
        <p>Guest: {{ hotel.guest_name }}</p>
        <p>Price per night: ${{ hotel.price_per_night }}</p>
        <p v-if="hotel.booking_reference">Ref: {{ hotel.booking_reference }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../utils/axios'
import { loadGoogleMaps } from '../utils/mapLoader'

export default {
  name: 'HotelMap',
  setup() {
    const mapContainer = ref(null)
    const hotels = ref([])
    const map = ref(null)
    const markers = ref([])
    const emailInput = ref(null)
    const isPickingLocation = ref(false)

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
        const google = await loadGoogleMaps()
        map.value = new google.maps.Map(mapContainer.value, {
          center: { lat: 0, lng: 0 },
          zoom: 2
        })
      } catch (error) {
        console.error('Error initializing map:', error)
      }
    }

    const loadHotels = async () => {
      try {
        const response = await api.get('/api/hotels')
        if (Array.isArray(response.data)) {
          hotels.value = response.data
          displayHotelsOnMap()
        } else {
          console.error('Unexpected response format:', response.data)
          hotels.value = []
        }
      } catch (error) {
        console.error('Error loading hotels:', error)
        hotels.value = []
      }
    }

    const displayHotelsOnMap = () => {
      if (!map.value || !window.google || !window.google.maps) {
        console.warn('Map not initialized yet')
        return
      }

      // Clear existing markers
      markers.value.forEach(marker => marker.setMap(null))
      markers.value = []

      if (!hotels.value || hotels.value.length === 0) {
        console.log('No hotels to display')
        return
      }

      hotels.value.forEach(hotel => {
        if (!hotel || typeof hotel.latitude !== 'number' || typeof hotel.longitude !== 'number') {
          console.warn('Invalid hotel data:', hotel)
          return
        }

        const marker = new window.google.maps.Marker({
          position: { lat: hotel.latitude, lng: hotel.longitude },
          map: map.value,
          title: hotel.hotel_name
        })

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div class="info-window">
              <h5>${hotel.hotel_name || 'Unnamed Hotel'}</h5>
              <p>${hotel.address || 'No address'}</p>
              <p>Check-in: ${formatDate(hotel.check_in)}</p>
              <p>Check-out: ${formatDate(hotel.check_out)}</p>
              <p>Guest: ${hotel.guest_name || 'No guest name'}</p>
              <p>Price: $${hotel.price_per_night || 0}/night</p>
            </div>
          `
        })

        marker.addListener('click', () => {
          infoWindow.open(map.value, marker)
        })

        markers.value.push(marker)
      })
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
      isPickingLocation.value = true
      alert('Click on the map to set the hotel location')

      const clickListener = map.value.addListener('click', (event) => {
        newHotel.value.latitude = event.latLng.lat()
        newHotel.value.longitude = event.latLng.lng()
        isPickingLocation.value = false
        google.maps.event.removeListener(clickListener)
        alert('Location set!')
      })
    }

    onMounted(async () => {
      await initMap()
      await loadHotels()
    })

    return {
      mapContainer,
      hotels,
      newHotel,
      emailInput,
      addHotelReservation,
      handleEmailImport,
      pickLocationOnMap,
      formatDate
    }
  }
}
</script>

<style scoped>
.hotel-map-container {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 20px;
  padding: 20px;
  height: calc(100vh - 100px);
}

.hotel-form {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow-y: auto;
}

.map-container {
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.hotel-list {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow-y: auto;
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
  background: white;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

.info-window {
  padding: 10px;
  max-width: 200px;
}

.info-window h5 {
  margin: 0 0 10px 0;
}

.info-window p {
  margin: 5px 0;
}

.import-options {
  background: white;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.coordinates-group {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 10px;
  align-items: center;
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
</style> 