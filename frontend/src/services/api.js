import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const getCities = async () => {
    try {
        const response = await axios.get(`${API_URL}/map/`);
        return response.data.cities;
    } catch (error) {
        console.error("Error fetching city data:", error);
        return [];
    }
};

export const getWeather = async (city) => {
    try {
        const response = await axios.get(`${API_URL}/weather/?city=${city}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching weather data:", error);
        return null;
    }
};
