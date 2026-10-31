import React from 'react';
import { StandardTurnResponse } from '../types/turn';
import { LanguageCode } from '../types/session';
import { TakeAwayCard } from '../components/assessment/TakeAwayCard';

interface ResultScreenProps {
  language: LanguageCode;
  resultData: StandardTurnResponse;
  onBackToChat: () => void;
  onStartNewAssessment: () => void;
}

export const ResultScreen: React.FC<ResultScreenProps> = ({
  language,
  resultData,
  onBackToChat,
  onStartNewAssessment,
}) => {
  const isHindi = language === 'hi';
  const assessment = resultData.assessment;
  const outcome = assessment?.result || 'cannot_determine';
  const reasons = assessment?.reasons || [];
  const missingInfo = assessment?.missing_information || [];
  const sources = resultData.sources || [];

  // Configuration for outcome appearance
  const outcomeConfig = {
    likely_eligible: {
      badgeBg: 'bg-emerald-100',
      badgeBorder: 'border-emerald-300',
      badgeText: 'text-emerald-800',
      icon: '✅',
      title: isHindi ? 'संभावित रूप से पात्र (Likely Eligible)' : 'Likely Eligible',
      summary: isHindi
        ? 'आपके द्वारा दिए गए उत्तरों के आधार पर आप इस योजना की प्राथमिक शर्तों को पूरा करते प्रतीत होते हैं।'
        : 'Based on the provided responses, you appear to meet the primary criteria for this scheme.',
    },
    likely_not_eligible: {
      badgeBg: 'bg-rose-100',
      badgeBorder: 'border-rose-300',
      badgeText: 'text-rose-800',
      icon: '⚠️',
      title: isHindi ? 'संभावित रूप से अपात्र (Likely Not Eligible)' : 'Likely Not Eligible',
      summary: isHindi
        ? 'आपके द्वारा दी गई जानकारी के अनुसार आप इस योजना की कुछ अनिवार्य शर्तें पूरी नहीं करते।'
        : 'Based on the information provided, one or more disqualifying conditions apply.',
    },
    cannot_determine: {
      badgeBg: 'bg-amber-100',
      badgeBorder: 'border-amber-300',
      badgeText: 'text-amber-800',
      icon: '❓',
      title: isHindi ? 'पात्रता अनिर्धारित (Cannot Determine)' : 'Cannot Determine',
      summary: isHindi
        ? 'पर्याप्त जानकारी उपलब्ध न होने के कारण अभी आपकी पात्रता का निर्धारण नहीं किया जा सकता।'
        : 'Eligibility could not be definitively determined because essential details are missing or pending verification.',
    },
  }[outcome];

  return (
    <div className="max-w-3xl mx-auto w-full px-4 py-8 space-y-8">
      {/* Top Navigation & Actions Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-stone-200 pb-4">
        <button
          type="button"
          onClick={onBackToChat}
          className="inline-flex items-center gap-2 text-sm font-medium text-stone-700 hover:text-stone-900 bg-white border border-stone-300 px-3.5 py-2 rounded-xl hover:bg-stone-50 transition-colors shadow-2xs"
        >
          <span>←</span>
          <span>{isHindi ? 'बातचीत पर वापस जाएँ' : 'Back to Conversation'}</span>
        </button>

        <button
          type="button"
          onClick={onStartNewAssessment}
          className="inline-flex items-center gap-2 text-sm font-medium text-amber-800 hover:text-amber-900 bg-amber-50 border border-amber-200 px-3.5 py-2 rounded-xl hover:bg-amber-100 transition-colors shadow-2xs"
        >
          <span>🔄</span>
          <span>{isHindi ? 'नया मूल्यांकन शुरू करें' : 'Start New Assessment'}</span>
        </button>
      </div>

      {/* Mandatory Official Disclaimer Header Banner */}
      <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-2xl shadow-2xs">
        <div className="flex items-start gap-3">
          <span className="text-xl">ℹ️</span>
          <div className="space-y-1">
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900">
              {isHindi ? 'प्रारंभिक सूचनात्मक मार्गदर्शन' : 'Indicative Guidance Notice'}
            </h4>
            <p className="text-xs text-amber-800 leading-relaxed">
              {isHindi
                ? 'यह परिणाम आपके द्वारा दी गई जानकारी और उपलब्ध आधिकारिक नियमों के आधार पर एक स्वचालित प्रारंभिक मूल्यांकन है। यह आधिकारिक सरकारी स्वीकृति या अस्वीकृति नहीं है। अंतिम निर्णय संबंधित सरकारी एजेंसी अथवा अधिकृत वितरक द्वारा मूल दस्तावेज़ सत्यापन के पश्चात ही मान्य होगा।'
                : 'This result is an automated indicative assessment based on your answers and published rules. It does NOT constitute official government approval or disqualification. The final decision rests entirely with the competent government authority or authorized distributor upon physical verification of documents.'}
            </p>
          </div>
        </div>
      </div>

      {/* Main Outcome Card */}
      <div className="bg-white border border-stone-200 rounded-3xl p-6 sm:p-8 shadow-xs space-y-6">
        {/* Outcome Header Badge */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="text-xs font-semibold uppercase tracking-wider text-stone-500">
              {isHindi ? 'मूल्यांकन परिणाम' : 'Assessment Result'}
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-stone-900 flex items-center gap-2.5">
              <span>{outcomeConfig.icon}</span>
              <span>{outcomeConfig.title}</span>
            </h2>
          </div>

          <div
            className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border text-xs font-bold uppercase tracking-wider self-start sm:self-center ${outcomeConfig.badgeBg} ${outcomeConfig.badgeBorder} ${outcomeConfig.badgeText}`}
          >
            <span>{outcome}</span>
          </div>
        </div>

        {/* Outcome Overview Summary */}
        <p className="text-stone-600 text-sm leading-relaxed">{outcomeConfig.summary}</p>

        {/* Narrative Answer Text (from backend) */}
        {resultData.answer?.text && (
          <div className="bg-stone-50 border border-stone-200 rounded-2xl p-4 text-sm text-stone-800 leading-relaxed">
            <span className="font-semibold block text-xs text-stone-500 mb-1">
              {isHindi ? 'विस्तृत उत्तर (Assistant Explanation):' : 'Detailed Explanation:'}
            </span>
            "{resultData.answer.text}"
          </div>
        )}

        {/* Evaluated Reasons Section */}
        <div className="space-y-3 pt-2">
          <h3 className="text-sm font-bold text-stone-900 flex items-center gap-2">
            <span>🔍</span>
            <span>{isHindi ? 'मूल्यांकन के मुख्य कारण व नियम' : 'Evaluation Reasons & Decision Factors'}</span>
          </h3>
          {reasons.length > 0 ? (
            <ul className="space-y-2">
              {reasons.map((reason, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-2 text-sm text-stone-700 bg-stone-50/70 p-3 rounded-xl border border-stone-100"
                >
                  <span className="text-stone-400 font-bold">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs italic text-stone-500 bg-stone-50 p-3 rounded-xl border border-stone-100">
              {isHindi
                ? 'कोई विशिष्ट कारण विवरण संलग्न नहीं है।'
                : 'No specific deterministic decision factors were attached.'}
            </p>
          )}
        </div>

        {/* Missing / Pending Information Section */}
        {missingInfo.length > 0 && (
          <div className="space-y-3 pt-2 border-t border-stone-100">
            <h3 className="text-sm font-bold text-amber-900 flex items-center gap-2">
              <span>❓</span>
              <span>{isHindi ? 'अपूर्ण या आवश्यक छूटी हुई जानकारी' : 'Missing Information Requiring Clarification'}</span>
            </h3>
            <div className="bg-amber-50/60 border border-amber-200 rounded-2xl p-4 space-y-2">
              <p className="text-xs text-amber-900">
                {isHindi
                  ? 'निम्नलिखित बिंदुओं की पुष्टि न होने के कारण अंतिम पात्रता निर्धारित नहीं हो पाई:'
                  : 'Eligibility could not be fully resolved due to the following pending inputs:'}
              </p>
              <ul className="space-y-1.5 pl-2">
                {missingInfo.map((field, idx) => (
                  <li key={idx} className="text-xs text-amber-800 flex items-center gap-2 font-mono">
                    <span className="text-amber-500">▶</span>
                    <span>{field}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Step 3: Take-Away Action Card */}
      <div className="space-y-3">
        <div className="text-xs font-bold uppercase tracking-wider text-stone-500 px-1">
          {isHindi ? 'नागरिक संदर्भ कार्ड' : 'Citizen Action & Guidance'}
        </div>
        <TakeAwayCard card={resultData.card} language={language} />
      </div>

      {/* Official Sources & Evidence Provenance */}
      <div className="bg-white border border-stone-200 rounded-3xl p-6 sm:p-8 shadow-xs space-y-4">
        <div className="space-y-1">
          <h3 className="text-sm font-bold text-stone-900 flex items-center gap-2">
            <span>📚</span>
            <span>{isHindi ? 'सत्यापित आधिकारिक स्रोत संदर्भ' : 'Verified Official Source References'}</span>
          </h3>
          <p className="text-xs text-stone-500">
            {isHindi
              ? 'यह जानकारी केवल सरकारी नियमों और आधिकारिक मार्गदर्शिकाओं से ली गई है।'
              : 'All factual criteria are strictly grounded in official guidelines and documentation.'}
          </p>
        </div>

        {sources.length > 0 ? (
          <div className="space-y-3">
            {sources.map((src, idx) => (
              <div
                key={idx}
                className="bg-stone-50 border border-stone-200 rounded-xl p-4 text-xs space-y-1.5 hover:border-stone-300 transition-colors"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="font-semibold text-stone-800 text-sm">{src.title}</span>
                  <span className="text-[10px] bg-stone-200 text-stone-700 px-2 py-0.5 rounded font-mono">
                    {src.document_id}
                  </span>
                </div>

                <div className="flex flex-wrap gap-x-4 gap-y-1 text-stone-500">
                  {src.page !== undefined && <span>{isHindi ? `पृष्ठ: ${src.page}` : `Page: ${src.page}`}</span>}
                  {src.section && <span>{isHindi ? `अनुभाग: ${src.section}` : `Section: ${src.section}`}</span>}
                </div>

                {src.url && (
                  <div className="pt-1">
                    <a
                      href={src.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-amber-700 hover:text-amber-900 hover:underline break-all inline-flex items-center gap-1"
                    >
                      <span>🔗</span>
                      <span>{src.url}</span>
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-stone-50 border border-stone-200 rounded-xl p-4 text-xs text-stone-500 italic">
            {isHindi
              ? 'इस प्रतिक्रिया के लिए कोई आधिकारिक स्रोत संदर्भ संलग्न नहीं है।'
              : 'No official source citations attached to this assessment response.'}
          </div>
        )}
      </div>

      {/* Footer Navigation Back Button */}
      <div className="pt-4 text-center">
        <button
          type="button"
          onClick={onBackToChat}
          className="text-sm text-stone-600 hover:text-stone-900 underline font-medium"
        >
          {isHindi ? '← वापस बातचीत पर जाएँ' : '← Return to conversation'}
        </button>
      </div>
    </div>
  );
};
