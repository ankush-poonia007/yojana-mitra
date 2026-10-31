import React from 'react';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  text: string;
  transcriptionTag?: boolean;
  language: 'hi' | 'en';
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  role,
  text,
  transcriptionTag = false,
  language,
}) => {
  const isUser = role === 'user';
  const isHindi = language === 'hi';

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
      </div>
    </div>
  );
};

