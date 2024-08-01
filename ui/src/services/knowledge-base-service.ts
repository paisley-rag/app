import axios from "axios";
import { z } from "zod";

const markdownConfigSchema = z.object({
  num_workers: z.number(),
});
const semanticConfigSchema = z.object({
  buffer_size: z.number(),
  breakpoint_percentile_threshold: z.number(),
});
const sentenceConfigSchema = z.object({
  chunk_size: z.number(),
  chunk_overlap: z.number(),
});

export const clientKnowledgeBaseConfigSchema = z.discriminatedUnion(
  "ingestion_method",
  [
    z.object({
      kb_name: z.string(),
      ingestion_method: z.literal("LlamaParse"),
      splitter: z.string(),
      embed_config: z.discriminatedUnion("embed_provider", [
        z.object({
          embed_provider: z.literal("OpenAI"),
          embed_model: z.enum([
            "text-embedding-3-small",
            "text-embedding-3-large",
          ]),
        }),
        z.object({
          embed_provider: z.literal("Cohere"),
          embed_model: z.enum([
            "embed-english-light-v3.0",
            "embed-english-v3.0",
            "embed-multilingual-light-v3.0",
            "embed-multilingual-v3.0",
          ]),
        }),
      ]),
      splitter_config: z.union([semanticConfigSchema, sentenceConfigSchema]),
      llm_config: z.discriminatedUnion("llm_provider", [
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
      ]),
    }),
    z.object({
      kb_name: z.string(),
      ingestion_method: z.literal("Simple"),
      splitter: z.string(),
      embed_config: z.object({
        embed_provider: z.string(),
        embed_model: z.string(),
      }),
      splitter_config: markdownConfigSchema,
    }),
  ]
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
  const response = await axios.get("/api/knowledge-bases");
  return knowledgeBasesSchema.parse(response.data);
}

async function fetchKnowledgeBaseById(id: string) {
  const response = await axios.get(`/api/knowledge-bases?id=${id}`);
  return serverKnowledgeBaseConfigSchema.parse(response.data[0]);
}

async function createKnowledgeBase(config: ClientKnowledgeBaseConfig) {
  const response = await axios.post("/api/knowledge-bases", config);
  return serverKnowledgeBaseConfigSchema.parse(response.data);
}

export const knowledgeBaseService = {
  fetchKnowledgeBases,
  fetchKnowledgeBaseById,
  createKnowledgeBase,
};
