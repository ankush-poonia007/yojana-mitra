import React from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { LanguageCode } from '../types/session';

interface LanguageSelectScreenProps {
  currentLanguage: LanguageCode;
  onSelectLanguage: (lang: LanguageCode) => void;
  onContinue: () => void;
}

export const LanguageSelectScreen: React.FC<LanguageSelectScreenProps> = ({
  currentLanguage,
  onSelectLanguage,
  onContinue,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-6 px-4 max-w-md mx-auto w-full min-h-[75vh]">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-amber-100 text-amber-700 text-2xl font-bold mb-4 shadow-xs">
          🇮🇳
        </div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">
          अपनी भाषा चुनें
        </h2>
        <p className="text-stone-600 text-base">
          Choose your preferred language to continue
        </p>
      </div>

      <div className="w-full space-y-4 mb-8">
        {/* Hindi Option */}
        <Card
          onClick={() => onSelectLanguage('hi')}
          selected={currentLanguage === 'hi'}
          className="flex items-center justify-between p-5"
        >
          <div className="flex items-center gap-3.5">
            <span className="w-10 h-10 rounded-full bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-lg">
              अ
            </span>
            <div>
              <div className="text-lg font-bold text-slate-900">हिन्दी</div>
              <div className="text-xs text-stone-500">बातचीत हिन्दी में होगी</div>
            </div>
          </div>
          <div
            className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
              currentLanguage === 'hi'
                ? 'border-amber-600 bg-amber-600 text-white'
                : 'border-stone-300'
            }`}
          >
            {currentLanguage === 'hi' && (
              <span className="w-2 h-2 rounded-full bg-white"></span>
            )}
          </div>
        </Card>

        {/* English Option */}
        <Card
          onClick={() => onSelectLanguage('en')}
          selected={currentLanguage === 'en'}
          className="flex items-center justify-between p-5"
        >
          <div className="flex items-center gap-3.5">
            <span className="w-10 h-10 rounded-full bg-slate-100 text-slate-800 flex items-center justify-center font-bold text-lg">
              A
            </span>
            <div>
              <div className="text-lg font-bold text-slate-900">English</div>
              <div className="text-xs text-stone-500">Interaction in English</div>
            </div>
          </div>
          <div
            className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
              currentLanguage === 'en'
                ? 'border-amber-600 bg-amber-600 text-white'
                : 'border-stone-300'
            }`}
          >
            {currentLanguage === 'en' && (
              <span className="w-2 h-2 rounded-full bg-white"></span>
            )}
          </div>
        </Card>
      </div>

      <Button
        variant="primary"
        fullWidth
        onClick={onContinue}
      >
        {currentLanguage === 'hi' ? 'आगे बढ़ें' : 'Continue'}
      </Button>
    </div>
  );
};

