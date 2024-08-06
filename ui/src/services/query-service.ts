import axios from "axios";

const baseUrl = import.meta.env.VITE_BASE_URL;

async function sendMessage(id: string, message: string) {
  const response = await axios.post(`${baseUrl}/api/query`, {
    message,
    chatbotId: id,
  });
  return response.data;
}

export const queryService = {
  sendMessage,
};
