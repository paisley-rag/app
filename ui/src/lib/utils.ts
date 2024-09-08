import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const baseUrl = () => {
  const base = import.meta.env.BASE_URL || '';
  if (base !== '/') return base;
  else return '';
};
