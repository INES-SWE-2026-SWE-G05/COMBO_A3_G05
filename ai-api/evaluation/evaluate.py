import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.data_loader import load_members
from app.matcher import MemberMatcher
from app.settings import DATA_PATH, MATCH_THRESHOLD


def main() -> None:
    cases = json.loads((Path(__file__).parent / "queries.json").read_text())
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    member_cases = cases["memberQueries"]
    errors = []
    correct = 0
    for case in member_cases:
        result = matcher.match(case["query"])
        actual = result.member["id"] if result.member else None
        correct += actual == case["expectedMemberId"]
        if actual != case["expectedMemberId"]:
            errors.append({"query": case["query"], "expected": case["expectedMemberId"], "actual": actual})
    rejected = sum(matcher.match(query).member is None for query in cases["noMatchQueries"])
    report = {
        "top1Accuracy": correct / len(member_cases) if member_cases else None,
        "noMatchRejectionAccuracy": rejected / len(cases["noMatchQueries"]) if cases["noMatchQueries"] else None,
        "memberQueryCount": len(member_cases),
        "noMatchQueryCount": len(cases["noMatchQueries"]),
        "errors": errors,
        "status": "NEEDS_APPROVED_MEMBER_QUERIES" if not member_cases else "COMPLETE",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

