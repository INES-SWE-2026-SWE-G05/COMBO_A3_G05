import json
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .data_loader import dataset_fingerprint, load_members
from .matcher import MemberMatcher
from .models import AskRequest, AskResponse
from .settings import (
    APP_VERSION, DATA_PATH, GROUP_CODE, MATCH_THRESHOLD, METADATA_PATH, MODEL_VERSION,
)


def public_profile(member: dict[str, Any]) -> dict[str, Any]:
    return {key: member[key] for key in (
        "id", "fullName", "registrationNumber", "aliases", "githubUsername",
        "role", "skills", "targetUser", "problem", "contribution", "feature",
        "outcomeMetric", "evidenceLinks", "testerFeedback", "introductionDraft",
    )}


def directory_profile(member: dict[str, Any]) -> dict[str, Any]:
    return {key: member[key] for key in ("id", "fullName", "aliases", "role", "skills", "feature")}


@asynccontextmanager
async def lifespan(app: FastAPI):
    members = load_members(DATA_PATH)
    app.state.members = members
    app.state.matcher = MemberMatcher(members, MATCH_THRESHOLD)
    yield


app = FastAPI(title="AgriSoko Pocket API", version=APP_VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": APP_VERSION, "groupCode": GROUP_CODE}


@app.get("/members")
async def members(request: Request) -> list[dict[str, Any]]:
    return [directory_profile(member) for member in request.app.state.members]


@app.get("/members/{member_id}")
async def member(member_id: str, request: Request) -> dict[str, Any]:
    found = next((item for item in request.app.state.members if item["id"] == member_id), None)
    if found is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return public_profile(found)


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest, request: Request) -> AskResponse:
    result = request.app.state.matcher.match(payload.question)
    matched = public_profile(result.member) if result.member else None
    return AskResponse(
        query=payload.question,
        match=matched,
        confidence=round(result.confidence, 4),
        reason=result.reason,
        introduction=result.member["introductionDraft"] if result.member else None,
        evidenceLinks=result.member["evidenceLinks"] if result.member else [],
        modelVersion=MODEL_VERSION,
        groupCode=GROUP_CODE,
        source="Live AI",
    )


@app.get("/model-info")
async def model_info(request: Request) -> dict[str, Any]:
    metadata = {
        "modelVersion": MODEL_VERSION,
        "vectorizer": "TfidfVectorizer(ngram_range=(1, 2), lowercase=True)",
        "threshold": MATCH_THRESHOLD,
        "datasetFingerprint": dataset_fingerprint(DATA_PATH),
        "memberCount": len(request.app.state.members),
        "buildCommit": "unknown",
        "limitations": [
            "Matches only approved member data.",
            "Unfamiliar wording can produce a no-match result.",
            "An empty approved dataset returns no matches.",
        ],
    }
    if METADATA_PATH.exists():
        built = json.loads(METADATA_PATH.read_text())
        metadata["buildCommit"] = built.get("buildCommit", "unknown")
    return metadata

