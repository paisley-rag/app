import axios from "axios";

// need to add zod validation to response types

async function fetchKnowledgeBases() {
  const response = await axios.get("/api/knowledge-bases");
  return response.data;
}

async function fetchFilesByKnolwedgeBaseId(id: number) {
  const response = await axios.get(`/api/knowledge-bases?id=${id}`);
  return response.data;
}

export default { fetchKnowledgeBases, fetchFilesByKnolwedgeBaseId };
