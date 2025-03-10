<template>
  <div class="map-wrapper">
    <LMap ref="mapRef" v-if="isMapLoaded" :zoom="zoom" :center="[13.736717, 100.523186]" class="map-container">
      <LTileLayer :url="tileLayerUrl" />

      <!-- ✅ City markers with weather popups -->
      <LMarker v-for="city in cities" :key="city.name" :lat-lng="[city.latitude, city.longitude]" @click="fetchWeather(city.name)">
        <LPopup>
          <strong>{{ city.name }}</strong><br />
          {{ city.country }}<br />
          Lat: {{ city.latitude }}, Lon: {{ city.longitude }}<br />
          <template v-if="weather[city.name]">
            🌡️ {{ weather[city.name].temperature }}°C<br />
            🌤️ {{ weather[city.name].weather }}<br />
            💨 Wind: {{ weather[city.name].wind_speed }} km/h<br />
            💧 Humidity: {{ weather[city.name].humidity }}%<br />
          </template>
        </LPopup>
      </LMarker>
    </LMap>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { getCities, getWeather } from "../services/api";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  components: { LMap, LTileLayer, LMarker, LPopup },
  setup() {
    const cities = ref([]);
    const weather = ref({});
    const tileLayerUrl = ref("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
    const zoom = ref(5);
    const isMapLoaded = ref(false);

    onMounted(async () => {
      try {
        cities.value = await getCities();
        console.log("Cities loaded:", cities.value);
        isMapLoaded.value = true;
      } catch (error) {
        console.error("Error fetching cities:", error);
      }
    });

    const fetchWeather = async (city) => {
      try {
        if (!weather.value[city]) {
          weather.value[city] = await getWeather(city);
          console.log(`Weather for ${city}:`, weather.value[city]);
        }
      } catch (error) {
        console.error("Error fetching weather:", error);
      }
    };

    return { cities, tileLayerUrl, zoom, isMapLoaded, weather, fetchWeather };
  }
};
</script>

<style>
.map-wrapper {
  width: 100vw;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.map-container {
  width: 100%;
  height: 100%;
}
</style>
