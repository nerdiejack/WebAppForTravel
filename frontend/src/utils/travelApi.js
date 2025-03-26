import axios from 'axios'

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
const SKYSCANNER_API_KEY = import.meta.env.VITE_SKYSCANNER_API_KEY

// Google Maps Distance Matrix API
export const searchRoutes = async (from, to, date) => {
  try {
    // First, get the coordinates for both locations using Geocoding API
    const fromCoords = await getCoordinates(from)
    const toCoords = await getCoordinates(to)

    // Get driving route
    const drivingRoute = await getDrivingRoute(fromCoords, toCoords)
    
    // Get transit route if available
    const transitRoute = await getTransitRoute(fromCoords, toCoords, date)

    // Get flight options if available
    const flightOptions = await getFlightOptions(from, to, date)

    // Combine all options
    const routes = [
      ...drivingRoute,
      ...transitRoute,
      ...flightOptions
    ]

    return routes
  } catch (error) {
    console.error('Error searching routes:', error)
    throw error
  }
}

const getCoordinates = async (location) => {
  try {
    const geocoder = new google.maps.Geocoder()
    const response = await geocoder.geocode({ address: location })
    if (response.results[0]) {
      return response.results[0].geometry.location
    }
    throw new Error('Location not found')
  } catch (error) {
    console.error('Error getting coordinates:', error)
    throw error
  }
}

const getDrivingRoute = async (from, to) => {
  try {
    const service = new google.maps.DistanceMatrixService()
    const response = await service.getDistanceMatrix({
      origins: [from],
      destinations: [to],
      travelMode: google.maps.TravelMode.DRIVING,
      drivingOptions: {
        departureTime: new Date(),
        trafficModel: google.maps.TrafficModel.BEST_GUESS
      }
    })

    if (response.rows[0].elements[0].status === 'OK') {
      const element = response.rows[0].elements[0]
      return [{
        id: 'driving',
        name: 'Car',
        duration: element.duration.text,
        price: '€' + (element.distance.value * 0.2).toFixed(2), // Rough estimate: €0.20 per km
        transportType: 'Car',
        departureTime: 'Flexible',
        arrivalTime: 'Flexible',
        stops: 'Direct',
        distance: element.distance.text,
        mode: 'driving'
      }]
    }
    return []
  } catch (error) {
    console.error('Error getting driving route:', error)
    return []
  }
}

const getTransitRoute = async (from, to, date) => {
  try {
    const service = new google.maps.DistanceMatrixService()
    const response = await service.getDistanceMatrix({
      origins: [from],
      destinations: [to],
      travelMode: google.maps.TravelMode.TRANSIT,
      transitOptions: {
        routingPreference: google.maps.TransitRoutePreference.FEWER_TRANSFERS
      }
    })

    if (response.rows[0].elements[0].status === 'OK') {
      const element = response.rows[0].elements[0]
      return [{
        id: 'transit',
        name: 'Public Transit',
        duration: element.duration.text,
        price: '€' + (element.distance.value * 0.1).toFixed(2), // Rough estimate: €0.10 per km
        transportType: 'Transit',
        departureTime: 'Check local schedule',
        arrivalTime: 'Check local schedule',
        stops: 'Multiple',
        distance: element.distance.text,
        mode: 'transit'
      }]
    }
    return []
  } catch (error) {
    console.error('Error getting transit route:', error)
    return []
  }
}

const getFlightOptions = async (from, to, date) => {
  try {
    // Using Skyscanner API
    const response = await axios.get('https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create', {
      params: {
        apiKey: SKYSCANNER_API_KEY,
        origin: from,
        destination: to,
        date: date,
        adults: 1,
        currency: 'EUR'
      }
    })

    // Process flight results
    return response.data.itineraries.map(flight => ({
      id: flight.id,
      name: `${flight.legs[0].carriers.marketing.name} Flight`,
      duration: formatDuration(flight.legs[0].durationInMinutes),
      price: `€${flight.pricingOptions[0].price.amount}`,
      transportType: 'Flight',
      departureTime: formatTime(flight.legs[0].departure),
      arrivalTime: formatTime(flight.legs[0].arrival),
      stops: flight.legs[0].stopCount === 0 ? 'Direct' : `${flight.legs[0].stopCount} stops`,
      distance: `${flight.legs[0].distance} km`,
      mode: 'flight'
    }))
  } catch (error) {
    console.error('Error getting flight options:', error)
    return []
  }
}

export const getRouteDetails = async (routeId) => {
  try {
    // For flights, get details from Skyscanner
    const response = await axios.get(`https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/${routeId}`, {
      params: {
        apiKey: SKYSCANNER_API_KEY
      }
    })
    return response.data
  } catch (error) {
    console.error('Error getting route details:', error)
    throw error
  }
}

export const getAutocompleteSuggestions = async (query) => {
  try {
    // Use Google Places Autocomplete
    const service = new google.maps.places.AutocompleteService()
    const response = await service.getPlacePredictions({
      input: query,
      types: ['(cities)']
    })
    return response.predictions.map(prediction => ({
      id: prediction.place_id,
      name: prediction.description
    }))
  } catch (error) {
    console.error('Error getting autocomplete suggestions:', error)
    throw error
  }
}

// Helper functions for formatting
const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}h ${mins}m`
}

const formatTime = (time) => {
  return new Date(time).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
} 