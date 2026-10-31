import React from 'react';
import { APP_STRINGS } from '../../utils/constants';
import { LanguageCode } from '../../types/session';

interface HeaderProps {
  language: LanguageCode;
  onLanguageChange: (lang: LanguageCode) => void;
  onReset: () => void;
  showReset: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  language,
  onLanguageChange,
  onReset,
  showReset,
}) => {
  const isMockMode = import.meta.env.VITE_MOCK_MODE === 'true';

  return (
    <header className="bg-white border-b border-stone-200 sticky top-0 z-30 shadow-xs">
      {isMockMode && (
        <div className="bg-amber-100 text-amber-900 text-xs px-3 py-1 font-medium text-center border-b border-amber-200 flex items-center justify-center gap-1.5">
          <span className="inline-block w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          <span>{APP_STRINGS.mockBadge[language]}: VITE_MOCK_MODE active</span>
        </div>
      )}
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-lg bg-slate-900 text-amber-500 flex items-center justify-center font-bold text-lg shadow-inner">
            YM
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-900 leading-tight">
              {APP_STRINGS.appName[language]}
            </h1>
            <p className="text-xs text-stone-500">
              {language === 'hi' ? 'बोलकर या लिखकर समझें' : 'Voice & Text Assistant'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Language Switcher Pill */}
          <div className="inline-flex rounded-full bg-stone-100 p-0.5 border border-stone-200">
            <button
              type="button"
              onClick={() => onLanguageChange('hi')}
              className={`px-3 py-1 text-xs font-semibold rounded-full transition-colors ${
                language === 'hi'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-stone-600 hover:text-stone-900'
              }`}
            >
              हिन्दी
            </button>
            <button
              type="button"
              onClick={() => onLanguageChange('en')}
              className={`px-3 py-1 text-xs font-semibold rounded-full transition-colors ${
                language === 'en'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-stone-600 hover:text-stone-900'
              }`}
            >
              English
            </button>
          </div>

          {showReset && (
            <button
              type="button"
              onClick={onReset}
              className="text-xs font-medium text-stone-600 hover:text-slate-900 px-2.5 py-1.5 rounded-lg border border-stone-200 hover:bg-stone-50 transition-colors"
            >
              {APP_STRINGS.resetSession[language]}
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

