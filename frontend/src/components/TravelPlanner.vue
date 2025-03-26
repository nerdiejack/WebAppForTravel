<template>
  <div class="travel-planner">
    <div class="container-fluid">
      <div class="row">
        <!-- Travel Search Form -->
        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">Plan Your Journey</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="searchRoute">
                <div class="mb-3">
                  <label class="form-label">From</label>
                  <div class="input-group">
                    <input type="text" class="form-control" v-model="fromLocation" placeholder="Enter city or location">
                    <button class="btn btn-outline-secondary" type="button" @click="useCurrentLocation">
                      <i class="fas fa-location-dot"></i>
                    </button>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">To</label>
                  <input type="text" class="form-control" v-model="toLocation" placeholder="Enter city or location">
                </div>
                <div class="mb-3">
                  <label class="form-label">Date</label>
                  <input type="date" class="form-control" v-model="travelDate">
                </div>
                <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-1"></span>
                  Search Routes
                </button>
              </form>
            </div>
          </div>

          <!-- Route Results -->
          <div v-if="routes.length > 0" class="card mt-3">
            <div class="card-header">
              <h5 class="card-title mb-0">Available Routes</h5>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div v-for="route in routes" :key="route.id" 
                     class="list-group-item list-group-item-action"
                     :class="{ 'active': selectedRoute?.id === route.id }"
                     @click="selectRoute(route)">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1">{{ route.name }}</h6>
                      <small class="text-muted">
                        {{ route.duration }} • {{ route.price }}
                      </small>
                    </div>
                    <div class="text-end">
                      <div class="badge bg-primary">{{ route.transportType }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Map and Route Details -->
        <div class="col-md-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Route Map</h5>
              <div class="btn-group">
                <button class="btn btn-outline-secondary btn-sm" @click="toggleMapType">
                  <i class="fas fa-layer-group"></i>
                </button>
              </div>
            </div>
            <div class="card-body p-0">
              <div id="route-map" class="route-map"></div>
            </div>
          </div>

          <!-- Route Details -->
          <div v-if="selectedRoute" class="card mt-3">
            <div class="card-header">
              <h5 class="card-title mb-0">Route Details</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6">
                  <h6>Journey Information</h6>
                  <ul class="list-unstyled">
                    <li><strong>Duration:</strong> {{ selectedRoute.duration }}</li>
                    <li><strong>Distance:</strong> {{ selectedRoute.distance }}</li>
                    <li><strong>Price:</strong> {{ selectedRoute.price }}</li>
                    <li><strong>Transport Type:</strong> {{ selectedRoute.transportType }}</li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <h6>Schedule</h6>
                  <ul class="list-unstyled">
                    <li><strong>Departure:</strong> {{ selectedRoute.departureTime }}</li>
                    <li><strong>Arrival:</strong> {{ selectedRoute.arrivalTime }}</li>
                    <li><strong>Stops:</strong> {{ selectedRoute.stops }}</li>
                  </ul>
                </div>
              </div>
              <div class="mt-3">
                <button class="btn btn-primary" @click="bookRoute">
                  <i class="fas fa-ticket-alt me-1"></i> Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Modal } from 'bootstrap'
import { searchRoutes, getRouteDetails } from '../utils/travelApi'

