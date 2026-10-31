import React from 'react';
import { StandardTurnResponse } from '../../types/turn';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  text: string;
  transcriptionTag?: boolean;
  language: 'hi' | 'en';
  assessmentResult?: StandardTurnResponse | null;
  onViewResult?: (result: StandardTurnResponse) => void;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  role,
  text,
  transcriptionTag = false,
  language,
  assessmentResult,
  onViewResult,
}) => {
  const isUser = role === 'user';
  const isHindi = language === 'hi';

  const hasAssessment = Boolean(assessmentResult && assessmentResult.assessment);
  const outcome = assessmentResult?.assessment?.result;

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 shadow-xs text-sm leading-relaxed ${
          isUser
            ? 'bg-emerald-600 text-white rounded-tr-xs'
            : 'bg-white border border-stone-200 text-stone-900 rounded-tl-xs'
        }`}
      >
        <div className="flex items-center justify-between gap-2 mb-1">
          <span
            className={`text-[10px] font-semibold uppercase tracking-wider ${
              isUser ? 'text-emerald-100' : 'text-amber-700'
            }`}
          >
            {isUser
              ? isHindi
                ? 'आप'
                : 'You'
              : isHindi
              ? '🤖 योजना मित्र सहायक'
              : '🤖 Yojana Mitra Assistant'}
          </span>
          {!isUser && (
            <span className="text-[9px] bg-amber-50 text-amber-800 border border-amber-200 px-1.5 py-0.2 rounded font-medium">
              {isHindi ? 'नमूना उत्तर' : 'Sample Reply'}
            </span>
          )}
          {isUser && transcriptionTag && (
            <span className="text-[9px] bg-emerald-700/80 text-emerald-100 px-1.5 py-0.2 rounded font-medium">
              {isHindi ? 'बोलकर पूछा' : 'Spoken'}
            </span>
          )}
        </div>

        <p className="whitespace-pre-wrap">{text}</p>

        {/* Explicit Action: View Result when an assessment payload is present */}
        {!isUser && hasAssessment && assessmentResult && onViewResult && (
          <div className="mt-3 pt-3 border-t border-stone-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-stone-50/80 -mx-2 px-3 py-2.5 rounded-xl border">
            <div className="text-xs">
              <span className="font-semibold text-stone-800 block text-[11px]">
                {isHindi ? '📊 पात्रता मूल्यांकन तैयार है' : '📊 Assessment Ready'}
              </span>
              <span className="text-[10px] text-stone-500 font-mono">
                {outcome === 'likely_eligible' && '✅ likely_eligible'}
                {outcome === 'likely_not_eligible' && '⚠️ likely_not_eligible'}
                {outcome === 'cannot_determine' && '❓ cannot_determine'}
              </span>
            </div>
            <button
              type="button"
              onClick={() => onViewResult(assessmentResult)}
              className="inline-flex items-center justify-center gap-1.5 text-xs font-bold bg-amber-600 hover:bg-amber-700 text-white px-3 py-1.5 rounded-lg shadow-2xs transition-colors shrink-0 cursor-pointer active:scale-95"
            >
              <span>{isHindi ? 'परिणाम देखें' : 'View Result'}</span>
              <span>→</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
