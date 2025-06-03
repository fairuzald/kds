import axios, { AxiosError } from "axios";
import {
  ApiResponse,
  BacteriaPredictionInput,
  PredictionResult,
  SimilarBacteria,
} from "./types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(error: AxiosError) {
    super(error.message);
    this.name = "ApiError";
    this.status = error.response?.status || 500;
    this.data = error.response?.data || {};
  }
}

export interface PaginationParams {
  page: number;
  page_size: number;
  search?: string;
  is_pathogen?: boolean;
  gram_stain?: string;
  phylum?: string;
}

export interface BacteriaStats {
  total: number;
  pathogenic: number;
  nonPathogenic: number;
  gramPositive: number;
  gramNegative: number;
}

export const bacteriaService = {
  predictPathogenicity: async (
    data: BacteriaPredictionInput
  ): Promise<PredictionResult> => {
    try {
      const response = await api.post<ApiResponse<PredictionResult>>(
        "/predictions/predict",
        data
      );

      if (!(response.status >= 200 && response.status < 300)) {
        throw new Error(response.data.error?.detail || "API request failed");
      }

      const result = response.data.data;

      if (!Array.isArray(result.similar_bacteria)) {
        result.similar_bacteria = [];
      }

      return result;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new ApiError(error);
      }
      throw error;
    }
  },

  getBacteriaList: async (
    params: PaginationParams
  ): Promise<ApiResponse<SimilarBacteria[]>> => {
    try {
      const cleanParams: Record<string, unknown> = {};
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
          cleanParams[key] = value;
        }
      });

      const response = await api.get<ApiResponse<SimilarBacteria[]>>(
        "/bacteria",
        { params: cleanParams }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new ApiError(error);
      }
      throw error;
    }
  },

  getBacteriaById: async (
    id: number
  ): Promise<ApiResponse<SimilarBacteria>> => {
    try {
      const response = await api.get<ApiResponse<SimilarBacteria>>(
        `/bacteria/${id}`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new ApiError(error);
      }
      throw error;
    }
  },

  getBacteriaByUniqueId: async (
    uniqueId: string
  ): Promise<ApiResponse<SimilarBacteria>> => {
    try {
      const response = await api.get<ApiResponse<SimilarBacteria>>(
        `/bacteria/search/id/${uniqueId}`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new ApiError(error);
      }
      throw error;
    }
  },
};
