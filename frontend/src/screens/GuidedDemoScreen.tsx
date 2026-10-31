import React, { useState, useEffect, useRef } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { LanguageCode } from '../types/session';
import { MOCK_DEMO_STEPS, MOCK_SAMPLE_CARD } from '../mocks/mockDemoData';

interface GuidedDemoScreenProps {
  language: LanguageCode;
  onFinishDemo: () => void;
  onSkipDemo: () => void;
  onBackToWelcome: () => void;
}

// Minimal type declaration for Web Speech API SpeechRecognition
interface IWindowSpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onresult: ((event: unknown) => void) | null;
  onerror: ((event: unknown) => void) | null;
  onend: (() => void) | null;
}

export const GuidedDemoScreen: React.FC<GuidedDemoScreenProps> = ({
  language,
  onFinishDemo,
  onSkipDemo,
  onBackToWelcome,
}) => {
  const isHindi = language === 'hi';

  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const currentStep = MOCK_DEMO_STEPS[currentStepIndex];
  const isLastStep = currentStepIndex === MOCK_DEMO_STEPS.length - 1;

  // Interaction State for Step 1 & Step 2
  const [inputText, setInputText] = useState<string>(currentStep.defaultPrompt[language]);
  const [submittedQuery, setSubmittedQuery] = useState<string | null>(null);
  const [isListening, setIsListening] = useState<boolean>(false);
  const [speechError, setSpeechError] = useState<string | null>(null);
  const [isSpeechRecognitionSupported, setIsSpeechRecognitionSupported] = useState<boolean>(true);

  // Audio Playback State for SpeechSynthesis
  const [isPlayingAudio, setIsPlayingAudio] = useState<boolean>(false);
  const [synthesisError, setSynthesisError] = useState<string | null>(null);

  // Recognition and Synthesis instance references
  const recognitionRef = useRef<IWindowSpeechRecognition | null>(null);
  const isMountedRef = useRef<boolean>(true);

  // Update default prompt when language or step changes
  useEffect(() => {
    setInputText(MOCK_DEMO_STEPS[currentStepIndex].defaultPrompt[language]);
    setSubmittedQuery(null);
    setSpeechError(null);
    setSynthesisError(null);
  }, [currentStepIndex, language]);

  // Check speech recognition support and clean up on unmount
  useEffect(() => {
    isMountedRef.current = true;
    const SpeechRecognitionConstructor =
      (window as unknown as { SpeechRecognition?: new () => IWindowSpeechRecognition }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: new () => IWindowSpeechRecognition }).webkitSpeechRecognition;

    if (!SpeechRecognitionConstructor) {
      setIsSpeechRecognitionSupported(false);
    }

    return () => {
      isMountedRef.current = false;
      // Abort any active recognition session
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // Ignore abort errors on cleanup
        }
        recognitionRef.current = null;
      }
      // Cancel any active speech synthesis
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // Handler: Start browser microphone speech recognition
  const handleStartListening = () => {
    setSpeechError(null);

    const SpeechRecognitionConstructor =
      (window as unknown as { SpeechRecognition?: new () => IWindowSpeechRecognition }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: new () => IWindowSpeechRecognition }).webkitSpeechRecognition;

    if (!SpeechRecognitionConstructor) {
      setSpeechError(
        isHindi
          ? 'आपके ब्राउज़र में बोलकर पहचानने की सुविधा उपलब्ध नहीं है। कृपया नीचे लिखकर पूछें।'
          : 'Speech recognition is not supported in your browser. Please type below.'
      );
      return;
    }

    // Stop active synthesis before speaking
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
    }

    // Clean up previous instance if any
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {
        // Safe catch
      }
    }

    try {
      const recognition = new SpeechRecognitionConstructor();
      recognitionRef.current = recognition;
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = isHindi ? 'hi-IN' : 'en-IN';

      recognition.onresult = (event: unknown) => {
        if (!isMountedRef.current) return;
        const speechEvent = event as { results: { 0: { 0: { transcript: string } } } };
        const transcript = speechEvent.results?.[0]?.[0]?.transcript;
        if (transcript && transcript.trim().length > 0) {
          setInputText(transcript.trim());
          setSpeechError(null);
        } else {
          setSpeechError(
            isHindi
              ? 'आवाज़ समझ नहीं आई। कृपया दोबारा बोलें या नीचे लिखें।'
              : 'Speech could not be understood. Please speak again or type.'
          );
        }
      };

      recognition.onerror = (event: unknown) => {
        if (!isMountedRef.current) return;
        const errEvent = event as { error?: string };
        setIsListening(false);
        if (errEvent.error === 'not-allowed') {
          setSpeechError(
            isHindi
              ? 'माइक्रोफ़ोन की अनुमति अस्वीकृत हुई। कृपया ब्राउज़र में अनुमति दें या लिखकर अभ्यास करें।'
              : 'Microphone permission denied. Please allow mic access or use text input.'
          );
        } else if (errEvent.error === 'no-speech') {
          setSpeechError(
            isHindi
              ? 'कोई आवाज़ सुनाई नहीं दी। कृपया माइक बटन दबाकर बोलें या लिखें।'
              : 'No speech was detected. Please tap mic and speak again, or type.'
          );
        } else {
          setSpeechError(
            isHindi
              ? 'पहचान में त्रुटि हुई। आप सीधे लिखकर भी आगे बढ़ सकते हैं।'
              : 'Speech recognition error. You can also type directly.'
          );
        }
      };

      recognition.onend = () => {
        if (isMountedRef.current) {
          setIsListening(false);
        }
      };

      recognition.start();
      setIsListening(true);
    } catch {
      setIsListening(false);
      setSpeechError(
        isHindi
          ? 'माइक्रोफ़ोन शुरू करने में समस्या आई। कृपया लिखकर अभ्यास करें।'
          : 'Could not access microphone. Please type below.'
      );
    }
  };

  // Handler: Stop speech recognition
  const handleStopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // Safe catch
      }
      setIsListening(false);
    }
  };

  // Handler: Submit User Query (from voice or typed input)
  const handleSubmitQuery = () => {
    if (!inputText.trim()) {
      setSpeechError(
        isHindi ? 'कृपया पहले कुछ बोलें या लिखें।' : 'Please speak or type a question first.'
      );
      return;
    }
    setSubmittedQuery(inputText.trim());
    setSpeechError(null);
  };

  // Handler: Speech Synthesis - Listen
  const handleSpeakAssistantReply = () => {
    setSynthesisError(null);

    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setSynthesisError(
        isHindi
          ? 'आपके ब्राउज़र में बोलकर सुनाने (Speech Synthesis) की सुविधा उपलब्ध नहीं है।'
          : 'Speech synthesis is not supported in this browser.'
      );
      return;
    }

    // Cancel any ongoing audio to prevent collisions
    window.speechSynthesis.cancel();

    try {
      const textToSpeak = currentStep.assistantReply[language];
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.lang = isHindi ? 'hi-IN' : 'en-IN';

      // Select voice if available
      const voices = window.speechSynthesis.getVoices();
      const targetLang = isHindi ? 'hi' : 'en';
      const matchedVoice = voices.find((v) => v.lang.toLowerCase().startsWith(targetLang));
      if (matchedVoice) {
        utterance.voice = matchedVoice;
      }

      utterance.onstart = () => {
        if (isMountedRef.current) {
          setIsPlayingAudio(true);
        }
      };

      utterance.onend = () => {
        if (isMountedRef.current) {
          setIsPlayingAudio(false);
        }
      };

      utterance.onerror = () => {
        if (isMountedRef.current) {
          setIsPlayingAudio(false);
          setSynthesisError(
            isHindi
              ? 'आवाज़ सुनाने में समस्या आई। आप उत्तर स्क्रीन पर पढ़ सकते हैं।'
              : 'Audio synthesis failed. You can read the reply on screen.'
          );
        }
      };

      window.speechSynthesis.speak(utterance);
    } catch {
      setIsPlayingAudio(false);
      setSynthesisError(
        isHindi
          ? 'आवाज़ चलाने में त्रुटि हुई।'
          : 'Failed to initiate audio synthesis.'
      );
    }
  };

  // Handler: Stop Audio Playback
  const handleStopAudio = () => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
    }
  };

  // Navigation Handlers
  const handleNext = () => {
    // Clean audio on transition
    handleStopAudio();
    handleStopListening();

    if (isLastStep) {
      onFinishDemo();
    } else {
      setCurrentStepIndex((prev) => prev + 1);
    }
  };

  const handleReplay = () => {
    handleStopAudio();
    handleStopListening();
    setCurrentStepIndex(0);
  };

  const handleSkip = () => {
    handleStopAudio();
    handleStopListening();
    onSkipDemo();
  };

  const handleBack = () => {
    handleStopAudio();
    handleStopListening();
    onBackToWelcome();
  };

  return (
    <div className="py-4 px-4 max-w-xl mx-auto w-full space-y-4">
      {/* Honest Demo Disclosure Banner */}
      <div className="bg-amber-100/95 border border-amber-300 text-amber-950 px-3.5 py-2.5 rounded-xl text-xs flex items-center justify-between gap-2 shadow-xs">
        <div className="flex items-center gap-2">
          <span className="text-base" aria-hidden="true">ℹ️</span>
          <span className="font-medium">
            {isHindi
              ? 'यह अभ्यास ट्यूटोरियल है। यहाँ वास्तविक माइक व ऑडियो का अभ्यास करें (कोई वास्तविक सरकारी निर्णय नहीं)।'
              : 'This is a practice tutorial with real mic and voice controls (no real government decisions).'}
          </span>
        </div>
        <button
          type="button"
          onClick={handleSkip}
          className="text-xs font-bold text-amber-900 underline whitespace-nowrap hover:text-amber-950 cursor-pointer"
        >
          {isHindi ? 'छोड़ें (Skip)' : 'Skip Tutorial'}
        </button>
      </div>

      {/* Step Header */}
      <div className="flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
            {currentStep.badge[language]}
          </span>
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 mt-1.5">
            {currentStep.title[language]}
          </h2>
        </div>
        <div className="text-xs font-medium text-stone-500">
          {isHindi
            ? `कदम ${currentStepIndex + 1} / ${MOCK_DEMO_STEPS.length}`
            : `Step ${currentStepIndex + 1} of ${MOCK_DEMO_STEPS.length}`}
        </div>
      </div>

      {/* Instruction Card */}
      <Card className="bg-white border-stone-200 p-4">
        <p className="text-sm text-stone-700 leading-relaxed">
          {currentStep.instruction[language]}
        </p>
      </Card>

      {/* Interactive Conversation Simulator Container */}
      <div className="bg-stone-100 border border-stone-300 rounded-2xl p-4 space-y-4 shadow-inner">
        {/* User Query Bubble (Rendered when submitted or active) */}
        <div className="flex justify-end">
          <div className="bg-emerald-600 text-white rounded-2xl rounded-tr-xs px-4 py-2.5 text-sm max-w-[90%] shadow-xs">
            <div className="text-[10px] text-emerald-100 font-medium mb-0.5">
              {isHindi ? 'आप (अभ्यास प्रश्न)' : 'You (Practice Query)'}
            </div>
            {submittedQuery || inputText}
          </div>
        </div>

        {/* Assistant Response Bubble (Rendered with audio controls) */}
        <div className="flex justify-start">
          <div className="bg-white border border-stone-200 text-stone-900 rounded-2xl rounded-tl-xs px-4 py-3 text-sm max-w-[90%] shadow-xs space-y-2.5 w-full">
            <div className="text-[10px] text-amber-700 font-semibold mb-0.5 flex items-center justify-between">
              <span className="flex items-center gap-1">
                <span aria-hidden="true">🤖</span>
                <span>{isHindi ? 'योजना मित्र सहायक (नमूना उत्तर)' : 'Assistant (Sample Reply)'}</span>
              </span>
              <span className="text-[10px] bg-amber-50 text-amber-800 px-1.5 py-0.5 rounded border border-amber-200">
                {isHindi ? 'स्क्रिप्टेड अभ्यास' : 'Scripted Demo'}
              </span>
            </div>

            <p className="text-sm leading-relaxed text-stone-800">
              {currentStep.assistantReply[language]}
            </p>

            {/* Audio Synthesis Playback Controls */}
            <div className="pt-2 border-t border-stone-100 flex flex-wrap items-center justify-between gap-2 text-xs">
              <div className="flex items-center gap-2">
                {!isPlayingAudio ? (
                  <button
                    type="button"
                    onClick={handleSpeakAssistantReply}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-600 text-white hover:bg-amber-700 font-medium transition-colors shadow-xs cursor-pointer min-h-[36px]"
                    aria-label={isHindi ? 'उत्तर बोलकर सुनें' : 'Listen to response'}
                  >
                    <span aria-hidden="true">🔊</span>
                    <span>{isHindi ? 'बोलकर सुनें (Listen)' : 'Listen'}</span>
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={handleStopAudio}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-600 text-white hover:bg-red-700 font-medium transition-colors shadow-xs cursor-pointer min-h-[36px] animate-pulse"
                    aria-label={isHindi ? 'ऑडियो रोकें' : 'Stop audio'}
                  >
                    <span aria-hidden="true">⏹</span>
                    <span>{isHindi ? 'रोकें (Stop)' : 'Stop'}</span>
                  </button>
                )}

                <button
                  type="button"
                  onClick={handleSpeakAssistantReply}
                  className="px-2.5 py-1.5 rounded-lg border border-stone-300 text-stone-600 hover:bg-stone-50 text-xs transition-colors cursor-pointer"
                  title={isHindi ? 'पुनः सुनें' : 'Replay'}
                >
                  {isHindi ? 'पुनः सुनें (Replay)' : 'Replay'}
                </button>
              </div>

              {isPlayingAudio && (
                <span className="text-xs text-amber-700 font-medium flex items-center gap-1">
                  <span className="inline-block w-2 h-2 rounded-full bg-amber-500 animate-ping"></span>
                  {isHindi ? 'ऑडियो चल रहा है...' : 'Speaking...'}
                </span>
              )}
            </div>

            {/* Synthesis Error Notice */}
            {synthesisError && (
              <div className="text-[11px] text-red-700 bg-red-50 p-2 rounded-lg border border-red-200">
                {synthesisError}
              </div>
            )}
          </div>
        </div>

        {/* Step 3 Sample Card Display */}
        {currentStepIndex === 2 && (
          <div className="bg-white border-2 border-amber-300 rounded-xl p-4 text-xs text-stone-800 shadow-sm space-y-2.5">
            <div className="font-bold text-slate-900 text-sm border-b border-stone-100 pb-1.5 flex items-center justify-between">
              <span>{MOCK_SAMPLE_CARD.schemeName[language]}</span>
              <span className="text-[10px] text-amber-800 bg-amber-100 px-2 py-0.5 rounded-full font-semibold">
                {isHindi ? 'नमूना कार्ड' : 'Sample Card'}
              </span>
            </div>
            <div>
              <span className="font-semibold text-stone-700">
                {isHindi ? 'ले जाने योग्य दस्तावेज़:' : 'Documents to Carry:'}
              </span>
              <ul className="list-disc list-inside mt-1 space-y-0.5 text-stone-600">
                {MOCK_SAMPLE_CARD.documents[language].map((doc, idx) => (
                  <li key={idx}>{doc}</li>
                ))}
              </ul>
            </div>
            <div>
              <span className="font-semibold text-stone-700">
                {isHindi ? 'कहाँ आवेदन करें:' : 'Where to Apply:'}
              </span>
              <ul className="list-disc list-inside mt-1 space-y-0.5 text-stone-600">
                {MOCK_SAMPLE_CARD.whereToApply[language].map((place, idx) => (
                  <li key={idx}>{place}</li>
                ))}
              </ul>
            </div>
            <div className="text-[11px] text-amber-900 bg-amber-50 p-2.5 rounded-lg border border-amber-200 leading-relaxed">
              ⚠️ {MOCK_SAMPLE_CARD.disclaimer[language]}
            </div>
          </div>
        )}

        {/* Microphone and Text Input Interaction Area */}
        <div className="bg-white rounded-xl p-3 border border-stone-200 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-800">
              {isHindi ? 'अभ्यास इनपुट (बोलें या लिखें):' : 'Practice Input (Speak or Type):'}
            </span>
            {isListening && (
              <span className="text-xs text-amber-600 font-semibold flex items-center gap-1 animate-pulse">
                <span className="w-2 h-2 rounded-full bg-amber-600"></span>
                {isHindi ? 'सुन रहा है... बोलिए' : 'Listening... Speak now'}
              </span>
            )}
          </div>

          {/* Action Row: Real Mic Button + Text Field */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
            {!isListening ? (
              <button
                type="button"
                onClick={handleStartListening}
                className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-amber-600 text-white font-semibold text-xs hover:bg-amber-700 active:scale-95 transition-all shadow-xs cursor-pointer min-h-[44px]"
                aria-label={isHindi ? 'माइक से अभ्यास करें' : 'Practice with microphone'}
              >
                <span className="text-base" aria-hidden="true">🎙️</span>
                <span>{isHindi ? 'माइक से बोलें' : 'Speak via Mic'}</span>
              </button>
            ) : (
              <button
                type="button"
                onClick={handleStopListening}
                className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-red-600 text-white font-semibold text-xs hover:bg-red-700 active:scale-95 transition-all shadow-xs cursor-pointer min-h-[44px] animate-pulse"
                aria-label={isHindi ? 'माइक बंद करें' : 'Stop microphone'}
              >
                <span className="text-base" aria-hidden="true">⏹</span>
                <span>{isHindi ? 'माइक रोकें' : 'Stop Listening'}</span>
              </button>
            )}

            {/* Editable / Review Input Field */}
            <div className="flex-1 flex items-center gap-1.5">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  isHindi ? 'यहाँ प्रश्न बोलें या लिखें...' : 'Speak or type query here...'
                }
                className="flex-1 px-3 py-2 text-xs border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 bg-stone-50 min-h-[44px]"
                aria-label={isHindi ? 'प्रश्न इनपुट' : 'Query input text'}
              />
              <button
                type="button"
                onClick={handleSubmitQuery}
                className="px-3.5 py-2 bg-slate-900 text-white rounded-lg text-xs font-semibold hover:bg-slate-800 transition-colors shadow-xs cursor-pointer min-h-[44px] whitespace-nowrap"
              >
                {isHindi ? 'भेजें' : 'Send'}
              </button>
            </div>
          </div>

          {/* Speech Error Notice */}
          {speechError && (
            <div className="text-[11px] text-amber-900 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
              {speechError}
            </div>
          )}

          {!isSpeechRecognitionSupported && (
            <div className="text-[11px] text-stone-600 bg-stone-100 p-2 rounded-lg">
              ℹ️ {isHindi
                ? 'इस ब्राउज़र में लाइव माइक स्पीच रिकग्निशन समर्थित नहीं है। आप सीधे टेक्स्ट बॉक्स में लिखकर अभ्यास कर सकते हैं।'
                : 'Speech recognition is not natively supported in this browser. You can type in the box above.'}
            </div>
          )}
        </div>
      </div>

      {/* Screen Action Bar */}
      <div className="flex flex-col sm:flex-row items-center gap-2.5 pt-2">
        <Button
          variant="primary"
          fullWidth
          onClick={handleNext}
        >
          {isLastStep
            ? isHindi
              ? 'ट्यूटोरियल पूर्ण करें और माध्यम चुनें →'
              : 'Complete Tutorial & Choose Mode →'
            : isHindi
            ? 'अगला कदम देखें →'
            : 'Next Step →'}
        </Button>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          {currentStepIndex > 0 && (
            <Button
              variant="outline"
              className="flex-1 sm:flex-initial text-xs"
              onClick={handleReplay}
            >
              {isHindi ? 'शुरुआत से देखें (Replay)' : 'Replay'}
            </Button>
          )}
          <Button
            variant="outline"
            className="flex-1 sm:flex-initial text-xs"
            onClick={handleBack}
          >
            {isHindi ? 'वापस (Back)' : 'Back'}
          </Button>
        </div>
      </div>
    </div>
  );
};
