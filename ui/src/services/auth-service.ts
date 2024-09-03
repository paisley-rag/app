import { axiosInstance } from "../auth";
import { baseUrl } from "../lib/utils";

export async function authenticate(username: string, password: string) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await axiosInstance.post(`${baseUrl}/api/token`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data.access_token;
}
