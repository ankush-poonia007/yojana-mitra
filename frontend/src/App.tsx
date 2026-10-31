import { useState } from 'react';
import { Header } from './components/layout/Header';
import { LanguageSelectScreen } from './screens/LanguageSelectScreen';
import { WelcomeScreen } from './screens/WelcomeScreen';
import { GuidedDemoScreen } from './screens/GuidedDemoScreen';
import { ModeSelectScreen } from './screens/ModeSelectScreen';
import { ChatVoiceScreen } from './screens/ChatVoiceScreen';
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
      <main className="flex-1 flex flex-col justify-center">
        {currentScreen === 'language' && (
          <div className="px-4 py-6">
            <LanguageSelectScreen
              currentLanguage={language}
              onSelectLanguage={setLanguage}
              onContinue={() => setCurrentScreen('welcome')}
            />
          </div>
        )}

        {currentScreen === 'welcome' && (
          <div className="px-4 py-6">
            <WelcomeScreen
              language={language}
              onStartDemo={() => setCurrentScreen('demo')}
              onStartDirectly={() => setCurrentScreen('mode_select')}
              onBackToLanguage={() => setCurrentScreen('language')}
            />
          </div>
        )}

        {currentScreen === 'demo' && (
          <div className="px-4 py-6">
            <GuidedDemoScreen
              language={language}
              onFinishDemo={() => setCurrentScreen('mode_select')}
              onSkipDemo={() => setCurrentScreen('mode_select')}
              onBackToWelcome={() => setCurrentScreen('welcome')}
            />
          </div>
        )}

        {currentScreen === 'mode_select' && (
          <div className="px-4 py-6">
            <ModeSelectScreen
              language={language}
              onSelectMode={handleModeConfirmed}
              onBackToWelcome={() => setCurrentScreen('welcome')}
            />
          </div>
        )}

        {/* Phase 4: Unified Conversation Workspace (Text & Siri-Style Voice Mode) */}
        {currentScreen === 'chat' && (
          <ChatVoiceScreen
            language={language}
            initialMode={interactionMode}
            onBackToModeSelect={() => setCurrentScreen('mode_select')}
          />
        )}
      </main>

      {/* Footer (Rendered except on fullscreen chat workspace to maximize vertical space) */}
      {currentScreen !== 'chat' && (
        <footer className="py-4 border-t border-stone-200 text-center text-xs text-stone-500 bg-white">
          <p>
            {language === 'hi'
              ? 'योजना मित्र — नागरिक सहायता पहल | केवल सूचनात्मक मार्गदर्शन'
              : 'Yojana Mitra — Citizen Assistance Initiative | Indicative Guidance Only'}
          </p>
        </footer>
      )}
    </div>
  );
}

export default App;
