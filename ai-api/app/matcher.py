import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


STOP_WORDS = {
    "about", "built", "did", "does", "for", "from", "have", "help", "made",
    "member", "on", "person", "please", "project", "tell", "team", "the", "what",
    "which", "who", "work", "worked", "works", "with",
}


def meaningful_tokens(value: str) -> set[str]:
    return {
        token for token in normalize(value).split()
        if len(token) >= 3 and token not in STOP_WORDS
    }


def searchable_document(member: dict[str, Any]) -> str:
    evidence = " ".join(str(link) for link in member.get("evidenceLinks", []))
    values = [
        member["fullName"], " ".join(member["aliases"]), member["role"],
        " ".join(member["skills"]), member["feature"], member["problem"],
        member["contribution"], evidence,
    ]
    return normalize(" ".join(values))


@dataclass(frozen=True)
class MatchResult:
    member: dict[str, Any] | None
    confidence: float
    reason: str


class MemberMatcher:
    def __init__(self, members: list[dict[str, Any]], threshold: float = 0.45):
        self.members = members
        self.threshold = threshold
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        if members:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
            self.matrix = self.vectorizer.fit_transform(searchable_document(m) for m in members)

    def match(self, query: str) -> MatchResult:
        normalized = normalize(query)
        if not normalized or not self.members or self.vectorizer is None:
            return MatchResult(None, 0.0, "No approved member matched this question.")

        # Exact names and aliases are trusted identifiers, so they receive a
        # transparent deterministic match instead of relying on vocabulary size.
        for member in self.members:
            identifiers = [member["fullName"], *member["aliases"]]
            for identifier in identifiers:
                token = normalize(identifier)
                if token and re.search(rf"\b{re.escape(token)}\b", normalized):
                    return MatchResult(member, 1.0, f"Exact name or alias match: {identifier}.")

        query_tokens = meaningful_tokens(normalized)

        # Accept a distinctive first, middle, or last name without requiring the
        # visitor to repeat the full approved name.
        for member in self.members:
            name_tokens = meaningful_tokens(" ".join([member["fullName"], *member["aliases"]]))
            shared = query_tokens & name_tokens
            if any(len(token) >= 4 for token in shared):
                recognized = max(shared, key=len)
                return MatchResult(member, 0.98, f"Recognized member name: {recognized}.")

        # Tolerate realistic name typos while requiring a strong similarity and
        # at least four characters to avoid unsafe matches on short words.
        fuzzy_candidates: list[tuple[float, dict[str, Any], str, str]] = []
        for member in self.members:
            name_tokens = meaningful_tokens(" ".join([member["fullName"], *member["aliases"]]))
            for typed in query_tokens:
                if len(typed) < 4:
                    continue
                for approved in name_tokens:
                    ratio = SequenceMatcher(None, typed, approved).ratio()
                    if ratio >= 0.78:
                        fuzzy_candidates.append((ratio, member, typed, approved))
        if fuzzy_candidates:
            ratio, member, typed, approved = max(fuzzy_candidates, key=lambda item: item[0])
            confidence = round(min(0.95, 0.8 + ratio * 0.15), 4)
            return MatchResult(member, confidence, f"Likely name match: {typed} → {approved}.")

        for member in self.members:
            for field_name in ("role", "feature"):
                phrase = normalize(member[field_name])
                if phrase and re.search(rf"\b{re.escape(phrase)}\b", normalized):
                    return MatchResult(member, 0.95, f"Exact approved {field_name} phrase match.")

        # Match a distinctive word from a skill phrase, so a natural question
        # such as "who worked on React?" can match "React Native".
        skill_candidates: list[tuple[dict[str, Any], set[str]]] = []
        for member in self.members:
            overlap = query_tokens & meaningful_tokens(" ".join(member["skills"]))
            if overlap:
                skill_candidates.append((member, overlap))
        if len(skill_candidates) == 1:
            member, overlap = skill_candidates[0]
            skill = max(overlap, key=len)
            return MatchResult(member, 0.9, f"Matched approved skill keyword: {skill}.")

        query_vector = self.vectorizer.transform([normalized])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        best_index = int(scores.argmax())
        score = float(scores[best_index])
        if score < self.threshold:
            return MatchResult(None, score, "Confidence was below the safe matching threshold.")
        member = self.members[best_index]
        return MatchResult(member, score, "Best TF-IDF similarity across approved profile fields.")

