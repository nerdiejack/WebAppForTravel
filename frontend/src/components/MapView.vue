<template>
  <div>
    <h2>City List</h2>
    <ul>
      <li v-for="city in cities" :key="city.name">
        {{ city.name }} ({{ city.country }}) - Lat: {{ city.latitude }}, Lon: {{ city.longitude }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getCities } from '../services/api';

export default {
  setup() {
    const cities = ref([]);

    onMounted(async () => {
      cities.value = await getCities();
    });

    return { cities };
  }
};
</script>
