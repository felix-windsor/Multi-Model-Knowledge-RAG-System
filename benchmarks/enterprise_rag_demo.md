# Enterprise Local RAG Demo Document

## Background

The AI application prototype targets private-network document reading acceleration.
The intended deployment environment uses locally hosted Qwen-family models and
keeps all document parsing, retrieval, and answer generation inside the internal
network.

## Business Problem

The original document workflow relied on coarse chunking and direct keyword
search. Users had to manually scan long technical reports, meeting notes, and
engineering files before they could ask precise questions. The main pain points
were slow document reading, weak semantic retrieval, missing entity relations,
and limited reuse of parsed knowledge across downstream systems.

## Prototype Architecture

The prototype exposes a FastAPI service with five core API groups:

- document upload
- asynchronous task status polling
- document question answering
- knowledge graph export
- service health checks

The retrieval layer combines vector retrieval and graph-enhanced reasoning.
The document pipeline extracts text chunks, entities, and relations, then stores
structured knowledge for later query and graph visualization.

## Model Configuration

The benchmark configuration uses a Qwen 80B-level text model for answer
generation, a Qwen-VL 32B-level multimodal model for visual understanding, and a
Qwen embedding model with 1024-dimensional vectors for semantic retrieval.
This setup is intended to approximate an enterprise private-network deployment
instead of relying on the newest general-purpose cloud model.

## Expected Evaluation Points

The demo should measure document processing latency, upload latency, query
latency, query success rate, answer usability, exported entity count, exported
relation count, and whether answers mention expected concepts such as FastAPI,
knowledge graph, vector retrieval, Qwen, internal network, and API integration.
