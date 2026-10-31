import React from 'react';
import { TakeAwayCard as TakeAwayCardType } from '../../types/assessment';
import { LanguageCode } from '../../types/session';

interface TakeAwayCardProps {
  card: TakeAwayCardType | null;
  language: LanguageCode;
}

export const TakeAwayCard: React.FC<TakeAwayCardProps> = ({ card, language }) => {
  const isHindi = language === 'hi';

  if (!card) {
    return (
      <div className="bg-stone-50 border border-dashed border-stone-300 rounded-2xl p-6 text-center text-stone-500 text-sm">
        <span className="text-xl block mb-2">📋</span>
        <p className="font-medium text-stone-700">
          {isHindi ? 'कार्यवाही कार्ड उपलब्ध नहीं है' : 'Action Card Unavailable'}
        </p>
        <p className="text-xs text-stone-500 mt-1">
          {isHindi
            ? 'इस मूल्यांकन के लिए कोई औपचारिक दस्तावेज़ या आवेदन विवरण संलग्न नहीं है।'
            : 'No formal documents or application guidance attached to this assessment.'}
        </p>
      </div>
    );
  }

  const hasDocuments = card.documents && card.documents.length > 0;
  const hasWhereToApply = card.where_to_apply && card.where_to_apply.length > 0;

  return (
    <div className="bg-white border-2 border-stone-200 rounded-2xl shadow-sm p-6 space-y-6 text-stone-900 print:border print:shadow-none">
      {/* Card Header */}
      <div className="border-b border-stone-200 pb-4">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-700">
          <span>📋</span>
          <span>{isHindi ? 'नागरिक कार्यवाही कार्ड (Take-Away Card)' : 'Citizen Take-Away Action Card'}</span>
        </div>
        <h3 className="text-xl font-bold text-stone-900 mt-1">
          {card.scheme_name || (isHindi ? 'योजना का नाम अनुपलब्ध' : 'Scheme Name Unavailable')}
        </h3>
      </div>

      {/* Required Documents Section */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-800 flex items-center gap-2">
          <span>📁</span>
          <span>{isHindi ? 'आवश्यक दस्तावेज़' : 'Required Documents'}</span>
        </h4>
        {hasDocuments ? (
          <ul className="space-y-2">
            {card.documents.map((doc, idx) => (
              <li
                key={idx}
                className="flex items-start gap-2.5 text-sm bg-stone-50 p-2.5 rounded-xl border border-stone-100"
              >
                <span className="text-emerald-600 font-bold">✓</span>
                <span className="text-stone-700">{doc}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs italic text-stone-500 bg-stone-50 p-3 rounded-xl border border-stone-100">
            {isHindi
              ? 'दस्तावेज़ों की सूची आधिकारिक स्रोत से सत्यापित नहीं हुई है।'
              : 'Document requirements have not yet been verified from official sources.'}
          </p>
        )}
      </div>

      {/* Where to Apply Section */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-800 flex items-center gap-2">
          <span>📍</span>
          <span>{isHindi ? 'आवेदन कहाँ करें (Next Steps)' : 'Where to Apply (Next Steps)'}</span>
        </h4>
        {hasWhereToApply ? (
          <ul className="space-y-2">
            {card.where_to_apply.map((place, idx) => (
              <li
                key={idx}
                className="flex items-start gap-2.5 text-sm bg-stone-50 p-2.5 rounded-xl border border-stone-100"
              >
                <span className="text-amber-600 font-bold">→</span>
                <span className="text-stone-700">{place}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs italic text-stone-500 bg-stone-50 p-3 rounded-xl border border-stone-100">
            {isHindi
              ? 'आवेदन केंद्र की जानकारी अभी उपलब्ध नहीं है।'
              : 'Application locations have not yet been verified from official sources.'}
          </p>
        )}
      </div>

      {/* Card Disclaimer Banner */}
      {card.disclaimer ? (
        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3 text-xs text-amber-900 leading-relaxed">
          <span className="font-semibold">{isHindi ? 'घोषणा: ' : 'Notice: '}</span>
          {card.disclaimer}
        </div>
      ) : (
        <div className="bg-stone-50 border border-stone-200 rounded-xl p-3 text-xs text-stone-600 leading-relaxed">
          <span className="font-semibold">{isHindi ? 'सूचना: ' : 'Notice: '}</span>
          {isHindi
            ? 'यह केवल सूचनात्मक मार्गदर्शन है, आधिकारिक सरकारी स्वीकृति नहीं।'
            : 'This guidance is indicative only and does not constitute official government approval.'}
        </div>
      )}
    </div>
  );
};
