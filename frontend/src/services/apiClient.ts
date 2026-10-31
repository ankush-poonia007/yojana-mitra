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
  public readonly status: number;

  constructor(errorEnvelope: ApiErrorEnvelope, status = 500) {
    super(errorEnvelope.error.message);
    this.name = 'ApiServiceError';
    this.code = errorEnvelope.error.code;
    this.retryable = Boolean(errorEnvelope.error.retryable);
    this.details = errorEnvelope.error.details || {};
    this.status = status;
  }
}

/**
 * Executes an HTTP fetch request against the configured backend base URL,
 * parses JSON, and normalizes errors into the standard ApiErrorEnvelope format.
 * Conforms to frozen Phase 3.3 API contract error envelope.
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

  let response: Response;
  try {
    response = await fetch(url, options);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Network connection failed.';
    throw new ApiServiceError(
      {
        error: {
          code: 'NETWORK_ERROR',
          message: `Could not connect to the backend server (${message}). Please ensure the server is running.`,
          retryable: true,
          details: {},
        },
      },
      0,
    );
  }

  // Parse JSON response body
  let data: unknown = null;
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  }

  if (!response.ok) {
    // Check if error response adheres to the frozen ApiErrorEnvelope schema
    if (data && typeof data === 'object' && 'error' in data) {
      const envelope = data as ApiErrorEnvelope;
      throw new ApiServiceError(envelope, response.status);
    }

    // Fallback standard error envelope for unexpected HTTP error bodies
    throw new ApiServiceError(
      {
        error: {
          code: `HTTP_${response.status}`,
          message: response.statusText || 'An unexpected server error occurred.',
          retryable: response.status >= 500,
          details: { status: response.status },
        },
      },
      response.status,
    );
  }

  return data as T;
}