export default {
  name: 'TravelPlanner',
  setup() {
    const map = ref(null)
    const fromLocation = ref('')
    const toLocation = ref('')
    const travelDate = ref('')
    const routes = ref([])
    const selectedRoute = ref(null)
    const isLoading = ref(false)
    const routeMap = ref(null)
    const mapType = ref('roadmap')
    const directionsRenderer = ref(null)

    const initMap = async () => {
      try {
        const { Map } = await google.maps.importLibrary("maps")
        const { DirectionsService, DirectionsRenderer } = await google.maps.importLibrary("places")
        
        routeMap.value = new Map(document.getElementById('route-map'), {
          center: { lat: 13.7563, lng: 100.5018 }, // Bangkok
          zoom: 6,
          mapTypeId: mapType.value
        })

        // Initialize directions service and renderer
        const directionsService = new DirectionsService()
        directionsRenderer.value = new DirectionsRenderer({
          map: routeMap.value
        })

        // Store references
        map.value = {
          instance: routeMap.value,
          directionsService,
          directionsRenderer: directionsRenderer.value
        }
      } catch (error) {
        console.error('Error initializing map:', error)
      }
    }

    const searchRoute = async () => {
      if (!fromLocation.value || !toLocation.value) {
        alert('Please enter both origin and destination')
        return
      }

      isLoading.value = true
      try {
        routes.value = await searchRoutes(fromLocation.value, toLocation.value, travelDate.value)
        if (routes.value.length === 0) {
          alert('No routes found. Please try different locations.')
        }
      } catch (error) {
        console.error('Error searching routes:', error)
        alert('Error searching routes. Please try again.')
      } finally {
        isLoading.value = false
      }
    }

    const selectRoute = async (route) => {
      selectedRoute.value = route
      
      if (route.mode === 'flight') {
        // For flights, just show the route line
        const details = await getRouteDetails(route.id)
        if (details && details.legs && details.legs[0]) {
          const leg = details.legs[0]
          const path = leg.segments.map(segment => ({
            lat: segment.origin.latitude,
            lng: segment.origin.longitude
          }))
          
          // Clear previous route
          directionsRenderer.value.setMap(null)
          directionsRenderer.value = new google.maps.DirectionsRenderer({
            map: routeMap.value,
            polylineOptions: {
              strokeColor: '#FF0000',
              strokeWeight: 3
            }
          })
          
          // Draw flight path
          const flightPath = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeWeight: 3,
            map: routeMap.value
          })
          
          // Fit bounds to show entire route
          const bounds = new google.maps.LatLngBounds()
          path.forEach(point => bounds.extend(point))
          routeMap.value.fitBounds(bounds)
        }
      } else {
        // For driving and transit routes
        const request = {
          origin: fromLocation.value,
          destination: toLocation.value,
          travelMode: route.mode === 'driving' ? 
            google.maps.TravelMode.DRIVING : 
            google.maps.TravelMode.TRANSIT
        }

        try {
          const result = await map.value.directionsService.route(request)
          map.value.directionsRenderer.setDirections(result)
          
          // Fit bounds to show entire route
          const bounds = new google.maps.LatLngBounds()
          result.routes[0].bounds.extend(bounds)
          routeMap.value.fitBounds(bounds)
        } catch (error) {
          console.error('Error displaying route:', error)
        }
      }
    }

    const useCurrentLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            fromLocation.value = `${position.coords.latitude}, ${position.coords.longitude}`
          },
          (error) => {
            console.error('Error getting location:', error)
            alert('Unable to get your location. Please enter it manually.')
          }
        )
      } else {
        alert('Geolocation is not supported by your browser')
      }
    }

    const toggleMapType = () => {
      const types = ['roadmap', 'satellite', 'terrain']
      const currentIndex = types.indexOf(mapType.value)
      mapType.value = types[(currentIndex + 1) % types.length]
      if (map.value?.instance) {
        map.value.instance.setMapTypeId(mapType.value)
      }
    }

    const bookRoute = () => {
      // TODO: Implement booking functionality
      alert('Booking functionality coming soon!')
    }

    onMounted(() => {
      initMap()
    })

    onUnmounted(() => {
      // Cleanup map instance
      if (map.value?.instance) {
        map.value.instance = null
      }
    })

    return {
      fromLocation,
      toLocation,
      travelDate,
      routes,
      selectedRoute,
      isLoading,
      searchRoute,
      selectRoute,
      useCurrentLocation,
      toggleMapType,
      bookRoute
    }
  }
}
</script>

<style scoped>
.travel-planner {
  height: 100%;
  padding: 1rem;
}

.route-map {
  height: 500px;
  width: 100%;
}

.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.list-group-item {
  cursor: pointer;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.badge {
  font-size: 0.75rem;
  padding: 0.5em 0.75em;
}
</style> 