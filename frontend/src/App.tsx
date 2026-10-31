import { useState } from 'react';
import { Header } from './components/layout/Header';
import { LanguageSelectScreen } from './screens/LanguageSelectScreen';
import { WelcomeScreen } from './screens/WelcomeScreen';
import { ScreenName } from './types/navigation';
import { LanguageCode } from './types/session';

export function App() {
  const [currentScreen, setCurrentScreen] = useState<ScreenName>('language');
  const [language, setLanguage] = useState<LanguageCode>('hi');

  const handleReset = () => {
    setCurrentScreen('welcome');
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
            onStartDemo={() => {
              // Stub transition for Phase 1
              alert(
                language === 'hi'
                  ? 'अभ्यास डेमो (Guided Demo) चरण 3 में उपलब्ध होगा।'
                  : 'Guided Demo will be available in Phase 3.'
              );
            }}
            onStartDirectly={() => {
              // Stub transition for Phase 1
              alert(
                language === 'hi'
                  ? 'बातचीत स्क्रीन (Chat/Voice) चरण 4 में उपलब्ध होगी।'
                  : 'Chat/Voice screen will be available in Phase 4.'
              );
            }}
            onBackToLanguage={() => setCurrentScreen('language')}
          />
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

