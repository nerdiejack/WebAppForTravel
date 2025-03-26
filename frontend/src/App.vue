<template>
  <div class="app">
    <nav class="navbar">
      <button @click="currentView = 'map'" :class="{ active: currentView === 'map' }">Map View</button>
      <button @click="currentView = 'hotels'" :class="{ active: currentView === 'hotels' }">Hotel Reservations</button>
      <button @click="currentView = 'admin'" :class="{ active: currentView === 'admin' }">Admin Dashboard</button>
      <button @click="currentView = 'travel'" :class="{ active: currentView === 'travel' }">Travel Planner</button>
    </nav>
    <main class="main-content">
      <template v-if="currentView === 'map'">
        <Map :zoom-to-location="zoomToLocation" />
      </template>
      <template v-if="currentView === 'hotels'">
        <HotelMap />
      </template>
      <template v-if="currentView === 'admin'">
        <AdminDashboard />
      </template>
      <template v-if="currentView === 'travel'">
        <TravelPlanner />
      </template>
    </main>
  </div>
</template>

<script>
import { ref, shallowRef } from 'vue'
import Map from './components/Map.vue'
import HotelMap from './components/HotelMap.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import TravelPlanner from './components/TravelPlanner.vue'

export default {
  name: 'App',
  components: {
    Map,
    HotelMap,
    AdminDashboard,
    TravelPlanner
  },
  setup() {
    const currentView = shallowRef('map')
    const zoomToLocation = shallowRef(null)

    const handleZoomToLocation = (location) => {
      zoomToLocation.value = location
      currentView.value = 'map'
    }

    return {
      currentView,
      zoomToLocation,
      handleZoomToLocation
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
}

.app {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.navbar {
  padding: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 1rem;
  z-index: 1000;
}

.navbar button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #f0f0f0;
  transition: background-color 0.2s ease;
}

.navbar button.active {
  background-color: #007bff;
  color: white;
}

.navbar button:hover:not(.active) {
  background-color: #e0e0e0;
}

.main-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.main-content > * {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
