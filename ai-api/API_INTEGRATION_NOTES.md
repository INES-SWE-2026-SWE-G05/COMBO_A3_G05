# API Integration Notes

## Purpose
This document describes the API integration for AgriSoko Pocket.

## Available Endpoints
- GET /health: Checks API availability.
- GET /members: Retrieves members.
- GET /members/{id}: Retrieves a member by ID.
- POST /ask: Submits a request to the API.
- GET /model-info: Retrieves model information.

## Validation and Testing
The API uses Pydantic response schemas and returns a 404 response for invalid member IDs.

API tests are located in ai-api/tests/test_api.py.

## Integration
The mobile client should follow the API response schemas when communicating with the backend.
