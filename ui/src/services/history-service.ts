import axios from "axios";
import { baseUrl, AXIOS_CONFIG } from '../lib/utils.ts';

async function fetchChatbotHistory() {
  const response = await axios.get(`${baseUrl}/api/history`, AXIOS_CONFIG);
  console.log('CHAT_HISTORY IS:', response.data)
  return response.data;
}

export const historyService = {
  fetchChatbotHistory,
};
