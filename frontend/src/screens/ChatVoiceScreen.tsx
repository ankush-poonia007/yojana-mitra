import React, { useState, useEffect, useRef } from 'react';
import { ChatBubble } from '../components/chat/ChatBubble';
import { ChatInput } from '../components/chat/ChatInput';
import { TypingIndicator } from '../components/chat/TypingIndicator';
import { LanguageCode, InteractionMode } from '../types/session';
import { StandardTurnResponse } from '../types/turn';
import {
  mockEligibleResponse,
  mockEligibleResponseEn,
  mockNotEligibleResponse,
  mockNotEligibleResponseEn,
  mockCannotDetermineResponse,
  mockCannotDetermineResponseEn,
} from '../mocks/mockResults';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  isSpoken?: boolean;
  assessmentResult?: StandardTurnResponse | null;
}

interface ChatVoiceScreenProps {
  language: LanguageCode;
  initialMode: InteractionMode;
  onBackToModeSelect: () => void;
  onViewResult: (result: StandardTurnResponse) => void;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  activeAssessmentResult: StandardTurnResponse | null;
  setActiveAssessmentResult: React.Dispatch<React.SetStateAction<StandardTurnResponse | null>>;
}

// Minimal Web Speech Recognition Interface
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

export const ChatVoiceScreen: React.FC<ChatVoiceScreenProps> = ({
  language,
  initialMode,
  onBackToModeSelect,
  onViewResult,
  messages,
  setMessages,
  activeAssessmentResult,
  setActiveAssessmentResult,
}) => {
  const isHindi = language === 'hi';

  // Mode state: 'text' or 'voice'
  const [mode, setMode] = useState<InteractionMode>(initialMode);

  // Input & loading states for Text Mode
  const [inputText, setInputText] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);

  // Voice Mode States: 'idle' | 'listening' | 'processing' | 'speaking' | 'error'
  const [voiceState, setVoiceState] = useState<
    'idle' | 'listening' | 'processing' | 'speaking' | 'error'
  >('idle');
  const [voiceTranscript, setVoiceTranscript] = useState<string>('');
  const [voiceErrorMessage, setVoiceErrorMessage] = useState<string | null>(null);

  // References
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<IWindowSpeechRecognition | null>(null);
  const isMountedRef = useRef<boolean>(true);

  // Auto-scroll to bottom of message list in Text Mode
  useEffect(() => {
    if (mode === 'text') {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping, mode]);

  // Clean up recognition and synthesis on unmount
  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // ignore
        }
        recognitionRef.current = null;
      }
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // When switching modes, cancel any active voice sessions
  const handleSwitchMode = (newMode: InteractionMode) => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {
        // ignore
      }
    }
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setVoiceState('idle');
    setVoiceErrorMessage(null);
    setMode(newMode);
  };

  // Predefined deterministic mock replies for informational questions
  const getMockReply = (userQuery: string): string => {
    const query = userQuery.toLowerCase();
    if (query.includes('पात्र') || query.includes('eligible') || query.includes('eligibility')) {
      return isHindi
        ? 'प्रधानमंत्री उज्ज्वला योजना (PMUY 2.0) के लिए मुख्य शर्तें हैं: 1. आवेदक 18 वर्ष से अधिक उम्र की महिला होनी चाहिए। 2. परिवार में पहले से कोई LPG कनेक्शन नहीं होना चाहिए। 3. गरीब परिवार (SECC / BPL / 14 सूत्री घोषणा) से होना चाहिए। क्या आपके परिवार में पहले से कोई गैस कनेक्शन है?'
        : 'Key eligibility criteria for PM Ujjwala Yojana (PMUY 2.0): 1. Applicant must be a woman aged 18 or above. 2. No existing LPG connection in the household. 3. Belongs to a poor household. Does your household already have an LPG connection?';
    }
    if (query.includes('दस्तावेज़') || query.includes('document') || query.includes('paper')) {
      return isHindi
        ? 'आवेदन के लिए ये दस्तावेज़ आवश्यक हैं: 1. आधार कार्ड (पहचान व पते का प्रमाण) 2. राशन कार्ड (परिवार संरचना प्रमाण) 3. बैंक खाता संख्या और IFSC 4. 14 सूत्री घोषणा पत्र। क्या आपके पास ये दस्तावेज़ तैयार हैं?'
        : 'Required documents for application: 1. Aadhaar Card (identity/address proof) 2. Ration Card (family composition proof) 3. Bank Account Number & IFSC 4. 14-point declaration. Do you have these documents ready?';
    }
    if (query.includes('कहाँ') || query.includes('apply') || query.includes('आवेदन') || query.includes('csc')) {
      return isHindi
        ? 'आप अपने निकटतम LPG वितरक (इंडेन, भारत गैस, या एचपी गैस) के पास जाकर या अपने ग्राम पंचायत के कॉमन सर्विस सेंटर (CSC) पर आवेदन कर सकते हैं। वितरक से रसीद लेना न भूलें।'
        : 'You can apply at your nearest LPG distributor (Indane, Bharat Gas, HP Gas) or at your Gram Panchayat Common Service Centre (CSC). Always remember to collect an acknowledgement receipt.';
    }
    return isHindi
      ? 'धन्यवाद। उज्ज्वला योजना में महिलाओं को मुफ्त गैस कनेक्शन, पहला भरा हुआ सिलेंडर और चूल्हा दिया जाता है। क्या आप पात्रता नियम या दस्तावेज़ सूची जानना चाहते हैं?'
      : 'Thank you. Under Ujjwala Yojana, eligible women receive a deposit-free LPG connection, first refill, and stove. Would you like to check eligibility criteria or the document list?';
  };

  // Text Mode Submit Handler (Informational turn)
  const handleSendTextMessage = () => {
    const textToSend = inputText.trim();
    if (!textToSend || isTyping) return;

    // Append user message
    const userMsg: Message = {
      id: `usr-${Date.now()}`,
      role: 'user',
      text: textToSend,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setIsTyping(true);

    // Simulate mock latency (500ms)
    setTimeout(() => {
      if (!isMountedRef.current) return;
      const replyText = getMockReply(textToSend);
      const assistantMsg: Message = {
        id: `ast-${Date.now()}`,
        role: 'assistant',
        text: replyText,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsTyping(false);
    }, 500);
  };

  // Test / Dev Control: Inject one of the 3 frozen assessment mock outcomes
  const handleInjectSampleOutcome = (outcomeType: 'eligible' | 'not_eligible' | 'cannot_determine') => {
    let mockResult: StandardTurnResponse;
    if (outcomeType === 'eligible') {
      mockResult = isHindi ? mockEligibleResponse : mockEligibleResponseEn;
    } else if (outcomeType === 'not_eligible') {
      mockResult = isHindi ? mockNotEligibleResponse : mockNotEligibleResponseEn;
    } else {
      mockResult = isHindi ? mockCannotDetermineResponse : mockCannotDetermineResponseEn;
    }

    setActiveAssessmentResult(mockResult);

    const userSimulatedPrompt: Message = {
      id: `usr-test-${Date.now()}`,
      role: 'user',
      text:
        outcomeType === 'eligible'
          ? isHindi
            ? '[परीक्षण इनपुट] मैं 18+ महिला हूँ, कोई LPG नहीं है।'
            : '[Test Input] I am an 18+ woman, no LPG connection in household.'
          : outcomeType === 'not_eligible'
          ? isHindi
            ? '[परीक्षण इनपुट] मेरे घर में पहले से गैस कनेक्शन है।'
            : '[Test Input] We already have an active gas cylinder connection.'
          : isHindi
          ? '[परीक्षण इनपुट] अभी स्पष्ट नहीं है कि परिवार में गैस कनेक्शन है या नहीं।'
          : '[Test Input] Unclear whether our household already has an LPG connection.',
    };

    const assistantAssessmentReply: Message = {
      id: `ast-test-${Date.now()}`,
      role: 'assistant',
      text: mockResult.answer.text,
      assessmentResult: mockResult,
    };

    setMessages((prev) => [...prev, userSimulatedPrompt, assistantAssessmentReply]);
  };

  // Suggested questions in empty/initial state
  const suggestedQueries = isHindi
    ? [
        'उज्ज्वला योजना के पात्रता नियम क्या हैं?',
        'आवेदन के लिए कौन-से दस्तावेज़ चाहिए?',
        'कहाँ जाकर आवेदन करना होगा?',
      ]
    : [
        'What are the eligibility criteria for PMUY?',
        'What documents are needed to apply?',
        'Where can I submit the application?',
      ];

  // ==========================================
  // VOICE MODE (Siri-Style Floating Circle)
  // ==========================================

  const handleStartVoiceListening = () => {
    setVoiceErrorMessage(null);
    setVoiceTranscript('');

    const SpeechRecognitionConstructor =
      (window as unknown as { SpeechRecognition?: new () => IWindowSpeechRecognition }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition?: new () => IWindowSpeechRecognition }).webkitSpeechRecognition;

    if (!SpeechRecognitionConstructor) {
      setVoiceState('error');
      setVoiceErrorMessage(
        isHindi
          ? 'आपके ब्राउज़र में स्पीच रिकग्निशन उपलब्ध नहीं है। कृपया नीचे "टेक्स्ट मोड" का उपयोग करें।'
          : 'Speech recognition is not supported in this browser. Please switch to Text Mode.'
      );
      return;
    }

    // Cancel speech synthesis if speaking
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {
        // ignore
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
          const cleanTranscript = transcript.trim();
          setVoiceTranscript(cleanTranscript);
          setVoiceState('processing');

          // Add user message to shared conversation
          const userMsg: Message = {
            id: `usr-${Date.now()}`,
            role: 'user',
            text: cleanTranscript,
            isSpoken: true,
          };
          setMessages((prev) => [...prev, userMsg]);

          // Prepare assistant mock reply
          setTimeout(() => {
            if (!isMountedRef.current) return;
            const reply = getMockReply(cleanTranscript);
            const assistantMsg: Message = {
              id: `ast-${Date.now()}`,
              role: 'assistant',
              text: reply,
            };
            setMessages((prev) => [...prev, assistantMsg]);
            speakAssistantReply(reply);
          }, 600);
        } else {
          setVoiceState('idle');
        }
      };

      recognition.onerror = (event: unknown) => {
        if (!isMountedRef.current) return;
        const errEvent = event as { error?: string };
        const errCode = errEvent.error;

        if (errCode === 'no-speech') {
          setVoiceState('idle');
          return;
        }

        setVoiceState('error');
        setVoiceErrorMessage(
          errCode === 'not-allowed'
            ? isHindi
              ? 'माइक्रोफ़ोन की अनुमति अस्वीकृत है। कृपया ब्राउज़र सेटिंग्स में अनुमति दें।'
              : 'Microphone permission denied. Please allow microphone access.'
            : isHindi
            ? 'आवाज़ पहचानने में समस्या आई। पुनः प्रयास करें या लिखकर पूछें।'
            : 'Error recognizing speech. Try again or switch to text mode.'
        );
      };

      recognition.onend = () => {
        if (isMountedRef.current && voiceState === 'listening') {
          setVoiceState('idle');
        }
      };

      setVoiceState('listening');
      recognition.start();
    } catch {
      setVoiceState('error');
      setVoiceErrorMessage(
        isHindi
          ? 'माइक्रोफ़ोन प्रारंभ नहीं हो सका।'
          : 'Could not start microphone.'
      );
    }
  };

  const handleStopVoiceListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // ignore
      }
      setVoiceState('idle');
    }
  };

  const speakAssistantReply = (textToSpeak: string) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setVoiceState('idle');
      return;
    }

    window.speechSynthesis.cancel();

    try {
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.lang = isHindi ? 'hi-IN' : 'en-IN';

      const voices = window.speechSynthesis.getVoices();
      const targetLang = isHindi ? 'hi' : 'en';
      const matchedVoice = voices.find((v) => v.lang.toLowerCase().startsWith(targetLang));
      if (matchedVoice) {
        utterance.voice = matchedVoice;
      }

      utterance.onstart = () => {
        if (isMountedRef.current) {
          setVoiceState('speaking');
        }
      };

      utterance.onend = () => {
        if (isMountedRef.current) {
          setVoiceState('idle');
        }
      };

      utterance.onerror = () => {
        if (isMountedRef.current) {
          setVoiceState('idle');
        }
      };

      window.speechSynthesis.speak(utterance);
    } catch {
      setVoiceState('idle');
    }
  };

  const handleStopSpeaking = () => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setVoiceState('idle');
    }
  };

  // Get the latest assistant message for Voice Mode caption
  const latestAssistantMessage = [...messages].reverse().find((m) => m.role === 'assistant');

  return (
    <div className="flex flex-col flex-1 h-[calc(100vh-64px)] max-h-[calc(100vh-64px)] overflow-hidden bg-stone-50">
      {/* Mode Switcher Top Bar */}
      <div className="bg-white border-b border-stone-200 px-4 py-2.5 flex items-center justify-between shadow-2xs shrink-0">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onBackToModeSelect}
            className="text-xs text-stone-500 hover:text-stone-900 transition-colors p-1"
            title={isHindi ? 'माध्यम चयन पर वापस' : 'Back to mode selection'}
          >
            ←
          </button>
          <span className="text-xs font-semibold text-slate-800">
            {isHindi ? 'योजना मित्र सहायक' : 'Yojana Mitra Assistant'}
          </span>
        </div>

        {/* View Active Assessment Result Button (Visible when assessment data exists) */}
        {activeAssessmentResult && (
          <button
            type="button"
            onClick={() => onViewResult(activeAssessmentResult)}
            className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded-full text-xs font-semibold shadow-xs transition-colors cursor-pointer"
          >
            <span>📊</span>
            <span>{isHindi ? 'परिणाम देखें' : 'View Result'}</span>
          </button>
        )}

        {/* Toggle Pills: Text vs Voice */}
        <div className="inline-flex rounded-full bg-stone-100 p-0.5 border border-stone-200">
          <button
            type="button"
            onClick={() => handleSwitchMode('text')}
            className={`px-3 py-1 text-xs font-semibold rounded-full transition-all flex items-center gap-1.5 ${
              mode === 'text'
                ? 'bg-slate-900 text-white shadow-xs'
                : 'text-stone-600 hover:text-stone-900'
            }`}
          >
            <span>⌨️</span>
            <span>{isHindi ? 'लिखकर (Text)' : 'Text'}</span>
          </button>
          <button
            type="button"
            onClick={() => handleSwitchMode('voice')}
            className={`px-3 py-1 text-xs font-semibold rounded-full transition-all flex items-center gap-1.5 ${
              mode === 'voice'
                ? 'bg-amber-600 text-white shadow-xs'
                : 'text-stone-600 hover:text-stone-900'
            }`}
          >
            <span>🎙️</span>
            <span>{isHindi ? 'बोलकर (Voice)' : 'Voice'}</span>
          </button>
        </div>
      </div>

      {/* Dev / Test Scenarios Bar (Clearly labeled MOCK / TEST DATA) */}
      <div className="bg-amber-50/90 border-b border-amber-200 px-4 py-1.5 flex flex-wrap items-center justify-between gap-2 text-[11px] shrink-0">
        <div className="flex items-center gap-1.5 font-bold text-amber-900 uppercase tracking-wider">
          <span className="bg-amber-200 text-amber-900 px-1.5 py-0.5 rounded text-[10px]">MOCK / TEST DATA</span>
          <span>{isHindi ? 'परिणाम सिमुलेशन:' : 'Simulate Outcome:'}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            onClick={() => handleInjectSampleOutcome('eligible')}
            className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 hover:bg-emerald-200 font-semibold border border-emerald-300 transition-colors"
          >
            ✅ {isHindi ? 'पात्र' : 'Eligible'}
          </button>
          <button
            type="button"
            onClick={() => handleInjectSampleOutcome('not_eligible')}
            className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 hover:bg-rose-200 font-semibold border border-rose-300 transition-colors"
          >
            ⚠️ {isHindi ? 'अपात्र' : 'Not Eligible'}
          </button>
          <button
            type="button"
            onClick={() => handleInjectSampleOutcome('cannot_determine')}
            className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 hover:bg-amber-200 font-semibold border border-amber-300 transition-colors"
          >
            ❓ {isHindi ? 'अनिर्धारित' : 'Cannot Determine'}
          </button>
        </div>
      </div>

      {/* ========================================================
          MODE 1: TEXT MODE (Classic Responsive Chat Interface)
          ======================================================== */}
      {mode === 'text' && (
        <div className="flex-1 flex flex-col h-full overflow-hidden">
          {/* Scrollable Message Feed */}
          <div className="flex-1 overflow-y-auto px-4 py-4 max-w-3xl mx-auto w-full space-y-1">
            {messages.map((msg) => (
              <ChatBubble
                key={msg.id}
                role={msg.role}
                text={msg.text}
                transcriptionTag={msg.isSpoken}
                language={language}
                assessmentResult={msg.assessmentResult}
                onViewResult={onViewResult}
              />
            ))}

            {isTyping && <TypingIndicator language={language} />}

            {/* Suggested Queries Chips (Rendered below initial welcome) */}
            {messages.length === 1 && !isTyping && (
              <div className="pt-3 pb-2">
                <div className="text-xs font-semibold text-stone-500 mb-2">
                  {isHindi ? '💡 सुझाव:' : '💡 Suggestions:'}
                </div>
                <div className="flex flex-wrap gap-2">
                  {suggestQueriesChips(suggestedQueries, (chip) => {
                    setInputText(chip);
                  })}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Bottom Docked Input */}
          <div className="shrink-0">
            <ChatInput
              value={inputText}
              onChange={setInputText}
              onSend={handleSendTextMessage}
              disabled={isTyping}
              language={language}
            />
          </div>
        </div>
      )}

      {/* ========================================================
          MODE 2: VOICE MODE (Siri-Style Floating Circle Interface)
          ======================================================== */}
      {mode === 'voice' && (
        <div className="flex-1 flex flex-col items-center justify-between p-6 sm:p-8 max-w-xl mx-auto w-full select-none">
          {/* Top Status & Context Prompt */}
          <div className="text-center w-full pt-2">
            <span className="inline-block px-3 py-1 bg-amber-100 text-amber-900 text-xs font-semibold rounded-full mb-3 border border-amber-200">
              {isHindi ? 'आवाज़ मोड (Voice Assistant)' : 'Voice Mode'}
            </span>
            <div className="text-xs text-stone-400">
              {voiceState === 'idle' && (isHindi ? 'शुरू करने के लिए गोले पर टैप करें' : 'Tap orb to start speaking')}
              {voiceState === 'listening' && (isHindi ? 'माइक सुन रहा है... बोलिए' : 'Listening... Speak now')}
              {voiceState === 'processing' && (isHindi ? 'समझ रहा है...' : 'Processing your query...')}
              {voiceState === 'speaking' && (isHindi ? 'सहायक बोल रहा है...' : 'Assistant is speaking...')}
              {voiceState === 'error' && (isHindi ? 'त्रुटि हुई' : 'Voice interaction error')}
            </div>
          </div>

          {/* Pulsing Siri-Style Interactive Orb */}
          <div className="my-auto flex flex-col items-center justify-center relative">
            {/* Ambient Background Glow Layer */}
            <div
              className={`absolute w-64 h-64 rounded-full filter blur-2xl opacity-40 transition-all duration-700 pointer-events-none ${
                voiceState === 'listening'
                  ? 'bg-rose-400 scale-125'
                  : voiceState === 'processing'
                  ? 'bg-amber-400 scale-110'
                  : voiceState === 'speaking'
                  ? 'bg-emerald-400 scale-135'
                  : 'bg-stone-300 scale-90'
              }`}
            />

            {/* Ripple Pulse Rings (Active when listening or speaking) */}
            {(voiceState === 'listening' || voiceState === 'speaking') && (
              <>
                <div
                  className={`absolute w-48 h-48 rounded-full border-2 border-current animate-ping opacity-25 pointer-events-none ${
                    voiceState === 'listening' ? 'text-rose-500' : 'text-emerald-500'
                  }`}
                />
                <div
                  className={`absolute w-56 h-56 rounded-full border border-current animate-pulse opacity-20 pointer-events-none ${
                    voiceState === 'listening' ? 'text-rose-400' : 'text-emerald-400'
                  }`}
                />
              </>
            )}

            {/* Main Interactive Button Orb */}
            <button
              type="button"
              onClick={() => {
                if (voiceState === 'listening') {
                  handleStopVoiceListening();
                } else if (voiceState === 'speaking') {
                  handleStopSpeaking();
                } else {
                  handleStartVoiceListening();
                }
              }}
              aria-label={
                voiceState === 'listening'
                  ? isHindi
                    ? 'सुनना बंद करें'
                    : 'Stop listening'
                  : voiceState === 'speaking'
                  ? isHindi
                    ? 'आवाज़ रोकें'
                    : 'Stop speaking'
                  : isHindi
                  ? 'बोलना शुरू करें'
                  : 'Start speaking'
              }
              className={`relative z-10 w-36 h-36 rounded-full flex flex-col items-center justify-center shadow-2xl transition-all duration-300 active:scale-95 cursor-pointer ${
                voiceState === 'listening'
                  ? 'bg-gradient-to-tr from-rose-500 to-amber-500 scale-110 ring-4 ring-rose-200'
                  : voiceState === 'processing'
                  ? 'bg-gradient-to-tr from-amber-400 to-amber-600 animate-spin ring-4 ring-amber-200'
                  : voiceState === 'speaking'
                  ? 'bg-gradient-to-tr from-emerald-500 to-teal-600 scale-105 ring-4 ring-emerald-200'
                  : 'bg-gradient-to-tr from-stone-800 to-stone-900 hover:scale-105 ring-4 ring-stone-200'
              }`}
            >
              <span className="text-3xl text-white">
                {voiceState === 'listening' ? '🛑' : voiceState === 'speaking' ? '🔊' : '🎙️'}
              </span>
              <span className="text-[10px] text-white/90 font-medium mt-1 uppercase tracking-wider">
                {voiceState === 'listening'
                  ? isHindi
                    ? 'रोकें'
                    : 'Stop'
                  : voiceState === 'speaking'
                  ? isHindi
                    ? 'सुनें'
                    : 'Playing'
                  : isHindi
                  ? 'टैप करें'
                  : 'Tap'}
              </span>
            </button>
          </div>

          {/* Transcript & Assistant Response Display Panel */}
          <div className="w-full space-y-3 pb-4">
            {/* Live Recognized User Transcript */}
            {voiceTranscript && (
              <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 px-4 py-2.5 rounded-xl text-xs text-center shadow-2xs">
                <span className="font-semibold block text-[10px] text-emerald-700 uppercase">
                  {isHindi ? 'आपकी बात (Recognized):' : 'You said:'}
                </span>
                "{voiceTranscript}"
              </div>
            )}

            {/* Latest Assistant Speech / Response Caption */}
            {latestAssistantMessage && (
              <div className="bg-white border border-stone-200 text-stone-900 p-4 rounded-2xl shadow-xs text-sm text-center leading-relaxed">
                <div className="text-[10px] text-amber-700 font-semibold mb-1 flex items-center justify-center gap-1">
                  <span>🤖</span>
                  <span>{isHindi ? 'योजना मित्र उत्तर (Assistant Reply):' : 'Yojana Mitra Reply:'}</span>
                </div>
                <p className="line-clamp-4">{latestAssistantMessage.text}</p>
                {voiceState === 'idle' && (
                  <button
                    type="button"
                    onClick={() => speakAssistantReply(latestAssistantMessage.text)}
                    className="mt-2 inline-flex items-center gap-1 text-xs text-amber-700 hover:text-amber-900 font-medium underline"
                  >
                    <span>🔊</span>
                    <span>{isHindi ? 'दोबारा सुनें' : 'Listen again'}</span>
                  </button>
                )}
              </div>
            )}

            {/* Error Banner */}
            {voiceErrorMessage && (
              <div className="bg-red-50 border border-red-200 text-red-800 p-3 rounded-xl text-xs text-center space-y-1.5">
                <p>⚠️ {voiceErrorMessage}</p>
                <button
                  type="button"
                  onClick={() => handleSwitchMode('text')}
                  className="font-bold underline text-red-900 hover:text-red-950 block mx-auto text-xs"
                >
                  {isHindi ? 'टेक्स्ट मोड में लिखकर पूछें' : 'Switch to Text Mode instead'}
                </button>
              </div>
            )}

            {/* Switch to Text Mode Footer Link */}
            <div className="text-center pt-1">
              <button
                type="button"
                onClick={() => handleSwitchMode('text')}
                className="text-xs text-stone-500 hover:text-stone-800 underline transition-colors"
              >
                {isHindi ? '⌨️ कीबोर्ड से लिखकर पूछना चाहते हैं? (Text Mode)' : '⌨️ Prefer to type? Switch to Text Mode'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper for rendering suggestion chips
function suggestQueriesChips(chips: string[], onSelect: (chip: string) => void) {
  return chips.map((chip, idx) => (
    <button
      key={idx}
      type="button"
      onClick={() => onSelect(chip)}
      className="text-xs bg-white text-stone-700 hover:text-slate-900 hover:border-amber-500 border border-stone-200 px-3 py-1.5 rounded-full transition-colors text-left shadow-2xs cursor-pointer active:scale-95"
    >
      {chip}
    </button>
  ));
}
