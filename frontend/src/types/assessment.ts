export type EligibilityResult =
  | 'likely_eligible'
  | 'likely_not_eligible'
  | 'cannot_determine';

export interface Assessment {
  scheme_id: string;
  result: EligibilityResult;
  reasons: string[];
  missing_information: string[];
}

export interface TakeAwayCard {
  scheme_name: string;
  documents: string[];
  where_to_apply: string[];
  disclaimer: string;
}

export interface SourceEvidence {
  document_id: string;
  title: string;
  url: string;
  page?: number;
  section?: string;
}

