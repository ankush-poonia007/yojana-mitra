import { ApiErrorEnvelope } from '../types/error';

/**
 * Base configuration and helper for the API client layer.
 * Keeps UI components isolated from fetch details and mock switches.
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const isMockMode = (): boolean => {
  return import.meta.env.VITE_MOCK_MODE === 'true';
};

export class ApiServiceError extends Error {
  public readonly code: string;
  public readonly retryable: boolean;
  public readonly details: Record<string, unknown>;

  constructor(errorEnvelope: ApiErrorEnvelope) {
    super(errorEnvelope.error.message);
    this.name = 'ApiServiceError';
    this.code = errorEnvelope.error.code;
    this.retryable = errorEnvelope.error.retryable;
    this.details = errorEnvelope.error.details || {};
  }
}

