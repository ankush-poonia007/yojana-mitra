export interface DemoStepContent {
  step: number;
  badge: {
    hi: string;
    en: string;
  };
  title: {
    hi: string;
    en: string;
  };
  instruction: {
    hi: string;
    en: string;
  };
  defaultPrompt: {
    hi: string;
    en: string;
  };
  assistantReply: {
    hi: string;
    en: string;
  };
}

export const MOCK_DEMO_STEPS: DemoStepContent[] = [
  {
    step: 1,
    badge: {
      hi: 'चरण 1: बोलकर या लिखकर पूछने का अभ्यास',
      en: 'Step 1: Practice Speaking or Typing',
    },
    title: {
      hi: 'माइक या कीबोर्ड से प्रश्न पूछें',
      en: 'Ask Using Microphone or Keyboard',
    },
    instruction: {
      hi: 'माइक बटन दबाकर अपना प्रश्न बोलें, या नीचे दिए गए टेक्स्ट बॉक्स में लिखकर "प्रश्न भेजें" पर क्लिक करें।',
      en: 'Tap the mic button and speak your query, or type in the box below and click "Submit Query".',
    },
    defaultPrompt: {
      hi: 'क्या मुझे उज्ज्वला योजना में गैस कनेक्शन मिल सकता है?',
      en: 'Can I get a gas connection under Ujjwala Yojana?',
    },
    assistantReply: {
      hi: 'मैं आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से कोई गैस कनेक्शन है?',
      en: 'I will help you understand your eligibility. Does your household already have an LPG connection?',
    },
  },
  {
    step: 2,
    badge: {
      hi: 'चरण 2: उत्तर सुनने व पढ़ने का अभ्यास',
      en: 'Step 2: Listen & Read Responses',
    },
    title: {
      hi: 'सहायक का उत्तर सुनें व पढ़ें',
      en: 'Listen to and Read the Assistant Reply',
    },
    instruction: {
      hi: 'सहायक का उत्तर स्क्रीन पर लिखा हुआ है। "बोलकर सुनें" बटन दबाकर आवाज़ सुनें, या "रोकें" पर क्लिक करें।',
      en: 'The assistant reply is shown on screen. Tap "Listen" to hear the voice playback, or "Stop" to halt.',
    },
    defaultPrompt: {
      hi: 'नहीं, हमारे पास पहले से कोई गैस कनेक्शन नहीं है।',
      en: 'No, we do not have an existing LPG connection.',
    },
    assistantReply: {
      hi: 'समझ गया। क्या आवेदन करने वाली महिला की उम्र 18 वर्ष या उससे अधिक है?',
      en: 'Understood. Is the woman applying aged 18 years or above?',
    },
  },
  {
    step: 3,
    badge: {
      hi: 'चरण 3: दस्तावेज़ व परिणाम कार्ड का नमूना',
      en: 'Step 3: Sample Action Card',
    },
    title: {
      hi: 'दस्तावेज़ और परिणाम कार्ड देखें',
      en: 'View Documents and Outcome Card',
    },
    instruction: {
      hi: 'बातचीत पूरी होने पर आपको ऐसा कार्ड मिलता है, जिसमें ज़रूरी दस्तावेज़ और आवेदन की जगह लिखी होती है।',
      en: 'At the end of a consultation, you receive an action card listing required documents and application venues.',
    },
    defaultPrompt: {
      hi: 'हाँ, उम्र 25 वर्ष है।',
      en: 'Yes, she is 25 years old.',
    },
    assistantReply: {
      hi: 'आपकी दी गई जानकारी के आधार पर आप संभवतः पात्र हो सकते हैं। नीचे दिया गया नमूना कार्ड देखें।',
      en: 'Based on the information provided, you may be likely eligible. See the sample card below.',
    },
  },
];

export const MOCK_SAMPLE_CARD = {
  schemeName: {
    hi: 'प्रधानमंत्री उज्ज्वला योजना (नमूना कार्ड)',
    en: 'Pradhan Mantri Ujjwala Yojana (Sample Card)',
  },
  documents: {
    hi: ['आधार कार्ड', 'राशन कार्ड (परिवार सूची का प्रमाण)', 'बैंक पासबुक'],
    en: ['Aadhaar Card', 'Ration Card (Proof of Family Composition)', 'Bank Passbook'],
  },
  whereToApply: {
    hi: ['निकटतम LPG वितरक एजेंसी', 'कॉमन सर्विस सेंटर (CSC)'],
    en: ['Nearest LPG Distributor Agency', 'Common Service Centre (CSC)'],
  },
  disclaimer: {
    hi: 'यह अभ्यास हेतु केवल एक नमूना कार्ड है, आधिकारिक सरकारी निर्णय नहीं।',
    en: 'This is an illustrative sample card for practice only, not an official decision.',
  },
};
