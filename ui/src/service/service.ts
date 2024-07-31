import axios from "axios";
import { z } from "zod";

export const pipelineConfigSchema = z.object({
  id: z.string(),
  name: z.string(),
  knowledge_bases: z.array(z.string()),
  generative_model: z.string(),
  similarity: z.object({
    on: z.boolean(),
    cutoff: z.number().optional(),
  }),
  colbert_rerank: z.object({
    on: z.boolean(),
    top_n: z.number().optional(),
  }),
  long_context_reorder: z.object({
    on: z.boolean(),
  }),
  prompt: z.string(),
});

async function fetchKnowledgeBases() {
  const response = await axios.get("/api/knowledge-bases");
  return response.data;
}

async function fetchFilesByKnolwedgeBaseId(id: string) {
  const response = await axios.get(`/api/knowledge-bases?id=${id}`);
  return response.data;
}

async function fetchChatbots() {
  const response = await axios.get(`/api/chatbots`);
  return response.data;
}

async function fetchChatbotById(id: string) {
  const response = await axios.get(`/api/chatbots?id=${id}`);

  // for testing only, should be removed when connected to backend with correct datatype of `id`
  response.data[0].id = String(response.data[0].id);
  return response.data[0];
}

async function sendMessage(id: string, message: string) {
  const response = await axios.post(`/api/query`, { message, chatbotId: id });
  return response.data;
}

async function updateChatbot(
  id: string,
  data: z.infer<typeof pipelineConfigSchema>
) {
  console.log(data);
  const response = await axios.put(`/api/chatbots?id=${id}`, data);
  return response.data;
}

export default {
  fetchKnowledgeBases,
  fetchFilesByKnolwedgeBaseId,
  fetchChatbots,
  fetchChatbotById,
  sendMessage,
  updateChatbot,
};
