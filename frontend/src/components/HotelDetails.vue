<template>
  <div class="hotel-details-container">
    <!-- Header -->
    <div class="details-header">
      <button class="btn btn-link back-btn" @click="$emit('back-to-map')">
        <i class="fas fa-arrow-left"></i> Back to Map
      </button>
      <div class="header-actions">
        <button class="btn btn-link" @click="$emit('edit', hotel)">
          <i class="fas fa-edit"></i> Edit
        </button>
        <button class="btn btn-link text-danger" @click="confirmDelete">
          <i class="fas fa-trash"></i> Delete
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="details-content">
      <h2>{{ hotel.hotel_name }}</h2>
      
      <div class="location-info">
        <i class="fas fa-map-marker-alt"></i>
        <span>{{ hotel.city }}</span>
        <span class="address">{{ hotel.address }}</span>
      </div>

      <div class="booking-info">
        <div class="info-group">
          <h6>Check-in</h6>
          <p>{{ formatDate(hotel.check_in) }}</p>
        </div>
        <div class="info-group">
          <h6>Check-out</h6>
          <p>{{ formatDate(hotel.check_out) }}</p>
        </div>
        <div class="info-group">
          <h6>Duration</h6>
          <p>{{ calculateDuration }}</p>
        </div>
      </div>

      <div class="room-info">
        <h6>Room Details</h6>
        <p><i class="fas fa-bed"></i> {{ hotel.room_type }}</p>
        <p><i class="fas fa-user"></i> {{ hotel.number_of_guests }} Guests</p>
        <p><i class="fas fa-user-tag"></i> {{ hotel.guest_name }}</p>
      </div>

      <div class="price-info">
        <h6>Price Details</h6>
        <p><i class="fas fa-euro-sign"></i> {{ formatPrice(hotel.price_per_night) }} per night</p>
        <p><i class="fas fa-receipt"></i> Total: {{ formatPrice(hotel.total_price) }}</p>
      </div>

      <div v-if="hotel.booking_reference" class="booking-reference">
        <h6>Booking Reference</h6>
        <p><i class="fas fa-bookmark"></i> {{ hotel.booking_reference }}</p>
      </div>

      <div v-if="hotel.special_requests" class="special-requests">
        <h6>Special Requests</h6>
        <p>{{ hotel.special_requests }}</p>
      </div>

      <div class="weather-info" v-if="weather && weather.daily">
        <h6>Weather Forecast</h6>
        <div class="weather-grid">
          <div v-for="(day, index) in weather.daily?.slice(0, 3)" :key="index" class="weather-day">
            <div class="weather-date">{{ formatWeatherDate(day.dt) }}</div>
            <div class="weather-icon">
              <i :class="getWeatherIcon(day.weather[0].icon)"></i>
            </div>
            <div class="weather-temp">
              {{ Math.round(day.temp.day) }}°C
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { getWeatherData } from '../utils/weatherApi'

export default {
  name: 'HotelDetails',
  props: {
    hotel: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const weather = ref(null)

    const calculateDuration = computed(() => {
      const checkIn = new Date(props.hotel.check_in)
      const checkOut = new Date(props.hotel.check_out)
      const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24))
      return `${nights} night${nights !== 1 ? 's' : ''}`
    })

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(price)
    }

    const formatWeatherDate = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
      })
    }

    const getWeatherIcon = (iconCode) => {
      const iconMap = {
        '01d': 'fas fa-sun',
        '01n': 'fas fa-moon',
        '02d': 'fas fa-cloud-sun',
        '02n': 'fas fa-cloud-moon',
        '03d': 'fas fa-cloud',
        '03n': 'fas fa-cloud',
        '04d': 'fas fa-cloud',
        '04n': 'fas fa-cloud',
        '09d': 'fas fa-cloud-rain',
        '09n': 'fas fa-cloud-rain',
        '10d': 'fas fa-cloud-sun-rain',
        '10n': 'fas fa-cloud-moon-rain',
        '11d': 'fas fa-bolt',
        '11n': 'fas fa-bolt',
        '13d': 'fas fa-snowflake',
        '13n': 'fas fa-snowflake',
        '50d': 'fas fa-smog',
        '50n': 'fas fa-smog'
      }
      return iconMap[iconCode] || 'fas fa-question'
    }

    const confirmDelete = () => {
      if (confirm('Are you sure you want to delete this hotel booking?')) {
        emit('hotel-deleted')
      }
    }

    const loadWeather = async () => {
      try {
        const data = await getWeatherData(props.hotel.latitude, props.hotel.longitude)
        weather.value = data
      } catch (error) {
        console.error('Error loading weather:', error)
      }
    }

    onMounted(() => {
      loadWeather()
    })

    return {
      weather,
      calculateDuration,
      formatDate,
      formatPrice,
      formatWeatherDate,
      getWeatherIcon,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.hotel-details-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  overflow-y: auto;
}

.details-header {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  position: sticky;
  top: 0;
  z-index: 1;
}

.back-btn {
  color: var(--secondary-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.header-actions .btn-link {
  color: var(--secondary-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.details-content {
  padding: 1.5rem;
  flex: 1;
}

.details-content h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--secondary-color);
  margin-bottom: 1.5rem;
}

.location-info .address {
  color: var(--secondary-color);
  font-size: 0.875rem;
}

.booking-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-group h6 {
  margin: 0;
  font-size: 0.875rem;
  color: var(--secondary-color);
}

.info-group p {
  margin: 0;
  font-weight: 500;
}

.room-info,
.price-info,
.booking-reference,
.special-requests,
.weather-info {
  margin-bottom: 1.5rem;
}

.room-info h6,
.price-info h6,
.booking-reference h6,
.special-requests h6,
.weather-info h6 {
  margin-bottom: 0.75rem;
  color: var(--secondary-color);
}

.room-info p,
.price-info p,
.booking-reference p,
.special-requests p {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.weather-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.weather-day {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.weather-date {
  font-size: 0.875rem;
  color: var(--secondary-color);
  margin-bottom: 0.5rem;
}

.weather-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.weather-temp {
  font-weight: 500;
}

@media (max-width: 768px) {
  .details-content {
    padding: 1rem;
  }

  .booking-info {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .weather-grid {
    grid-template-columns: 1fr;
  }
}
</style> 