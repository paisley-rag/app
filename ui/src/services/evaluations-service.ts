import axios from "axios";

const baseUrl = import.meta.env.VITE_BASE_URL;

async function fetchChatbotHistory() {
  console.log('BASE URL', baseUrl)
  const response = await axios.get(`${baseUrl}/api/history`);
  console.log('RESPONSE IS:', response)
  console.log('RESPONSE.DATA IS:', response.data)
  console.log('RESPONSE.DATA[TABLE_DATA] IS:', response.data['table_data'])
  
  return response.data['table_data'];
}

export const evaluationsService = {
  fetchChatbotHistory,
};
