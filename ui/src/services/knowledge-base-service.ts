import axios from "axios";
import { z } from "zod";

const baseUrl = import.meta.env.VITE_BASE_URL;

// Common Schemas
const markdownSplitterConfig = z.object({
  splitter: z.literal("Markdown"),
  splitter_config: z.object({
    num_workers: z.number(),
  }),
});

const semanticSplitterConfig = z.object({
  splitter: z.literal("Semantic"),
  splitter_config: z.object({
    buffer_size: z.number(),
    breakpoint_percentile_threshold: z.number(),
  }),
});

const sentenceSplitterConfig = z.object({
  splitter: z.literal("Sentence"),
  splitter_config: z.object({
    chunk_size: z.number(),
    chunk_overlap: z.number(),
  }),
});

const openAIEmbedConfig = z.object({
  embed_provider: z.literal("OpenAI"),
  embed_model: z.enum(["text-embedding-3-small", "text-embedding-3-large"]),
});

const cohereEmbedConfig = z.object({
  embed_provider: z.literal("Cohere"),
  embed_model: z.enum([
    "embed-english-light-v3.0",
    "embed-english-v3.0",
    "embed-multilingual-light-v3.0",
    "embed-multilingual-v3.0",
  ]),
});

// Main Schemas
const splitterConfigSchema = z.discriminatedUnion("splitter", [
  markdownSplitterConfig,
  semanticSplitterConfig,
  sentenceSplitterConfig,
]);

const embeddingConfigSchema = z.discriminatedUnion("embed_provider", [
  openAIEmbedConfig,
  cohereEmbedConfig,
]);

const llmConfigSchema = z.discriminatedUnion("llm_provider", [
  z.object({
    llm_provider: z.literal("OpenAI"),
    llm_model: z.enum([
      "gpt-3.5-turbo",
      "gpt-4-turbo",
      "gpt-4o-mini",
      "gpt-4o",
    ]),
  }),
  z.object({
    llm_provider: z.literal("Anthropic"),
    llm_model: z.enum([
      "claude-4-haiku-20240307",
      "claude-3-sonnet-20240229",
      "claude-3-5-sonnet-20240620",
    ]),
  }),
]);

export const clientKnowledgeBaseConfigSchema = z.intersection(
  z.union([
    z.object({
      kb_name: z.string(),
      ingest_method: z.literal("LlamaParse"),
      llm_config: llmConfigSchema,
      embed_config: embeddingConfigSchema,
    }),
    z.object({
      kb_name: z.string(),
      ingest_method: z.literal("Simple"),
      embed_config: embeddingConfigSchema,
    }),
  ]),
  splitterConfigSchema
);

const fileSchema = z.object({
  file_name: z.string(),
  content_type: z.string(),
  date_uploaded: z.string(),
  time_uploaded: z.string(),
});

const serverKnowledgeBaseFields = z.object({
  id: z.string(),
  files: z.array(fileSchema),
});

const serverKnowledgeBaseConfigSchema = z.intersection(
  clientKnowledgeBaseConfigSchema,
  serverKnowledgeBaseFields
);

const knowledgeBasesSchema = z.array(serverKnowledgeBaseConfigSchema);

export type ClientKnowledgeBaseConfig = z.infer<
  typeof clientKnowledgeBaseConfigSchema
>;

export type ServerKnowledgeBaseConfig = z.infer<
  typeof serverKnowledgeBaseConfigSchema
>;

async function fetchKnowledgeBases() {
  const response = await axios.get(`${baseUrl}/api/knowledge-bases`);
  console.log(response);
  try {
    return knowledgeBasesSchema.parse(response.data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("Zod validation error:", error.errors);
    }
    throw error;
  }
}

async function fetchKnowledgeBaseById(id: string) {
  const response = await axios.get(`${baseUrl}/api/knowledge-bases?id=${id}`);
  return serverKnowledgeBaseConfigSchema.parse(response.data[0]);
}

async function createKnowledgeBase(config: ClientKnowledgeBaseConfig) {
  const response = await axios.post(`${baseUrl}/api/knowledge-bases`, config);
  return serverKnowledgeBaseConfigSchema.parse(response.data);
}

export const knowledgeBaseService = {
  fetchKnowledgeBases,
  fetchKnowledgeBaseById,
  createKnowledgeBase,
};
