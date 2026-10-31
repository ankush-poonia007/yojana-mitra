import {
  CreateSessionRequest,
  SessionResponse,
  SessionDetailsResponse,
} from '../types/session';
import { isMockMode, apiRequest } from './apiClient';
import { mockCreatedSession, mockSessionDetails } from '../mocks/mockSessions';

/**
 * Service abstraction for session operations.
 * In mock mode (VITE_MOCK_MODE=true): returns schema-compliant fixtures with zero network calls.
 * In real mode: connects to POST /api/v1/sessions and GET /api/v1/sessions/{id}
 * per frozen Phase 3.3 API contract.
 */
export async function createSession(
  request: CreateSessionRequest,
): Promise<SessionResponse> {
  if (isMockMode()) {
    // Return deterministic mock fixture matching shared/examples/session_create_response.json
    return Promise.resolve({
      ...mockCreatedSession,
      language: request.language,
      mode: request.mode,
      created_at: new Date().toISOString(),
    });
  }

  return apiRequest<SessionResponse>('/api/v1/sessions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      language: request.language,
      mode: request.mode,
    }),
  });
}

export async function getSession(
  sessionId: string,
): Promise<SessionDetailsResponse> {
  if (isMockMode()) {
    return Promise.resolve({
      ...mockSessionDetails,
      session_id: sessionId,
    });
  }

  return apiRequest<SessionDetailsResponse>(`/api/v1/sessions/${sessionId}`);
}
