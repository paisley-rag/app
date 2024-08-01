import axios from "axios";
import { z } from "zod";

export const clientPipelineConfigSchema = z.object({
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

export type ClientPipelineConfig = z.infer<typeof clientPipelineConfigSchema>;

async function updateChatbot(id: string, data: ClientPipelineConfig) {
  const response = await axios.put(`/api/chatbots?id=${id}`, data);
  return response.data;
}

async function fetchChatbots() {
  const response = await axios.get(`/api/chatbots`);
  return response.data;
}

async function fetchChatbotById(id: string) {
  const response = await axios.get(`/api/chatbots?id=${id}`);
  return response.data[0];
}

export const chatbotService = {
  updateChatbot,
  fetchChatbots,
  fetchChatbotById,
};
