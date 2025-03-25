import axios from "axios";

const API_URL = "https://nhs-project.onrender.com/api";

// Fetch full translated condition data
export const fetchData = async () => {
  try {
    const response = await axios.get(`${API_URL}/translated-conditions`);
    console.log("✅ Data received from backend:", response.data); // for debugging
    return response.data;
  } catch (error) {
    console.error("❌ Error fetching data:", error);
    throw error;
  }
};
