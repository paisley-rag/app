import axios from "axios";

// need to add zod validation to response types

async function fetchKnowledgeBases() {
  const response = await axios.get("/api/knowledge-bases");
  return response.data;
}

async function fetchFilesByKnolwedgeBaseId(id: number) {
  const response = await axios.get(`/api/knowledge-bases?id=${id}`);
  return response.data;
}

async function fetchChatbots() {
  const response = await axios.get(`/api/chatbots`);
  return response.data;
}

async function fetchChatbotById(id: number) {
  const response = await axios.get(`/api/chatbots?id=${id}`);
  return response.data;
}

async function sendMessage(id: number, message: string) {
  const response = await axios.post(`/api/query`, { message, chatbotId: id });
  return response.data;
}

export default {
  fetchKnowledgeBases,
  fetchFilesByKnolwedgeBaseId,
  fetchChatbots,
  fetchChatbotById,
  sendMessage,
};
