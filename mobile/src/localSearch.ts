import {GROUP_CODE} from './config';
import type {AskResult, Member} from './types';

const STOP_WORDS = new Set(['about', 'built', 'did', 'does', 'for', 'from', 'made', 'member', 'on', 'person', 'please', 'project', 'tell', 'team', 'the', 'what', 'which', 'who', 'work', 'worked', 'works', 'with']);

const normalize = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
const tokens = (value: string) => normalize(value).split(' ').filter(token => token.length >= 3 && !STOP_WORDS.has(token));

function similarity(left: string, right: string): number {
  const a = normalize(left); const b = normalize(right);
  if (!a || !b) return 0;
  const rows = Array.from({length: a.length + 1}, (_, i) => Array<number>(b.length + 1).fill(0).map((_, j) => i === 0 ? j : j === 0 ? i : 0));
  for (let i = 1; i <= a.length; i += 1) for (let j = 1; j <= b.length; j += 1) rows[i]![j] = a[i - 1] === b[j - 1] ? rows[i - 1]![j - 1]! : 1 + Math.min(rows[i - 1]![j]!, rows[i]![j - 1]!, rows[i - 1]![j - 1]!);
  return 1 - rows[a.length]![b.length]! / Math.max(a.length, b.length);
}

export function localAsk(question: string, members: Member[], reasonPrefix = 'Using information built into the app.'): AskResult {
  const queryTokens = new Set(tokens(question));
  let best: {member: Member; score: number; reason: string} | null = null;
  for (const member of members) {
    const names = [member.fullName, ...member.aliases];
    for (const name of names) {
      const normalizedName = normalize(name);
      if (normalizedName && normalize(question).includes(normalizedName)) return result(question, member, 1, `${reasonPrefix} Recognized name or alias: ${name}.`);
    }
    for (const nameToken of tokens(names.join(' '))) {
      for (const queryToken of queryTokens) {
        const score = similarity(queryToken, nameToken);
        if (score >= 0.75 && (!best || score > best.score)) best = {member, score: Math.min(.95, .8 + score * .15), reason: `${reasonPrefix} Likely name match: ${queryToken} → ${nameToken}.`};
      }
    }
    const searchable = tokens([member.role, member.feature, member.contribution, ...member.skills].join(' '));
    const overlap = searchable.filter(token => queryTokens.has(token));
    if (overlap.length) {
      const score = Math.min(.94, .82 + overlap.length * .04);
      if (!best || score > best.score) best = {member, score, reason: `${reasonPrefix} Matched profile keyword${overlap.length > 1 ? 's' : ''}: ${overlap.join(', ')}.`};
    }
  }
  return best ? result(question, best.member, best.score, best.reason) : {
    query: question, match: null, confidence: 0, reason: `${reasonPrefix} No confident member match was found.`, introduction: null,
    evidenceLinks: [], modelVersion: 'bundled-search-v1', groupCode: GROUP_CODE, source: 'Built-in fallback',
  };
}

function result(query: string, member: Member, confidence: number, reason: string): AskResult {
  return {query, match: member, confidence, reason, introduction: member.introductionDraft, evidenceLinks: member.evidenceLinks, modelVersion: 'bundled-search-v1', groupCode: GROUP_CODE, source: 'Built-in fallback'};
}
