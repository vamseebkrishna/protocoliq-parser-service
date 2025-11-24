# protocoliq-parser-service
Microservice that converts clinical protocol text into structured inclusion/exclusion rules using LLMs. Built with FastAPI and aligned with the Eligibility Engine OpenAPI v1 contract.

AI-powered microservice built with FastAPI that parses clinical trial protocols into structured eligibility RuleSets.
Implements the /rulesets:parseProtocol endpoint defined in the Eligibility Engine OpenAPI v1 contract, enabling downstream systems (Rules Engine, CTMS, EDC, RTSM) to consume standardized inclusion/exclusion criteria.

🚀 Overview

The ProtocolIQ Parser Service takes raw protocol text as input and uses LLM-based extraction + normalization pipelines to generate:

Inclusion criteria

Exclusion criteria

Metadata (rulesetId, version, timestamps)

Confidence levels

Source text traceability

This service does not store rulesets. It only generates and returns them to the Eligibility Engine.

🧩 Architecture

<img width="603" height="239" alt="image" src="https://github.com/user-attachments/assets/54ea84df-deaa-4b49-953f-920bf3235339" />

Key layers:

API Layer (FastAPI)

LLM Service (OpenAI GPT models)

Normalization Layer (rule shaping, metadata injection)

Schema Validation (Draft 2020-12)

Observability (correlation IDs & structured logging)

📦 Features

Implements /rulesets:parseProtocol from the Eligibility Engine contract

AI-driven extraction using GPT-4.1 / GPT-5

Schema validation against RuleSet.schema.json

Rule normalization for consistent downstream processing

Multi-tenant support via X-Tenant-Id

Correlation ID tracing for GxP/Part 11 compliance

Modular service layout for easy expansion

Docker-ready for production deployment

📁 Project Structure

<img width="701" height="416" alt="image" src="https://github.com/user-attachments/assets/56607504-5fd4-497a-8f3a-368d7c648f69" />

🔌 API Endpoint

POST /rulesets:parseProtocol

Description:

Parses protocol text and generates a structured RuleSet.

Headers:

<img width="421" height="90" alt="image" src="https://github.com/user-attachments/assets/905c1352-1401-4750-81a7-dd5cc4625af7" />

Body:

<img width="513" height="204" alt="image" src="https://github.com/user-attachments/assets/9da1ad73-81fc-4dae-a041-fabd4a48d21c" />

Response:

Returns a RuleSet compliant with the JSON Schema and OpenAPI contract.

🧠 LLM Integration

This service uses OpenAI models to:

Extract eligibility criteria

Identify rule types (age, diagnosis, medication, labs, flags, custom)

Populate confidence + sourceText

Output normalized JSON only

The output always matches

RuleSet.schema.json.

🛡 Validation

All outputs are validated against the JSON Schema definitions located in the eligibility-engine-contract repository:

RuleSet.schema.json

Rule.schema.json

ParseProtocolResponse.schema.json

Prevents malformed or incomplete rule extraction.

🧪 Local Development

Install dependencies:

pip install -r requirements.txt

Run service:

uvicorn app.main:app --reload


Service runs at:

http://localhost:8001


Interactive API docs:

http://localhost:8001/docs

🐳 Docker Usage

Build:

docker build -t protocoliq-parser-service .

Run:

docker run -p 8001:8001 protocoliq-parser-service

🔐 Authentication

Uses API key header:

x-api-key: <your-key>


Future: OAuth2/JWT support for production integrations.

📜 Contract Compliance

This service follows:

OpenAPI v1 (Eligibility Engine Contract)

JSON Schema Draft 2020-12

21 CFR Part 11 principles (traceability via correlation IDs)

Everything returned from this service must be compatible with downstream engine services.

🤝 Related Repositories

eligibility-engine-contract

OpenAPI v1 & JSON Schemas

protocoliq-rules-engine (future)

Handles patient eligibility evaluation

🧭 Roadmap (Next Versions)

Support PDF ingestion + OCR

Metadata extraction (study design, endpoints)

Multi-language parsing

Enhanced rule classification

FDA submission-friendly audit logs
