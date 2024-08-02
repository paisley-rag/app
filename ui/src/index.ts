import { z } from "zod";
import { pipelineConfigSchema } from "./services/chatbot";

type PipelineConfig = z.infer<typeof pipelineConfigSchema>;

export type { PipelineConfig };
