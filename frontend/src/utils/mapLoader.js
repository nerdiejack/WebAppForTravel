import { Loader } from '@googlemaps/js-api-loader'

// Create a single instance of the loader with CSP-friendly settings
const loader = new Loader({
  apiKey: 'AIzaSyB4V-NcENgmVIrhZE6fQjzkSKZETcgZKTM',
  version: 'weekly',
  libraries: ['places', 'geometry'],
  language: 'en',
  region: 'US',
  nonce: null,
  authReferrerPolicy: 'origin',
  // Add CSP-friendly settings
  useragent: navigator.userAgent,
  channel: 'stable'
})

let loadPromise = null
let googleMaps = null

const validateGoogleMaps = (google) => {
  if (!google || !google.maps) {
    throw new Error('Google Maps failed to load properly')
  }
  return google
}

export const loadGoogleMaps = async () => {
  try {
    if (googleMaps) {
      return validateGoogleMaps(googleMaps)
    }

    if (!loadPromise) {
      loadPromise = loader.load()
        .then(google => {
          googleMaps = validateGoogleMaps(google)
          return googleMaps
        })
        .catch(error => {
          console.error('Error loading Google Maps:', error)
          loadPromise = null
          googleMaps = null
          throw new Error(`Failed to load Google Maps: ${error.message}`)
        })
    }

    return await loadPromise
  } catch (error) {
    console.error('Error in loadGoogleMaps:', error)
    loadPromise = null
    googleMaps = null
    throw error
  }
}

// Add a cleanup function
export const cleanupGoogleMaps = () => {
  loadPromise = null
  googleMaps = null
} 