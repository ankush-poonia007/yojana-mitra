import { SubmitTextTurnRequest, StandardTurnResponse } from '../types/turn';
import { isMockMode } from './apiClient';
import {
  mockAwaitingTurnResponse,
  mockVoiceTurnResponse,
} from '../mocks/mockTurns';
import {
  mockEligibleResponse,
  mockNotEligibleResponse,
  mockCannotDetermineResponse,
} from '../mocks/mockResults';

export type PredefinedScenario = 'eligible' | 'not_eligible' | 'cannot_determine' | 'awaiting';

/**
 * Service abstraction for submitting conversation turns.
 * Isolates UI from HTTP calls and mock logic.
 */
export async function submitTextTurn(
  request: SubmitTextTurnRequest,
  scenario: PredefinedScenario = 'awaiting',
): Promise<StandardTurnResponse> {
  if (isMockMode()) {
    switch (scenario) {
      case 'eligible':
        return Promise.resolve({
          ...mockEligibleResponse,
          session_id: request.session_id,
        });
      case 'not_eligible':
        return Promise.resolve({
          ...mockNotEligibleResponse,
          session_id: request.session_id,
        });
      case 'cannot_determine':
        return Promise.resolve({
          ...mockCannotDetermineResponse,
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

  throw new Error('Real backend integration for submitTextTurn is reserved for Phase 6.');
}

export async function submitVoiceTurn(
  sessionId: string,
  _audioBlob: Blob,
  _language?: string,
): Promise<StandardTurnResponse> {
  if (isMockMode()) {
    return Promise.resolve({
      ...mockVoiceTurnResponse,
      session_id: sessionId,
    });
  }

  throw new Error('Real backend integration for submitVoiceTurn is reserved for Phase 6.');
}

