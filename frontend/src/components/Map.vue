<template>
  <div class="map-page">
    <div class="map-container">
      <div id="map"></div>
      <!-- Custom layer control -->
      <div class="layer-control">
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
  data() {
    return {
      map: null,
      currentMapType: 'roadmap'
    }
  },
  methods: {
    setMapType(type) {
      if (this.map) {
        this.map.setMapTypeId(type);
        this.currentMapType = type;
      }
    }
  },
  async mounted() {
    try {
      const google = await loadGoogleMaps();
      
      // Initialize the map with more Google-like defaults
      this.map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 13.7563, lng: 100.5018 }, // Bangkok coordinates
        zoom: 6,
        mapTypeControl: false, // Hide default type control
        streetViewControl: true,
        streetViewControlOptions: {
          position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        fullscreenControl: true,
        fullscreenControlOptions: {
          position: google.maps.ControlPosition.RIGHT_TOP
        },
        zoomControl: true,
        zoomControlOptions: {
          position: google.maps.ControlPosition.RIGHT_CENTER
        },
        scaleControl: true,
        rotateControl: true,
        language: 'en',
        gestureHandling: 'greedy', // Enables one-finger zoom on mobile
        styles: [
          {
            featureType: 'administrative',
            elementType: 'labels',
            stylers: [{ visibility: 'on' }]
          },
          {
            featureType: 'water',
            elementType: 'geometry',
            stylers: [{ color: '#aadaff' }]
          }
        ]
      });

    } catch (error) {
      console.error('Error loading Google Maps:', error);
    }
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
</style> 