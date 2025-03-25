import axios from "axios";

const API_URL = "https://nhs-project.onrender.com"; // New API endpoint

export const fetchData = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/conditions`);
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};


