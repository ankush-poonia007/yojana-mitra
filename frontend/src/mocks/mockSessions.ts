import { SessionResponse, SessionDetailsResponse } from '../types/session';

/**
 * Matches shared/examples/session_create_response.json
 */
export const mockCreatedSession: SessionResponse = {
  session_id: 'sess_demo_001',
  status: 'active',
  language: 'hi',
  mode: 'voice',
  created_at: '2026-10-30T18:30:00Z',
};

/**
 * Matches shared/examples/session_get_response.json
 */
export const mockSessionDetails: SessionDetailsResponse = {
  session_id: 'sess_demo_001',
  status: 'active',
  language: 'hi',
  mode: 'voice',
  turns: [
    {
      turn_id: 'turn_001',
      role: 'user',
      text: 'क्या मैं उज्ज्वला योजना के लिए पात्र हूं?',
    },
    {
      turn_id: 'turn_002',
      role: 'assistant',
      text: 'क्या आपके घर में पहले से LPG कनेक्शन है?',
    },
  ],
};

