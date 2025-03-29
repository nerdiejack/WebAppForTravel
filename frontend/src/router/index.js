import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import HotelMap from '../components/HotelMap.vue'
import TravelDiary from '../components/TravelDiary.vue'
import AdminDashboard from '../components/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/hotels',
    name: 'Hotels',
    component: HotelMap
  },
  {
    path: '/diary',
    name: 'TravelDiary',
    component: TravelDiary
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminDashboard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 