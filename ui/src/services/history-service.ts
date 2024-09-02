import axios from "axios";
import { baseUrl, axiosHeader } from '../lib/utils.ts';

async function fetchChatbotHistory(apiKey: string) {
  const response = await axios.get(`${baseUrl}/api/history`, axiosHeader(apiKey));
  return response.data;
}

export const historyService = {
  fetchChatbotHistory,
};
