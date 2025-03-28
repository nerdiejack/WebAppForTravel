import { WEATHER_API_KEY, WEATHER_API_BASE_URL } from '../config/weather';

export const getWeatherData = async (lat, lon) => {
  try {
    const response = await fetch(
      `${WEATHER_API_BASE_URL}/weather?lat=${lat}&lon=${lon}&units=metric&appid=${WEATHER_API_KEY}`
    );
    
    if (!response.ok) {
      throw new Error('Weather data fetch failed');
    }

    const data = await response.json();
    
    // Get timezone offset in milliseconds
    const timezoneOffset = data.timezone * 1000;
    
    // Calculate local time for the location
    const utcTime = new Date();
    const localTime = new Date(utcTime.getTime() + timezoneOffset);
    
    // Calculate sunrise time in local timezone
    const sunriseUTC = new Date(data.sys.sunrise * 1000);
    const sunriseLocal = new Date(sunriseUTC.getTime() + timezoneOffset);
    
    // Calculate sunset time in local timezone
    const sunsetUTC = new Date(data.sys.sunset * 1000);
    const sunsetLocal = new Date(sunsetUTC.getTime() + timezoneOffset);

    return {
      temperature: Math.round(data.main.temp),
      description: data.weather[0].description,
      icon: data.weather[0].icon,
      sunrise: sunriseLocal.toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC'
      }),
      sunset: sunsetLocal.toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC'
      }),
      timezone: data.timezone,
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed * 3.6) // Convert m/s to km/h
    };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    return null;
  }
}; 