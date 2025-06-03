import { z } from "zod";

export const bacteriaPredictionSchema = z.object({
  bacteria_id: z.string().optional(),
  name: z.string().optional(),
  superkingdom: z.string().optional(),
  kingdom: z.string().optional(),
  phylum: z.string().optional(),
  class_name: z.string().optional(),
  order: z.string().optional(),
  family: z.string().optional(),
  genus: z.string().optional(),
  species: z.string().optional(),
  strain: z.string().optional(),
  gram_stain: z.string().optional(),
  shape: z.string().optional(),
  mobility: z.string().optional().nullable(),
  flagellar_presence: z.string().optional().nullable(),
  number_of_membranes: z.string().optional().nullable(),
  oxygen_preference: z.string().optional().nullable(),
  optimal_temperature: z.string().optional().nullable(),
  temperature_range: z.string().optional().nullable(),
  habitat: z.string().optional().nullable(),
  biotic_relationship: z.string().optional().nullable(),
  cell_arrangement: z.string().optional().nullable(),
  sporulation: z.string().optional().nullable(),
  metabolism: z.string().optional().nullable(),
  energy_source: z.string().optional().nullable(),
});

export type BacteriaPredictionInput = z.infer<typeof bacteriaPredictionSchema>;

export interface SimilarBacteria {
  id?: number;
  bacteria_id: string;
  name: string | null;
  superkingdom?: string | null;
  kingdom?: string | null;
  phylum?: string | null;
  class_name?: string | null;
  order?: string | null;
  family?: string | null;
  genus?: string | null;
  species?: string | null;
  strain?: string | null;
  gram_stain?: string | null;
  shape?: string | null;
  mobility?: boolean | null;
  flagellar_presence?: boolean | null;
  number_of_membranes?: string | null;
  oxygen_preference?: string | null;
  optimal_temperature?: number | null;
  temperature_range?: string | null;
  habitat?: string | null;
  biotic_relationship?: string | null;
  cell_arrangement?: string | null;
  sporulation?: boolean | null;
  metabolism?: string | null;
  energy_source?: string | null;
  is_pathogen?: boolean | null;
  similarity_score: number;
  created_at?: string;
  updated_at?: string;
}

export interface PredictionResult {
  input_bacteria: BacteriaPredictionInput;
  is_pathogen_prediction: boolean;
  pathogen_probability: number;
  similar_bacteria: SimilarBacteria[];
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  error?: {
    detail: string;
  };
  meta?: {
    current_page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_previous: boolean;
    has_next: boolean;
  };
}

export interface BacteriaStats {
  total: number;
  pathogenic: number;
  nonPathogenic: number;
  gramPositive: number;
  gramNegative: number;
}

export interface PaginationMeta {
  total_items: number;
  total_pages: number;
  current_page: number;
  page_size: number;
}

export interface PaginationParams {
  page: number;
  page_size: number;
  search?: string;
  is_pathogen?: boolean;
  gram_stain?: string;
  phylum?: string;
}

export interface FilterFormData {
  name: string;
  gramStain: string;
  isPathogen: string;
  phylum: string;
}
