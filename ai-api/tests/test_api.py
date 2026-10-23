def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_members_are_safe_directory_records(client):
    data = client.get("/members").json()
    assert len(data) == 2
    assert "registrationNumber" not in data[0]


def test_member_and_missing_member(client):
    assert client.get("/members/aline-test").status_code == 200
    assert client.get("/members/not-real").status_code == 404


def test_exact_name_and_alias(client):
    for question in ("Tell me about Aline Test", "What did Ali build?"):
        data = client.post("/ask", json={"question": question}).json()
        assert data["match"]["id"] == "aline-test"
        assert data["confidence"] == 1.0


def test_role_and_feature(client):
    role = client.post("/ask", json={"question": "Who is the AI Engineer?"}).json()
    feature = client.post("/ask", json={"question": "Who built offline mode?"}).json()
    assert role["match"]["id"] == "beno-test"
    assert feature["match"]["id"] == "aline-test"


def test_no_match(client):
    data = client.post("/ask", json={"question": "Who repairs tractors in Nyagatare?"}).json()
    assert data["match"] is None
    assert data["evidenceLinks"] == []


def test_question_validation(client):
    assert client.post("/ask", json={}).status_code == 422
    assert client.post("/ask", json={"question": "   "}).status_code == 422
    assert client.post("/ask", json={"question": "x" * 301}).status_code == 422


def test_ask_schema(client):
    data = client.post("/ask", json={"question": "Tell me about Ben"}).json()
    assert set(data) == {"query", "match", "confidence", "reason", "introduction", "evidenceLinks", "modelVersion", "groupCode", "source"}


def test_model_info(client):
    data = client.get("/model-info").json()
    assert data["memberCount"] == 2
    assert len(data["datasetFingerprint"]) == 64

