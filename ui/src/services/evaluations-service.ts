import axios from "axios";

async function fetchChatbotHistory() {
  const response = await axios.get(`/api/history`);
  return response.data.table_data;
}

export const evaluationsService = {
  fetchChatbotHistory,
};
