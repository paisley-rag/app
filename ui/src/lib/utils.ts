import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const baseUrl = import.meta.env.BASE_URL || '';

// export const PAISLEY_API_KEY = import.meta.env.VITE_PAISLEY_API_KEY;

//  TODO: (maybe) Add API-key for query route use
export const AXIOS_CONFIG = {
  //  headers: {
  //    "X-API-Key": PAISLEY_API_KEY
  //  }
};
