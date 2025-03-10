import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

export const getCities = async () => {
  const response = await axios.get(`${API_BASE_URL}/map/`);
  return response.data.cities;
};

export const getWeather = async (city) => {
  const response = await axios.get(`${API_BASE_URL}/weather/?city=${city}`);
  return response.data;
};
