import React from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { LanguageCode, InteractionMode } from '../types/session';

interface ModeSelectScreenProps {
  language: LanguageCode;
  onSelectMode: (mode: InteractionMode) => void;
  onBackToWelcome: () => void;
}

export const ModeSelectScreen: React.FC<ModeSelectScreenProps> = ({
  language,
  onSelectMode,
  onBackToWelcome,
}) => {
  const isHindi = language === 'hi';

  return (
    <div className="py-6 px-4 max-w-md mx-auto w-full space-y-6">
      <div className="text-center pt-2">
        <span className="inline-block px-3 py-1 bg-amber-100 text-amber-800 text-xs font-semibold rounded-full mb-3">
          {isHindi ? 'बातचीत का माध्यम चुनें' : 'Choose Interaction Mode'}
        </span>
        <h2 className="text-2xl font-bold text-slate-900 leading-snug">
          {isHindi
            ? 'आप कैसे बातचीत शुरू करना चाहते हैं?'
            : 'How would you like to start?'}
        </h2>
        <p className="mt-2 text-stone-600 text-sm">
          {isHindi
            ? 'आप बातचीत के दौरान कभी भी बोलकर या लिखकर पूछने का माध्यम बदल सकते हैं।'
            : 'You can switch between voice and text anytime during the conversation.'}
        </p>
      </div>

      <div className="space-y-4">
        {/* Voice Option Card */}
        <Card
          onClick={() => onSelectMode('voice')}
          className="flex items-center gap-4 p-5 hover:border-amber-600 cursor-pointer group"
        >
          <div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-700 flex items-center justify-center text-2xl group-hover:scale-105 transition-transform">
            🎙️
          </div>
          <div className="flex-1">
            <div className="text-base font-bold text-slate-900 flex items-center justify-between">
              <span>{isHindi ? 'बोलकर बातचीत करें' : 'Voice-first'}</span>
              <span className="text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                {isHindi ? 'अनुशंसित' : 'Recommended'}
              </span>
            </div>
            <p className="text-xs text-stone-500 mt-1">
              {isHindi
                ? 'माइक से अपनी भाषा में बोलें और उत्तर सुनें'
                : 'Speak in your language and listen to answers'}
            </p>
          </div>
        </Card>

        {/* Text Option Card */}
        <Card
          onClick={() => onSelectMode('text')}
          className="flex items-center gap-4 p-5 hover:border-slate-800 cursor-pointer group"
        >
          <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center text-2xl group-hover:scale-105 transition-transform">
            ⌨️
          </div>
          <div className="flex-1">
            <div className="text-base font-bold text-slate-900">
              {isHindi ? 'लिखकर बातचीत करें' : 'Text-first'}
            </div>
            <p className="text-xs text-stone-500 mt-1">
              {isHindi
                ? 'कीबोर्ड से टाइप करें और स्क्रीन पर पढ़ें'
                : 'Type messages and read responses on screen'}
            </p>
          </div>
        </Card>
      </div>

      <div className="pt-2 text-center">
        <Button
          variant="outline"
          fullWidth
          onClick={onBackToWelcome}
        >
          {isHindi ? '← मुख्य पृष्ठ पर लौटें' : '← Back to Welcome'}
        </Button>
      </div>
    </div>
  );
};

