import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(date);
}

export function parseOptionalBoolean(
  value: string | null | undefined
): boolean | null {
  if (value === "Yes" || value === "true" || value === "True") return true;
  if (value === "No" || value === "false" || value === "False") return false;
  return null;
}

export function parseOptionalNumber(
  value: string | null | undefined
): number | null {
  if (value === null || value === undefined || value === "") return null;
  const parsed = parseFloat(value);
  return isNaN(parsed) ? null : parsed;
}

export function sanitizeBacteriaPredictionInput(formData: Record<string, any>) {
  const sanitized = {
    ...formData,
    optimal_temperature: parseOptionalNumber(formData.optimal_temperature),
    mobility: parseOptionalBoolean(formData.mobility),
    flagellar_presence: parseOptionalBoolean(formData.flagellar_presence),
    sporulation: parseOptionalBoolean(formData.sporulation),
  };

  return sanitized;
}

export function ensureDefaultValues<T>(obj: Partial<T>, defaults: T): T {
  return { ...defaults, ...obj };
}
