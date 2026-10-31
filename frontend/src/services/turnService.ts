import { SubmitTextTurnRequest, StandardTurnResponse } from '../types/turn';
import { isMockMode, apiRequest } from './apiClient';
import {
  mockAwaitingTurnResponse,
  mockVoiceTurnResponse,
} from '../mocks/mockTurns';
import {
  mockEligibleResponse,
  mockEligibleResponseEn,
  mockNotEligibleResponse,
  mockNotEligibleResponseEn,
  mockCannotDetermineResponse,
  mockCannotDetermineResponseEn,
} from '../mocks/mockResults';

export type PredefinedScenario = 'eligible' | 'not_eligible' | 'cannot_determine' | 'awaiting';

/**
 * Service abstraction for submitting conversation turns.
 * Isolates UI from HTTP calls and mock logic.
 * In mock mode: returns predefined fixture responses without network calls.
 * In real mode: calls POST /api/v1/turns per frozen Phase 3.3 API contract.
 */
export async function submitTextTurn(
  request: SubmitTextTurnRequest,
  scenario: PredefinedScenario = 'awaiting',
  language: 'hi' | 'en' = 'hi',
): Promise<StandardTurnResponse> {
  if (isMockMode()) {
    switch (scenario) {
      case 'eligible':
        return Promise.resolve({
          ...(language === 'en' ? mockEligibleResponseEn : mockEligibleResponse),
          session_id: request.session_id,
        });
      case 'not_eligible':
        return Promise.resolve({
          ...(language === 'en' ? mockNotEligibleResponseEn : mockNotEligibleResponse),
          session_id: request.session_id,
        });
      case 'cannot_determine':
        return Promise.resolve({
          ...(language === 'en' ? mockCannotDetermineResponseEn : mockCannotDetermineResponse),
          session_id: request.session_id,
        });
      case 'awaiting':
      default:
        return Promise.resolve({
          ...mockAwaitingTurnResponse,
          session_id: request.session_id,
        });
    }
  }

  return apiRequest<StandardTurnResponse>('/api/v1/turns', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: request.session_id,
      text: request.text,
    }),
  });
}

export async function submitVoiceTurn(
  sessionId: string,
  audioBlob: Blob,
  language?: string,
): Promise<StandardTurnResponse> {
  if (isMockMode()) {
    return Promise.resolve({
      ...mockVoiceTurnResponse,
      session_id: sessionId,
    });
  }

  const formData = new FormData();
  formData.append('session_id', sessionId);
  formData.append('audio', audioBlob, 'turn_audio.wav');
  if (language) {
    formData.append('language', language);
  }

  return apiRequest<StandardTurnResponse>('/api/v1/voice/turns', {
    method: 'POST',
    body: formData,
  });
}
