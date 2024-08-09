import axios from "axios";
import { z } from "zod";

const HOST = 'http://52.4.226.198';

const uploadSuccessSchema = z.object({
  message: z.string(),
});

const messageSchema = z
  .object({
    type: z.string(),
    body: z.string(),
  })
  .refine((data) => data.type === "query" || data.type === "response", {
    message: "Message type must be `query` or `response`.",
  });

export async function uploadFile(formData: FormData) {
  const result = await axios(`${HOST}/api/upload`, {
    method: "POST",
    data: formData,
  });
  return uploadSuccessSchema.parse(result.data);
}

export async function sendQuery(query: string) {
  const result = await axios(`${HOST}/api/query`, {
    method: "POST",
    data: { query },
  });
  return messageSchema.parse(result.data);
}
