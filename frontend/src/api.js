import axios from "axios";

// Base URL for the deployed backend
const API_URL = "https://nhs-project.onrender.com/api";

// Fetch the full translated conditions with sections and paragraphs
export const fetchData = async () => {
  try {
    const response = await axios.get(`${API_URL}/translated-conditions`);
    return response.data;
  } catch (error) {
    console.error("❌ Error fetching translated conditions:", error.message);
    return [];
  }
};
