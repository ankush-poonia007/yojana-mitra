export type LanguageCode = 'hi' | 'en';
export type InteractionMode = 'voice' | 'text';
export type SessionStatus = 'active' | 'completed' | 'expired';

export interface CreateSessionRequest {
  language: LanguageCode;
  mode: InteractionMode;
}

export interface SessionResponse {
  session_id: string;
  status: SessionStatus | string;
  language: LanguageCode;
  mode: InteractionMode;
  created_at: string;
}

export interface SessionHistoryTurn {
  turn_id: string;
  role: 'user' | 'assistant';
  text: string;
}

export interface SessionDetailsResponse {
  session_id: string;
  status: SessionStatus | string;
  language: LanguageCode;
  mode: InteractionMode;
  turns: SessionHistoryTurn[];
}
