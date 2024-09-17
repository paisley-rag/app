import { axiosInstance } from "../auth";
import { baseUrl } from '../lib/utils.ts';
// import z from "zod";

// const querySchema = z.object({
//   message: z.string(),
//   chatbot_id: z.string(),
// });

// const responseSchema = z.object({
//   type: z.literal("response"),
//   body: z.string(),
// });

async function sendMessage(id: string, message: string) {
  const response = await axiosInstance.post(`${baseUrl()}/api/query`, {
    query: message,
    chatbot_id: id,
  });
  return response.data;
}

export const queryService = {
  sendMessage,
};
