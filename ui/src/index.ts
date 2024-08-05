import { z } from "zod";
import { clientPipelineConfigSchema } from "./services/chatbot-service";

type PipelineConfig = z.infer<typeof clientPipelineConfigSchema>;

export type { PipelineConfig };
