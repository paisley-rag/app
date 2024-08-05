import axios from "axios";

async function sendMessage(id: string, message: string) {
  const response = await axios.post(`/api/query`, { message, chatbotId: id });
  return response.data;
}

export const queryService = {
  sendMessage,
};
