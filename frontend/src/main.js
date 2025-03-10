import { createApp } from 'vue';
import './style.css';
import App from './App.vue';

// ✅ Add Leaflet CSS (Fixes Misaligned Tiles)
import "leaflet/dist/leaflet.css";

createApp(App).mount('#app');
