import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const baseUrl = import.meta.env.VITE_BASE_URL || '';

export const axiosHeader = (apiKey: string) => {
  return {
    headers: {
      "X-API-Key": apiKey
    }
  };
};