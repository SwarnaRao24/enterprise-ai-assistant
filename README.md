# Enterprise AI Assistant with Guardrails

## Overview
FastAPI backend that answers questions using an LLM with input/output guardrails and JSONL logging.
This repo simulates a two-person workflow.

- Person A: Backend + GenAI integration
- Person B: Evaluation + Documentation

## Endpoints
- GET /health
- POST /ask

## Logging
Interactions are logged with timestamps and guardrail decisions.

## Evaluation (Person B)
Manual scoring metrics:
- Relevance
- Completeness
- Clarity

Files:
- app/eval/rubric.md
- app/eval/samples.jsonl
