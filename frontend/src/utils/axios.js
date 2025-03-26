import axios from 'axios'

// Create axios instance with base URL
const api = axios.create({
  baseURL: '/',  // Use root path since we include /api in the requests
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response || error)
    return Promise.reject(error)
  }
)

export default api 