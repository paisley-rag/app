import axios from "axios";
import z from "zod";

const baseUrl = import.meta.env.VITE_BASE_URL;

// const querySchema = z.object({
//   message: z.string(),
//   chatbot_id: z.string(),
// });

const responseSchema = z.object({
  type: z.literal("response"),
  body: z.string(),
});

async function sendMessage(id: string, message: string) {
  const response = await axios.post(`${baseUrl}/api/query`, {
    query: message,
    chatbot_id: id,
  });
  return responseSchema.parse(response.data);
}

export const queryService = {
  sendMessage,
};
