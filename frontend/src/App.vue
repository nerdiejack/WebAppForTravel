<template>
  <div class="app-container">
    <h1>Travel Planner</h1>
    <MapComponent />
  </div>
</template>

<script>
import MapComponent from "./components/MapComponent.vue";

export default {
  components: { MapComponent }
};
</script>

<style>
/* Ensure full width and height */
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Remove default margins */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
