import axios from "axios";

const API_URL = "nhsproject-production.up.railway.app"; // New API endpoint

export const fetchData = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};


