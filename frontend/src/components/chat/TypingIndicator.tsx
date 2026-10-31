import React from 'react';

interface TypingIndicatorProps {
  language: 'hi' | 'en';
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ language }) => {
  const isHindi = language === 'hi';

  return (
    <div className="flex w-full justify-start my-2">
      <div className="bg-white border border-stone-200 rounded-2xl rounded-tl-xs px-4 py-3 shadow-xs max-w-[85%] sm:max-w-[75%] space-y-1">
        <div className="flex items-center gap-1.5 text-[10px] text-amber-700 font-semibold mb-1">
          <span>🤖</span>
          <span>
            {isHindi
              ? 'योजना मित्र सहायक सोच रहा है...'
              : 'Yojana Mitra Assistant is thinking...'}
          </span>
        </div>
        <div className="flex items-center gap-1.5 py-1 px-1">
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:-0.3s]"></span>
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:-0.15s]"></span>
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce"></span>
        </div>
      </div>
    </div>
  );
};

