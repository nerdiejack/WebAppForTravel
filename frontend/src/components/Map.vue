<template>
  <div class="map-page">
    <div class="map-container">
      <!-- Loading state -->
      <div v-if="loading" class="map-overlay">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="map-overlay error">
        <div class="alert alert-danger" role="alert">
          {{ error }}
        </div>
      </div>

      <div id="map"></div>
      <!-- Custom layer control -->
      <div v-if="!loading && !error" class="layer-control">
        <div class="layer-button" @click="setMapType('roadmap')" :class="{ active: currentMapType === 'roadmap' }">
          Road
        </div>
        <div class="layer-button" @click="setMapType('satellite')" :class="{ active: currentMapType === 'satellite' }">
          Satellite
        </div>
        <div class="layer-button" @click="setMapType('terrain')" :class="{ active: currentMapType === 'terrain' }">
          Terrain
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { loadGoogleMaps } from '../utils/mapLoader';

export default {
  name: 'MapComponent',
  props: {
    zoomToLocation: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      map: null,
      currentMapType: 'roadmap',
      loading: true,
      error: null,
      markers: [],
      geocoder: null,
      google: null,
      mapElement: null
    }
  },
  watch: {
    zoomToLocation: {
      handler(newLocation) {
        if (newLocation && this.map) {
          this.zoomToLocationData(newLocation)
        }
      },
      immediate: true
    }
  },
  methods: {
    setMapType(type) {
      if (this.map) {
        this.map.setMapTypeId(type)
        this.currentMapType = type
      }
    },
    async initMap() {
      try {
        this.loading = true
        this.error = null
        
        // Get map DOM element
        this.mapElement = document.getElementById('map')
        if (!this.mapElement) {
          throw new Error('Map element not found')
        }

        // Load Google Maps API
        this.google = await loadGoogleMaps()
        
        // Create the map instance
        this.map = new this.google.maps.Map(this.mapElement, {
          center: { lat: 13.7563, lng: 100.5018 }, // Bangkok coordinates
          zoom: 6,
          mapTypeControl: false,
          streetViewControl: true,
          streetViewControlOptions: {
            position: this.google.maps.ControlPosition.RIGHT_BOTTOM
          },
          fullscreenControl: true,
          fullscreenControlOptions: {
            position: this.google.maps.ControlPosition.RIGHT_TOP
          },
          zoomControl: true,
          zoomControlOptions: {
            position: this.google.maps.ControlPosition.RIGHT_CENTER
          },
          scaleControl: true,
          rotateControl: true,
          language: 'en',
          gestureHandling: 'greedy'
        })

        // Initialize geocoder if needed
        if (this.zoomToLocation) {
          this.geocoder = new this.google.maps.Geocoder()
        }

        this.loading = false
      } catch (error) {
        console.error('Error loading Google Maps:', error)
        this.error = 'Failed to load Google Maps. Please try again later.'
        this.loading = false
      }
    },
    async zoomToLocationData(location) {
      if (!this.map || !this.google) return

      try {
        if (location.lat && location.lng) {
          const position = { 
            lat: parseFloat(location.lat), 
            lng: parseFloat(location.lng) 
          }
          
          if (isNaN(position.lat) || isNaN(position.lng)) {
            throw new Error('Invalid coordinates')
          }

          this.map.setZoom(location.zoom || 15)
          this.map.panTo(position)
          
          this.clearMarkers()
          const marker = new this.google.maps.Marker({
            position,
            map: this.map,
            title: location.name || '',
            animation: this.google.maps.Animation.DROP
          })
          this.markers.push(marker)
        } else if (location.address) {
          if (!this.geocoder) {
            this.geocoder = new this.google.maps.Geocoder()
          }

          this.geocoder.geocode({ address: location.address }, (results, status) => {
            if (status === 'OK' && results[0]) {
              const position = results[0].geometry.location
              this.map.setZoom(location.zoom || 13)
              this.map.panTo(position)

              this.clearMarkers()
              const marker = new this.google.maps.Marker({
                position,
                map: this.map,
                title: location.name || location.address,
                animation: this.google.maps.Animation.DROP
              })
              this.markers.push(marker)
            } else {
              console.error('Geocoding failed:', status)
              this.error = `Failed to find location: ${location.address}`
            }
          })
        }
      } catch (error) {
        console.error('Error zooming to location:', error)
        this.error = `Failed to zoom to location: ${error.message}`
      }
    },
    clearMarkers() {
      if (this.markers.length > 0) {
        this.markers.forEach(marker => {
          if (marker) marker.setMap(null)
        })
        this.markers = []
      }
    },
    cleanup() {
      this.clearMarkers()
      if (this.map) {
        // Remove event listeners if any
        this.google?.maps.event.clearInstanceListeners(this.map)
        this.map = null
      }
      this.geocoder = null
      this.google = null
      if (this.mapElement) {
        this.mapElement.innerHTML = ''
        this.mapElement = null
      }
    }
  },
  async mounted() {
    await this.initMap()
    if (this.zoomToLocation) {
      await this.zoomToLocationData(this.zoomToLocation)
    }
  },
  beforeUnmount() {
    this.cleanup()
  }
}
</script>

<style>
.map-page {
  flex: 1;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-container {
  position: relative;
  width: 95%;
  max-width: 1400px;
  height: 90vh;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#map {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
}

/* Custom layer control */
.layer-control {
  position: absolute;
  top: 10px;
  left: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  z-index: 1;
}

.layer-button {
  padding: 12px 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  border-bottom: 1px solid #e6e6e6;
  transition: background-color 0.2s;
}

.layer-button:last-child {
  border-bottom: none;
}

.layer-button:hover {
  background-color: #f8f9fa;
}

.layer-button.active {
  background-color: #e8f0fe;
  color: #1a73e8;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .map-page {
    padding: 12px 24px;
  }
  
  .layer-control {
    top: auto;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: row;
  }

  .layer-button {
    padding: 8px 12px;
    border-bottom: none;
    border-right: 1px solid #e6e6e6;
  }

  .layer-button:last-child {
    border-right: none;
  }
}

/* Loading and error overlays */
.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 2;
}

.map-overlay.error {
  background-color: rgba(255, 255, 255, 0.95);
}

.alert {
  max-width: 80%;
  text-align: center;
}
</style> 