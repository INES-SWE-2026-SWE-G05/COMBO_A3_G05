import json
from pathlib import Path

from app.data_loader import dataset_fingerprint, load_members
from app.matcher import MemberMatcher
from app.settings import DATA_PATH, MATCH_THRESHOLD


def test_empty_dataset_is_safe():
    assert MemberMatcher([]).match("anything").member is None


def test_fixture_dataset_validates():
    path = Path(__file__).parent / "fixtures" / "members.json"
    assert len(load_members(path)) == 2


def fixture_matcher() -> MemberMatcher:
    path = Path(__file__).parent / "fixtures" / "members.json"
    return MemberMatcher(load_members(path))


def test_partial_name_in_a_natural_question():
    result = fixture_matcher().match("Can you tell me what Aline did for the project?")
    assert result.member is not None
    assert result.member["id"] == "aline-test"


def test_misspelled_name_is_tolerated():
    result = fixture_matcher().match("Tell me about Alinne")
    assert result.member is not None
    assert result.member["id"] == "aline-test"
    assert "Likely name match" in result.reason


def test_single_skill_keyword_matches_longer_skill():
    result = fixture_matcher().match("Who worked with React?")
    assert result.member is not None
    assert result.member["id"] == "aline-test"
    assert "skill keyword" in result.reason


def test_production_dataset_loads_all_six_members():
    members = load_members(DATA_PATH)
    assert len(members) == 6
    assert all(m["id"] and m["fullName"] and m["role"] for m in members)


def test_production_dataset_fingerprint_is_valid():
    fingerprint = dataset_fingerprint(DATA_PATH)
    assert len(fingerprint) == 64
    assert int(fingerprint, 16) > 0


def test_production_exact_name_queries():
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    for expected_id in [
        "kawaya-gueylord",
        "adam-ibrahim-hachim",
        "isimbi-huguette-parvine",
        "sebit-umkalsum-karim-mustafa",
        "tuyisingize-dieudonne",
        "yaya-gouni-souleyman",
    ]:
        member = next(m for m in matcher.members if m["id"] == expected_id)
        res = matcher.match(f"Tell me about {member['fullName']}")
        assert res.member is not None
        assert res.member["id"] == expected_id
        assert res.confidence == 1.0


def test_production_alias_queries():
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    aliases = {
        "Gueylord": "kawaya-gueylord",
        "Adam": "adam-ibrahim-hachim",
        "Huguette": "isimbi-huguette-parvine",
        "Sebit": "sebit-umkalsum-karim-mustafa",
        "Dieudonne": "tuyisingize-dieudonne",
        "Yaya": "yaya-gouni-souleyman",
    }
    for alias, expected_id in aliases.items():
        res = matcher.match(f"What did {alias} build?")
        assert res.member is not None
        assert res.member["id"] == expected_id
        assert res.confidence == 1.0


def test_production_role_queries():
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    for expected_id in [
        "kawaya-gueylord",
        "adam-ibrahim-hachim",
        "isimbi-huguette-parvine",
        "sebit-umkalsum-karim-mustafa",
        "tuyisingize-dieudonne",
        "yaya-gouni-souleyman",
    ]:
        member = next(m for m in matcher.members if m["id"] == expected_id)
        res = matcher.match(f"Who is the {member['role']}?")
        assert res.member is not None
        assert res.member["id"] == expected_id
        assert res.confidence >= 0.95


def test_production_feature_queries():
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    for expected_id in [
        "kawaya-gueylord",
        "adam-ibrahim-hachim",
        "isimbi-huguette-parvine",
        "sebit-umkalsum-karim-mustafa",
        "tuyisingize-dieudonne",
        "yaya-gouni-souleyman",
    ]:
        member = next(m for m in matcher.members if m["id"] == expected_id)
        res = matcher.match(f"Who built {member['feature']}?")
        assert res.member is not None
        assert res.member["id"] == expected_id
        assert res.confidence >= 0.95


def test_production_no_match_queries():
    matcher = MemberMatcher(load_members(DATA_PATH), MATCH_THRESHOLD)
    no_matches = [
        "What is today's maize price in Kigali?",
        "How do I reset my account password?",
        "Where is the nearest agricultural cooperative office?",
        "Can you predict tomorrow's rainfall in Musanze?",
        "Who won the football match yesterday?",
    ]
    for q in no_matches:
        res = matcher.match(q)
        assert res.member is None
        assert res.confidence < MATCH_THRESHOLD
