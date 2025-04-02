const WEATHER_API_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall';

export const getWeatherData = async (lat, lon) => {
  try {
    const apiKey = process.env.VUE_APP_WEATHER_API_KEY;
    if (!apiKey) {
      console.error('Weather API key is missing');
      return null;
    }

    console.log('Fetching weather data for:', { lat, lon });
    const response = await fetch(
      `${WEATHER_API_BASE_URL}?lat=${lat}&lon=${lon}&units=metric&exclude=minutely,hourly,daily,alerts&appid=${apiKey}`
    );
    
    if (!response.ok) {
      throw new Error(`Weather data fetch failed: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Weather data received:', data);
    
    if (!data || !data.current) {
      throw new Error('Invalid weather data format received');
    }

    return {
      current: {
        temp: data.current.temp,
        weather: data.current.weather,
        pressure: data.current.pressure,
        sunrise: data.current.sunrise,
        sunset: data.current.sunset,
        humidity: data.current.humidity,
        wind_speed: data.current.wind_speed
      },
      timezone: data.timezone,
      timezone_offset: data.timezone_offset
    };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    return null;
  }
}; 