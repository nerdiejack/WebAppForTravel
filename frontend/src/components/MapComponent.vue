<template>
  <div class="map-wrapper">
    <div class="map-container" id="map"></div>
  </div>
</template>

<script>
import { onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { getCities } from "../services/api"; // Import API function

export default {
  setup() {
    onMounted(async () => {
      // Initialize the map
      const map = L.map("map").setView([13.736717, 100.523186], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

      try {
        // Fetch city data from FastAPI
        const cities = await getCities();
        console.log("Cities loaded:", cities);

        // Add markers for each city
        cities.forEach(city => {
          L.marker([city.latitude, city.longitude])
            .addTo(map)
            .bindPopup(`<strong>${city.name}</strong><br>${city.country}<br>Lat: ${city.latitude}, Lon: ${city.longitude}`);
        });
      } catch (error) {
        console.error("Error fetching cities:", error);
      }
    });
  }
};
</script>

<style>
/* Ensure the wrapper expands */
.map-wrapper {
  width: 100vw; /* Full screen width */
  height: 90vh; /* 90% of the screen height */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Ensure the map takes full width */
.map-container {
  width: 100%;  /* Take full width */
  height: 100%; /* Take full height */
}

/* Ensure no restrictions from body */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
</style>
