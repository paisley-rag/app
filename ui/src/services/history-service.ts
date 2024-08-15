import axios from "axios";

const baseUrl = import.meta.env.VITE_BASE_URL;

async function fetchChatbotHistory() {
  const response = await axios.get(`${baseUrl}/api/history`);
  return response.data;
}

export const historyService = {
  fetchChatbotHistory,
};
