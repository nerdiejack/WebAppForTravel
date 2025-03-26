import { Loader } from '@googlemaps/js-api-loader'

// Create a single instance of the loader
const loader = new Loader({
  apiKey: 'AIzaSyB4V-NcENgmVIrhZE6fQjzkSKZETcgZKTM',
  version: 'weekly',
  libraries: [],
  language: 'en'
})

let loadPromise = null

export const loadGoogleMaps = async () => {
  if (!loadPromise) {
    loadPromise = loader.load()
  }
  return loadPromise
} 