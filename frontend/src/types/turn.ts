import { LanguageCode } from './session';
import { Assessment, TakeAwayCard, SourceEvidence } from './assessment';

export type TurnStatus = 'awaiting_information' | 'completed';

export interface AnswerPayload {
  text: string;
}

export interface SpeechPayload {
  status: 'generated' | 'failed' | 'not_requested' | string;
  content_type: string;
  audio_base64: string;
}

export interface TranscriptionPayload {
  text: string;
  confidence: number | null;
}

export interface StandardTurnResponse {
  session_id: string;
  turn_id: string;
  status: TurnStatus | string;
  language: LanguageCode;
  transcription?: TranscriptionPayload;
  answer: AnswerPayload;
  assessment: Assessment | null;
  card: TakeAwayCard | null;
  sources: SourceEvidence[];
  speech?: SpeechPayload;
}

export interface SubmitTextTurnRequest {
  session_id: string;
  text: string;
}

