import { Loader } from '@googlemaps/js-api-loader'

const MAPS_API_KEY = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;

// Debug the API key
console.log('Google Maps API Key:', MAPS_API_KEY ? 'Present' : 'Missing');

// Create a single instance of the loader with CSP-friendly settings
const loader = new Loader({
  apiKey: MAPS_API_KEY,
  version: 'weekly',
  libraries: ['places', 'geometry'],
  language: 'en',
  region: 'US',
  authReferrerPolicy: 'origin'
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
    if (!MAPS_API_KEY) {
      throw new Error('Google Maps API key is missing')
    }

    if (googleMaps) {
      return validateGoogleMaps(googleMaps)
    }

    if (!loadPromise) {
      console.log('Initializing Google Maps...');
      loadPromise = loader.load()
        .then(google => {
          console.log('Google Maps loaded successfully');
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

export const cleanupGoogleMaps = () => {
  loadPromise = null
  googleMaps = null
} 