import axios from "axios";
import { z } from "zod";

export const pipelineConfigSchema = z.object({
  id: z.string(),
  name: z.string(),
  knowledge_bases: z.array(z.string()),
  generative_model: z.string(),
  postprocessing: z.object({
    similarity: z.object({
      on: z.boolean(),
      cutoff: z.number(),
    }),
    colbert_rerank: z.object({
      on: z.boolean(),
      top_n: z.number(),
    }),
    long_context_reorder: z.object({
      on: z.boolean(),
    }),
  }),
  prompt: z.string(),
});

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
  return response.data[0];
}

async function sendMessage(id: number, message: string) {
  const response = await axios.post(`/api/query`, { message, chatbotId: id });
  return response.data;
}

async function updateChatbot(
  id: number,
  data: z.infer<typeof pipelineConfigSchema>
) {
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
