export type DirectoryMember = {
  id: string; fullName: string; aliases: string[]; role: string; skills: string[]; feature: string;
};

export type Member = DirectoryMember & {
  registrationNumber: string; githubUsername: string; targetUser: string; problem: string;
  contribution: string; outcomeMetric: string; evidenceLinks: string[];
  testerFeedback: string; introductionDraft: string;
};

export type AskResult = {
  query: string; match: Member | null; confidence: number; reason: string;
  introduction: string | null; evidenceLinks: string[]; modelVersion: string;
  groupCode: string; source: 'Live AI' | 'Cached' | 'Offline Match' | 'Built-in fallback';
};

export type RootStackParamList = {
  Main: undefined;
  Result: { result: AskResult };
  Profile: { memberId: string; fallback?: Member };
};

