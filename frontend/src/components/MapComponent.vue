<template>
  <div class="map-wrapper">
    <LMap
      ref="mapRef"
      v-if="isMapLoaded"
      :zoom="zoom"
      :center="[13.736717, 100.523186]"
      class="map-container"
      @update:zoom="resizeMap"
      @update:center="resizeMap"
    >
      <LTileLayer :url="tileLayerUrl" />
      <LMarker v-for="city in cities" :key="city.name" :lat-lng="[city.latitude, city.longitude]">
        <LPopup>
          <strong>{{ city.name }}</strong><br />
          {{ city.country }}<br />
          Lat: {{ city.latitude }}, Lon: {{ city.longitude }}
        </LPopup>
      </LMarker>
    </LMap>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from "vue";
import { getCities } from "../services/api";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  components: { LMap, LTileLayer, LMarker, LPopup },
  setup() {
    const cities = ref([]);
    const tileLayerUrl = ref("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
    const zoom = ref(5);
    const isMapLoaded = ref(false);
    const mapRef = ref(null);

    const resizeMap = () => {
      nextTick(() => {
        if (mapRef.value?.leafletObject) {
          console.log("Resizing map...");
          mapRef.value.leafletObject.invalidateSize();
        }
      });
    };

    onMounted(async () => {
      try {
        cities.value = await getCities();
        console.log("Cities loaded:", cities.value);
        isMapLoaded.value = true;

        // Ensure the map resizes correctly after the component is loaded
        setTimeout(resizeMap, 1000);
      } catch (error) {
        console.error("Error fetching cities:", error);
      }
    });

    return { cities, tileLayerUrl, zoom, isMapLoaded, mapRef, resizeMap };
  }
};
</script>

<style>
/* Ensure the map container takes full width and height */
.map-wrapper {
  width: 100vw;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Fix map loading issues */
.map-container {
  width: 100%;
  height: 100%;
}

/* Fix leaflet tile loading issues */
.leaflet-container {
  width: 100% !important;
  height: 100% !important;
}
</style>
