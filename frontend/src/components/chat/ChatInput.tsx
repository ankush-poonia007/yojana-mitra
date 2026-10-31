import React, { useRef, useEffect } from 'react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
  language: 'hi' | 'en';
}

export const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChange,
  onSend,
  disabled = false,
  language,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isHindi = language === 'hi';

  // Auto-resize textarea height
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && value.trim()) {
        onSend();
      }
    }
  };

  return (
    <div className="bg-white border-t border-stone-200 p-3 sm:p-4">
      <div className="max-w-3xl mx-auto flex items-end gap-2 bg-stone-50 border border-stone-300 rounded-2xl p-2 focus-within:border-amber-600 focus-within:ring-2 focus-within:ring-amber-500/20 transition-all">
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={
            isHindi
              ? 'अपना प्रश्न यहाँ लिखें... (Enter से भेजें, Shift+Enter से नई पंक्ति)'
              : 'Type your message... (Enter to send, Shift+Enter for new line)'
          }
          className="flex-1 bg-transparent resize-none border-none outline-none text-sm text-stone-900 placeholder:text-stone-400 max-h-28 py-1.5 px-2"
          aria-label={isHindi ? 'संदेश इनपुट' : 'Message input'}
        />

        <button
          type="button"
          onClick={onSend}
          disabled={disabled || !value.trim()}
          className="inline-flex items-center justify-center w-10 h-10 rounded-xl bg-slate-900 text-amber-500 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all active:scale-95 cursor-pointer shadow-xs shrink-0"
          aria-label={isHindi ? 'संदेश भेजें' : 'Send message'}
        >
          <svg
            className="w-5 h-5 translate-x-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
      <div className="max-w-3xl mx-auto text-[11px] text-stone-400 mt-1.5 px-1 flex items-center justify-between">
        <span>
          {isHindi
            ? 'केवल सूचनात्मक मार्गदर्शन | आधिकारिक निर्णय नहीं'
            : 'Indicative guidance only | Not an official decision'}
        </span>
        <span className="hidden sm:inline">Enter ↵</span>
      </div>
    </div>
  );
};

