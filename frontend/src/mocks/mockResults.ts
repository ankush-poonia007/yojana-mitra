import { StandardTurnResponse } from '../types/turn';

/**
 * Scenario 1: Likely Eligible (PMUY 2.0 Qualifying Applicant)
 * Direct match with shared/examples/turn_completed_response.json
 */
export const mockEligibleResponse: StandardTurnResponse = {
  session_id: 'sess_demo_001',
  turn_id: 'turn_010',
  status: 'completed',
  language: 'hi',
  answer: {
    text: 'आपके दिए गए उत्तरों के आधार पर आप संभवतः पात्र हैं। अंतिम पुष्टि LPG वितरक द्वारा होगी।',
  },
  assessment: {
    scheme_id: 'pmuy',
    result: 'likely_eligible',
    reasons: [
      'आवेदक महिला है और उसकी उम्र 18 वर्ष या अधिक है।',
      'परिवार के पास पहले से LPG कनेक्शन नहीं है।',
    ],
    missing_information: [],
  },
  card: {
    scheme_name: 'प्रधानमंत्री उज्ज्वला योजना',
    documents: [
      'आधार कार्ड',
      'राशन कार्ड या परिवार संरचना का प्रमाण',
      'बैंक पासबुक',
    ],
    where_to_apply: [
      'LPG वितरक',
      'Common Service Centre',
    ],
    disclaimer: 'यह केवल प्रारंभिक पात्रता जानकारी है, आधिकारिक स्वीकृति नहीं।',
  },
  sources: [
    {
      document_id: 'pmuy_official_001',
      title: 'PMUY Official Guidelines',
      url: 'https://example.gov.in/official-document',
      page: 4,
    },
  ],
  speech: {
    status: 'generated',
    content_type: 'audio/mpeg',
    audio_base64: 'DEMO_AUDIO_DATA',
  },
};

/**
 * Scenario 2: Likely Not Eligible (Disqualifying Criterion Met: Has Active LPG)
 * Evaluated strictly by deterministic backend rules in real pipeline.
 */
export const mockNotEligibleResponse: StandardTurnResponse = {
  session_id: 'sess_demo_002',
  turn_id: 'turn_011',
  status: 'completed',
  language: 'hi',
  answer: {
    text: 'आपके परिवार में पहले से LPG कनेक्शन होने के कारण आप वर्तमान में प्रधानमंत्री उज्ज्वला योजना के तहत नए कनेक्शन के लिए संभवतः अपात्र हैं।',
  },
  assessment: {
    scheme_id: 'pmuy',
    result: 'likely_not_eligible',
    reasons: [
      'परिवार के किसी भी सदस्य के नाम पर पहले से LPG कनेक्शन मौजूद नहीं होना चाहिए।',
    ],
    missing_information: [],
  },
  card: {
    scheme_name: 'प्रधानमंत्री उज्ज्वला योजना',
    documents: [
      'राशन कार्ड (परिवार स्थिति सत्यापन हेतु)',
      'आधार कार्ड',
    ],
    where_to_apply: [
      'निकटतम LPG वितरक एजेंसी',
      'ग्राम पंचायत नागरिक सुविधा केंद्र',
    ],
    disclaimer: 'यह केवल प्रारंभिक पात्रता जानकारी है, आधिकारिक स्वीकृति नहीं।',
  },
  sources: [
    {
      document_id: 'pmuy_official_001',
      title: 'PMUY Official Guidelines',
      url: 'https://example.gov.in/official-document',
      page: 2,
    },
  ],
  speech: {
    status: 'generated',
    content_type: 'audio/mpeg',
    audio_base64: 'DEMO_AUDIO_DATA',
  },
};

/**
 * Scenario 3: Cannot Determine (Incomplete / Ambiguous Information)
 * Illustrates cannot_determine assessment with explicit missing_information list.
 */
export const mockCannotDetermineResponse: StandardTurnResponse = {
  session_id: 'sess_demo_003',
  turn_id: 'turn_012',
  status: 'completed',
  language: 'hi',
  answer: {
    text: 'दी गई जानकारी से अभी आपकी पात्रता निश्चित नहीं हो सकती है। कृपया छूटी हुई जानकारी स्पष्ट करें।',
  },
  assessment: {
    scheme_id: 'pmuy',
    result: 'cannot_determine',
    reasons: [],
    missing_information: [
      'household_lpg_connection',
      'applicant_age',
    ],
  },
  card: {
    scheme_name: 'प्रधानमंत्री उज्ज्वला योजना',
    documents: [
      'आधार कार्ड (आयु सत्यापन)',
      'राशन कार्ड (परिवार सत्यापन)',
    ],
    where_to_apply: [
      'LPG वितरक',
    ],
    disclaimer: 'यह केवल प्रारंभिक पात्रता जानकारी है, आधिकारिक स्वीकृति नहीं।',
  },
  sources: [
    {
      document_id: 'pmuy_official_001',
      title: 'PMUY Official Guidelines',
      url: 'https://example.gov.in/official-document',
      page: 4,
    },
  ],
  speech: {
    status: 'generated',
    content_type: 'audio/mpeg',
    audio_base64: 'DEMO_AUDIO_DATA',
  },
};

