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

// temp, schema must be refactored on the backend
export const serverPipelineConfigSchema = z.object({
  id: z.string(),
  name: z.string(),
  generative_model: z.string(),
  knowledgebases: z.array(z.string()),
  postprocessing: z.object({
    similarity: z.object({
      on: z.string(),
      cutoff: z.number().optional(),
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

const serverPipelinesConfigSchema = z.array(serverPipelineConfigSchema);

export type ClientPipelineConfig = z.infer<typeof clientPipelineConfigSchema>;
export type ServerPipelineConfig = z.infer<typeof serverPipelineConfigSchema>;

async function updateChatbot(id: string, data: ClientPipelineConfig) {
  const response = await axios.put(`/api/chatbots/${id}`, data);
  return serverPipelineConfigSchema.parse(JSON.parse(response.data));
}

async function fetchChatbots() {
  const response = await axios.get(`/api/chatbots`);
  const chatbots = serverPipelinesConfigSchema.parse(JSON.parse(response.data));
  const clientChatbots: ClientPipelineConfig[] = chatbots.map((chatbot) => ({
    id: chatbot.id,
    name: chatbot.name,
    knowledge_bases: chatbot.knowledgebases,
    generative_model: chatbot.generative_model,
    similarity: {
      on: chatbot.postprocessing.similarity.on === "True",
      cutoff: chatbot.postprocessing.similarity.cutoff,
    },
    colbert_rerank: {
      on: chatbot.postprocessing.colbertRerank.on === "True",
      top_n: chatbot.postprocessing.colbertRerank.top_n,
    },
    long_context_reorder: {
      on: chatbot.postprocessing.longContextReorder.on === "True",
    },
    prompt: "",
  }));
  return clientChatbots;
}

async function fetchChatbotById(id: string) {
  const response = await axios.get(`/api/chatbots/${id}`);
  const chatbot = serverPipelineConfigSchema.parse(JSON.parse(response.data));
  console.log(chatbot);
  const clientChatbot: ClientPipelineConfig = {
    id: chatbot.id,
    name: chatbot.name,
    knowledge_bases: chatbot.knowledgebases,
    generative_model: chatbot.generative_model,
    similarity: {
      on: chatbot.postprocessing.similarity.on === "True",
      cutoff: chatbot.postprocessing.similarity.cutoff,
    },
    colbert_rerank: {
      on: chatbot.postprocessing.colbertRerank.on === "True",
      top_n: chatbot.postprocessing.colbertRerank.top_n,
    },
    long_context_reorder: {
      on: chatbot.postprocessing.longContextReorder.on === "True",
    },
    prompt: "",
  };

  return clientChatbot;
}

export const chatbotService = {
  updateChatbot,
  fetchChatbots,
  fetchChatbotById,
};
