import { useState } from 'react';
import { Header } from './components/layout/Header';
import { LanguageSelectScreen } from './screens/LanguageSelectScreen';
import { WelcomeScreen } from './screens/WelcomeScreen';
import { GuidedDemoScreen } from './screens/GuidedDemoScreen';
import { ModeSelectScreen } from './screens/ModeSelectScreen';
import { ChatVoiceScreen } from './screens/ChatVoiceScreen';
import { ResultScreen } from './screens/ResultScreen';
import { ScreenName } from './types/navigation';
import { LanguageCode, InteractionMode } from './types/session';
import { StandardTurnResponse } from './types/turn';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  isSpoken?: boolean;
  assessmentResult?: StandardTurnResponse | null;
}

export function App() {
  const [currentScreen, setCurrentScreen] = useState<ScreenName>('language');
  const [language, setLanguage] = useState<LanguageCode>('hi');
  const [interactionMode, setInteractionMode] = useState<InteractionMode>('voice');

  // Lifted conversation & assessment state to preserve history across navigation
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'msg-welcome',
      role: 'assistant',
      text:
        language === 'hi'
          ? 'नमस्ते! मैं योजना मित्र हूँ। मैं प्रधानमंत्री उज्ज्वला योजना (PMUY) की पात्रता और ज़रूरी दस्तावेज़ समझने में आपकी मदद कर सकता हूँ। आप क्या जानना चाहते हैं?'
          : 'Hello! I am Yojana Mitra. I can help you understand eligibility and required documents for Pradhan Mantri Ujjwala Yojana (PMUY). What would you like to know?',
    },
  ]);

  const [activeAssessmentResult, setActiveAssessmentResult] = useState<StandardTurnResponse | null>(null);

  // When user changes language at top shell level, update initial greeting if only 1 message
  const handleLanguageChange = (newLang: LanguageCode) => {
    setLanguage(newLang);
    setMessages((prev) => {
      if (prev.length <= 1) {
        return [
          {
            id: 'msg-welcome',
            role: 'assistant',
            text:
              newLang === 'hi'
                ? 'नमस्ते! मैं योजना मित्र हूँ। मैं प्रधानमंत्री उज्ज्वला योजना (PMUY) की पात्रता और ज़रूरी दस्तावेज़ समझने में आपकी मदद कर सकता हूँ। आप क्या जानना चाहते हैं?'
                : 'Hello! I am Yojana Mitra. I can help you understand eligibility and required documents for Pradhan Mantri Ujjwala Yojana (PMUY). What would you like to know?',
          },
        ];
      }
      return prev;
    });
  };

  const handleReset = () => {
    setCurrentScreen('welcome');
  };

  const handleStartNewAssessment = () => {
    // Reset conversation and assessment state only, preserving user's chosen language
    setMessages([
      {
        id: `msg-welcome-${Date.now()}`,
        role: 'assistant',
        text:
          language === 'hi'
            ? 'नमस्ते! मैं योजना मित्र हूँ। मैं प्रधानमंत्री उज्ज्वला योजना (PMUY) की पात्रता और ज़रूरी दस्तावेज़ समझने में आपकी मदद कर सकता हूँ। आप क्या जानना चाहते हैं?'
            : 'Hello! I am Yojana Mitra. I can help you understand eligibility and required documents for Pradhan Mantri Ujjwala Yojana (PMUY). What would you like to know?',
      },
    ]);
    setActiveAssessmentResult(null);
    setCurrentScreen('chat');
  };

  const handleModeConfirmed = (mode: InteractionMode) => {
    setInteractionMode(mode);
    setCurrentScreen('chat');
  };

  const handleViewResult = (result: StandardTurnResponse) => {
    setActiveAssessmentResult(result);
    setCurrentScreen('result');
  };

  return (
    <div className="min-h-screen flex flex-col bg-stone-50 text-stone-900">
      {/* Shell Header */}
      <Header
        language={language}
        onLanguageChange={handleLanguageChange}
        onReset={handleReset}
        showReset={currentScreen !== 'language'}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 flex flex-col justify-center">
        {currentScreen === 'language' && (
          <div className="px-4 py-6">
            <LanguageSelectScreen
              currentLanguage={language}
              onSelectLanguage={handleLanguageChange}
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

        {/* Phase 4 & Phase 5: Unified Conversation Workspace */}
        {currentScreen === 'chat' && (
          <ChatVoiceScreen
            language={language}
            initialMode={interactionMode}
            onBackToModeSelect={() => setCurrentScreen('mode_select')}
            onViewResult={handleViewResult}
            messages={messages}
            setMessages={setMessages}
            activeAssessmentResult={activeAssessmentResult}
            setActiveAssessmentResult={setActiveAssessmentResult}
          />
        )}

        {/* Phase 5: Assessment Result Screen & Citizen Take-Away Card */}
        {currentScreen === 'result' && activeAssessmentResult && (
          <div className="px-4 py-6">
            <ResultScreen
              language={language}
              resultData={activeAssessmentResult}
              onBackToChat={() => setCurrentScreen('chat')}
              onStartNewAssessment={handleStartNewAssessment}
            />
          </div>
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
