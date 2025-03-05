import axios from "axios";

const API_URL = "http://localhost:5000"; // Backend URL

export const getArticles = async () => {
    try {
        const response = await axios.get(`${API_URL}/articles`);
        return response.data;
    } catch (error) {
        console.error("Error fetching articles:", error);
        return [];
    }
};

export const getArticleById = async (id) => {
    try {
        const response = await axios.get(`${API_URL}/articles/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching article:", error);
        return null;
    }
};
