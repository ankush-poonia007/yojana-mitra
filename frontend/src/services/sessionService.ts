import {
  CreateSessionRequest,
  SessionResponse,
  SessionDetailsResponse,
} from '../types/session';
import { isMockMode } from './apiClient';
import { mockCreatedSession, mockSessionDetails } from '../mocks/mockSessions';

/**
 * Service abstraction for session operations.
 * When VITE_MOCK_MODE=true, returns schema-compliant fixtures.
 * When real API mode is active, connects to POST /api/v1/sessions and GET /api/v1/sessions/{id}.
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

  throw new Error('Real backend integration for createSession is reserved for Phase 6.');
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

  throw new Error('Real backend integration for getSession is reserved for Phase 6.');
}

