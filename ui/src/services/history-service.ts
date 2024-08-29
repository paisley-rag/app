import { axiosInstance } from "../auth";
import { baseUrl } from '../lib/utils.ts';

async function fetchChatbotHistory() {
  const response = await axiosInstance.get(`${baseUrl}/api/history`);
  return response.data;
}

export const historyService = {
  fetchChatbotHistory,
};
