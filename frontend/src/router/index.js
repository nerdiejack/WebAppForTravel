import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import HotelView from '../components/HotelView.vue'
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
    component: HotelView
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