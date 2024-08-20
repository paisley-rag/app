import axios from "axios";
import { z } from "zod";
import { AXIOS_CONFIG, baseUrl } from '../lib/utils.ts';


export const clientPipelineConfigSchema = z.object({
  id: z.string().optional(),
  name: z.string(),
  knowledge_bases: z.array(z.string()),
  generative_model: z.string(),
  similarity: z.object({
    on: z.boolean(),
    similarity_cutoff: z.number().optional(),
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

// temp, schema must be refactored on the backend
export const serverPipelineConfigSchema = z.object({
  id: z.string(),
  name: z.string(),
  generative_model: z.string(),
  knowledgebases: z.array(z.string()),
  postprocessing: z.object({
    similarity: z.object({
      on: z.string(),
      similarity_cutoff: z.number().optional(),
    }),
    colbertRerank: z.object({
      on: z.string(),
      top_n: z.number().optional(),
    }),
    longContextReorder: z.object({
      on: z.string(),
    }),
  }),
});

// const serverPipelinesConfigSchema = z.array(serverPipelineConfigSchema);

export type ClientPipelineConfig = z.infer<typeof clientPipelineConfigSchema>;
export type ServerPipelineConfig = z.infer<typeof serverPipelineConfigSchema>;

async function updateChatbot(id: string, data: ClientPipelineConfig) {
  const response = await axios.put(`${baseUrl}/api/chatbots/${id}/update`, data, AXIOS_CONFIG);
  return response.data;
}

async function createChatbot(data: ClientPipelineConfig) {
  const response = await axios.post(`${baseUrl}/api/chatbots`, data, AXIOS_CONFIG);
  return response.data;
}

async function fetchChatbots() {
  const response = await axios.get(`${baseUrl}/api/chatbots`, AXIOS_CONFIG);
  return response.data;
}

async function fetchChatbotById(id: string) {
  const response = await axios.get(`${baseUrl}/api/chatbots/${id}`, AXIOS_CONFIG);
  return response.data;
}

async function deleteChatbotById(id: string) {
  const response = await axios.delete(`${baseUrl}/api/chatbots/${id}/delete`, AXIOS_CONFIG);
  return response.data;
}

export const chatbotService = {
  updateChatbot,
  fetchChatbots,
  fetchChatbotById,
  createChatbot,
  deleteChatbotById,
};
