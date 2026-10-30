import React from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { LanguageCode } from '../types/session';

interface WelcomeScreenProps {
  language: LanguageCode;
  onStartDemo: () => void;
  onStartDirectly: () => void;
  onBackToLanguage: () => void;
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({
  language,
  onStartDemo,
  onStartDirectly,
  onBackToLanguage,
}) => {
  const isHindi = language === 'hi';

  return (
    <div className="py-6 px-4 max-w-xl mx-auto w-full space-y-6">
      {/* Hero Welcome Card */}
      <div className="text-center pt-2 pb-4">
        <span className="inline-block px-3 py-1 bg-amber-100 text-amber-800 text-xs font-semibold rounded-full mb-3">
          {isHindi ? 'प्रधानमंत्री उज्ज्वला योजना (PMUY) सहायता' : 'PM Ujjwala Yojana (PMUY) Support'}
        </span>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-snug">
          {isHindi
            ? 'सरकारी योजनाओं की सही जानकारी, अपनी आवाज़ में'
            : 'Find Government Schemes in Your Own Voice'}
        </h2>
        <p className="mt-2 text-stone-600 text-sm sm:text-base">
          {isHindi
            ? 'सरल बातचीत के ज़रिए जानें कि क्या आप पात्र हैं और कौन-से दस्तावेज़ आवश्यक हैं।'
            : 'Check indicative eligibility and required documents through a simple conversation.'}
        </p>
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card className="text-center p-4">
          <div className="text-2xl mb-1.5">🎙️</div>
          <div className="font-semibold text-slate-900 text-sm">
            {isHindi ? 'बोलकर पूछें' : 'Speak or Type'}
          </div>
          <div className="text-xs text-stone-500 mt-1">
            {isHindi ? 'टाइप करने की ज़रूरत नहीं' : 'No complex typing needed'}
          </div>
        </Card>

        <Card className="text-center p-4">
          <div className="text-2xl mb-1.5">📄</div>
          <div className="font-semibold text-slate-900 text-sm">
            {isHindi ? 'दस्तावेज़ सूची' : 'Document List'}
          </div>
          <div className="text-xs text-stone-500 mt-1">
            {isHindi ? 'ले जाने योग्य स्पष्ट कार्ड' : 'Take-away action card'}
          </div>
        </Card>

        <Card className="text-center p-4">
          <div className="text-2xl mb-1.5">🏛️</div>
          <div className="font-semibold text-slate-900 text-sm">
            {isHindi ? 'सरकारी स्रोत' : 'Official Sources'}
          </div>
          <div className="text-xs text-stone-500 mt-1">
            {isHindi ? 'प्रमाणित दिशानिर्देश' : 'Verified official rules'}
          </div>
        </Card>
      </div>

      {/* Indicative Disclaimer Alert */}
      <div className="border-l-4 border-amber-500 bg-amber-50 p-4 rounded-r-xl text-xs text-amber-900">
        <div className="font-bold flex items-center gap-1.5 mb-1">
          <span>⚠️</span>
          <span>{isHindi ? 'महत्वपूर्ण सूचना' : 'Important Notice'}</span>
        </div>
        <p>
          {isHindi
            ? 'यह केवल प्रारंभिक पात्रता जानकारी और मार्गदर्शन है, आधिकारिक स्वीकृति नहीं। अंतिम पुष्टि संबंधित विभाग या LPG वितरक द्वारा होगी।'
            : 'This is indicative guidance only, not an official decision. Final verification is conducted by the relevant department or distributor.'}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="space-y-3 pt-2">
        <Button
          variant="secondary"
          fullWidth
          onClick={onStartDemo}
          className="flex items-center justify-center gap-2"
        >
          <span>🎯</span>
          <span>{isHindi ? 'अभ्यास डेमो देखें (Guided Demo)' : 'Try Guided Demo (Practice)'}</span>
        </Button>

        <Button
          variant="primary"
          fullWidth
          onClick={onStartDirectly}
          className="flex items-center justify-center gap-2"
        >
          <span>💬</span>
          <span>{isHindi ? 'सीधे बातचीत शुरू करें' : 'Start Assistant Directly'}</span>
        </Button>

        <div className="text-center pt-2">
          <button
            type="button"
            onClick={onBackToLanguage}
            className="text-xs text-stone-500 hover:text-stone-800 underline transition-colors"
          >
            {isHindi ? '← भाषा बदलें (Change Language)' : '← Change Language'}
          </button>
        </div>
      </div>
    </div>
  );
};

