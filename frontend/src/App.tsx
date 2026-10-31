import { useState } from 'react';
import { Header } from './components/layout/Header';
import { LanguageSelectScreen } from './screens/LanguageSelectScreen';
import { WelcomeScreen } from './screens/WelcomeScreen';
import { GuidedDemoScreen } from './screens/GuidedDemoScreen';
import { ModeSelectScreen } from './screens/ModeSelectScreen';
import { ScreenName } from './types/navigation';
import { LanguageCode, InteractionMode } from './types/session';

export function App() {
  const [currentScreen, setCurrentScreen] = useState<ScreenName>('language');
  const [language, setLanguage] = useState<LanguageCode>('hi');
  const [interactionMode, setInteractionMode] = useState<InteractionMode>('voice');

  const handleReset = () => {
    setCurrentScreen('welcome');
  };

  const handleModeConfirmed = (mode: InteractionMode) => {
    setInteractionMode(mode);
    // Explicit Phase 4 boundary handoff
    setCurrentScreen('chat');
  };

  return (
    <div className="min-h-screen flex flex-col bg-stone-50 text-stone-900">
      {/* Shell Header */}
      <Header
        language={language}
        onLanguageChange={setLanguage}
        onReset={handleReset}
        showReset={currentScreen !== 'language'}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 flex flex-col justify-center px-4 py-6">
        {currentScreen === 'language' && (
          <LanguageSelectScreen
            currentLanguage={language}
            onSelectLanguage={setLanguage}
            onContinue={() => setCurrentScreen('welcome')}
          />
        )}

        {currentScreen === 'welcome' && (
          <WelcomeScreen
            language={language}
            onStartDemo={() => setCurrentScreen('demo')}
            onStartDirectly={() => setCurrentScreen('mode_select')}
            onBackToLanguage={() => setCurrentScreen('language')}
          />
        )}

        {currentScreen === 'demo' && (
          <GuidedDemoScreen
            language={language}
            onFinishDemo={() => setCurrentScreen('mode_select')}
            onSkipDemo={() => setCurrentScreen('mode_select')}
            onBackToWelcome={() => setCurrentScreen('welcome')}
          />
        )}

        {currentScreen === 'mode_select' && (
          <ModeSelectScreen
            language={language}
            onSelectMode={handleModeConfirmed}
            onBackToWelcome={() => setCurrentScreen('welcome')}
          />
        )}

        {/* Phase 4 Boundary Handoff Placeholder */}
        {currentScreen === 'chat' && (
          <div className="max-w-md mx-auto text-center py-10 px-4 space-y-4 bg-white rounded-2xl border border-stone-200 shadow-xs">
            <div className="text-4xl">💬</div>
            <h3 className="text-xl font-bold text-slate-900">
              {language === 'hi'
                ? 'ऑनबोर्डिंग पूर्ण! बातचीत स्क्रीन (Phase 4)'
                : 'Onboarding Complete! Conversation Screen (Phase 4)'}
            </h3>
            <p className="text-sm text-stone-600">
              {language === 'hi'
                ? `चुनी गई भाषा: ${language === 'hi' ? 'हिन्दी' : 'English'} | माध्यम: ${
                    interactionMode === 'voice' ? 'आवाज़ (Voice)' : 'लिखकर (Text)'
                  }`
                : `Language: ${language} | Mode: ${interactionMode}`}
            </p>
            <div className="text-xs text-amber-800 bg-amber-50 p-3 rounded-xl border border-amber-200">
              {language === 'hi'
                ? 'Phase 4 में लाइव चैट और वॉइस इंटरैक्शन स्क्रीन जोड़ी जाएगी।'
                : 'The unified ChatVoiceScreen will be implemented in Phase 4.'}
            </div>
            <button
              type="button"
              onClick={() => setCurrentScreen('mode_select')}
              className="text-xs text-stone-500 hover:text-stone-800 underline transition-colors"
            >
              {language === 'hi' ? '← माध्यम पुनः चुनें' : '← Re-select Mode'}
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="py-4 border-t border-stone-200 text-center text-xs text-stone-500 bg-white">
        <p>
          {language === 'hi'
            ? 'योजना मित्र — नागरिक सहायता पहल | केवल सूचनात्मक मार्गदर्शन'
            : 'Yojana Mitra — Citizen Assistance Initiative | Indicative Guidance Only'}
        </p>
      </footer>
    </div>
  );
}

export default App;
