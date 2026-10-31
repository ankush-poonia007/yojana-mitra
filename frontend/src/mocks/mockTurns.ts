import { StandardTurnResponse } from '../types/turn';

/**
 * Standard turn response representing awaiting_information workflow status.
 * Matches shared/examples/turn_awaiting_response.json
 */
export const mockAwaitingTurnResponse: StandardTurnResponse = {
  session_id: 'sess_demo_001',
  turn_id: 'turn_003',
  status: 'awaiting_information',
  language: 'hi',
  answer: {
    text: 'मैं आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से LPG कनेक्शन है?',
  },
  assessment: null,
  card: null,
  sources: [],
  speech: {
    status: 'generated',
    content_type: 'audio/mpeg',
    audio_base64: 'DEMO_AUDIO_DATA',
  },
};

/**
 * Voice turn response matching shared/examples/voice_turn_response.json
 */
export const mockVoiceTurnResponse: StandardTurnResponse = {
  session_id: 'sess_demo_001',
  turn_id: 'turn_004',
  status: 'awaiting_information',
  language: 'hi',
  transcription: {
    text: 'मेरे घर में पहले से गैस कनेक्शन नहीं है।',
    confidence: null,
  },
  answer: {
    text: 'समझ गया। क्या आवेदन करने वाली महिला की उम्र 18 वर्ष या उससे अधिक है?',
  },
  assessment: null,
  card: null,
  sources: [],
  speech: {
    status: 'generated',
    content_type: 'audio/mpeg',
    audio_base64: 'DEMO_AUDIO_DATA',
  },
};

