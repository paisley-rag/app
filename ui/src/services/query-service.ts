import axios from "axios";
import { axiosHeader, baseUrl } from '../lib/utils.ts';
// import z from "zod";

// const querySchema = z.object({
//   message: z.string(),
//   chatbot_id: z.string(),
// });

// const responseSchema = z.object({
//   type: z.literal("response"),
//   body: z.string(),
// });

async function sendMessage(id: string, message: string, apiKey: string) {
  const response = await axios.post(`${baseUrl}/api/query`, {
    query: message,
    chatbot_id: id,
  }, axiosHeader(apiKey));
  return response.data;
}

export const queryService = {
  sendMessage,
};
