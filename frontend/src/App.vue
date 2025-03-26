<template>
  <div class="app">
    <nav class="navbar">
      <button @click="currentView = 'map'" :class="{ active: currentView === 'map' }">Map View</button>
      <button @click="currentView = 'hotels'" :class="{ active: currentView === 'hotels' }">Hotel Reservations</button>
      <button @click="currentView = 'admin'" :class="{ active: currentView === 'admin' }">Admin Dashboard</button>
    </nav>
    <main class="main-content">
      <Map v-if="currentView === 'map'" />
      <HotelMap v-if="currentView === 'hotels'" />
      <AdminDashboard v-if="currentView === 'admin'" />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import Map from './components/Map.vue'
import HotelMap from './components/HotelMap.vue'
import AdminDashboard from './components/AdminDashboard.vue'

export default {
  name: 'App',
  components: {
    Map,
    HotelMap,
    AdminDashboard
  },
  setup() {
    const currentView = ref('map')
    return {
      currentView
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
}

.navbar button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #f0f0f0;
}

.navbar button.active {
  background-color: #007bff;
  color: white;
}

.main-content {
  flex: 1;
  position: relative;
}

/* Reset default margins */
body {
  margin: 0;
  padding: 0;
}
</style>
