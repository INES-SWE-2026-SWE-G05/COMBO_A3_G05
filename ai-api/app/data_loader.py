import hashlib
import json
import re
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "fullName", "registrationNumber", "aliases", "githubUsername", "role",
    "skills", "targetUser", "problem", "contribution", "feature",
    "outcomeMetric", "evidenceLinks", "testerFeedback", "introductionDraft",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "member"


def load_members(path: Path) -> list[dict[str, Any]]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise ValueError(f"Member dataset not found: {path}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid member dataset JSON: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError("Member dataset must be a JSON array")
    seen: set[str] = set()
    members: list[dict[str, Any]] = []
    for index, member in enumerate(data):
        if not isinstance(member, dict):
            raise ValueError(f"Member {index + 1} must be an object")
        missing = REQUIRED_FIELDS - member.keys()
        if missing:
            raise ValueError(f"Member {index + 1} missing fields: {', '.join(sorted(missing))}")
        if not str(member["fullName"]).strip():
            raise ValueError(f"Member {index + 1} has an empty fullName")
        for field in ("aliases", "skills", "evidenceLinks"):
            if not isinstance(member[field], list):
                raise ValueError(f"Member {index + 1} field {field} must be an array")
        enriched = dict(member)
        enriched["id"] = str(member.get("id") or slugify(member["fullName"]))
        if enriched["id"] in seen:
            raise ValueError(f"Duplicate member id: {enriched['id']}")
        seen.add(enriched["id"])
        members.append(enriched)
    return members


def dataset_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

