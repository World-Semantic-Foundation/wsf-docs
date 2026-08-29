# Architecture Deep-Dive : The WSF Semantic Engine

> **A deep technical dive into the WSF Semantic Engine architecture, design rationale, and implementation patterns.**

## 1. Purpose

This document explains **why** the WSF Semantic Engine is designed the way it is, going beyond the **what** documented in [ADR-WSF-24](../wsf-governance/ADR/ADR-WSF-24-WSF-Software-Architecture.md) and the **how** documented in [ARCHITECTURE.md](../wsf-software/docs/ARCHITECTURE.md).

## 2. Design Goals

The WSF Semantic Engine is designed to:

1. **Be authoritative** : The single source of truth for the 38 WSF concepts and all relationships
2. **Be queryable** : Support efficient graph, semantic, and fulltext queries
3. **Be validatable** : Apply SHACL constraints to ensure conformance
4. **Be integrable** : Connect to external semantic ecosystems (Schema.org, SKOS, TM Forum)
5. **Be visualizable** : Generate concept diagrams and relationship maps
6. **Be simulatable** : Support digital twins and capability simulation
7. **Be applicable** : Enable real-world enterprise architecture (OTCHERE Inc)

## 3. Architectural Principles

The WSF Semantic Engine follows these principles:

### 3.1 : Layered Architecture (3 layers)

Per ADR-WSF-24, the engine is structured as 3 distinct layers:

- **API Layer** : REST, gRPC, GraphQL, CLI, WebSocket (5 surfaces)
- **Services Layer** : 8 service modules (Concept, Relationship, Assertion, Identity, Validation, Inference, Query, Audit)
- **Store Layer** : Pluggable backends (PostgreSQL, Neo4j, MongoDB, SQLite, in-memory)

Each layer depends only on the layer below it. This enables:

- **Pluggable backends** : Replace Store without changing Services or API
- **Pluggable API surfaces** : Add new API types without changing Services
- **Independent testing** : Test each layer in isolation

### 3.2 : Pluggable Store Backends

Per ADR-WSF-24 §5, the engine supports 5 store backends:

| Backend | Use Case |
|---|---|
| **In-memory (MemoryStore)** | Development, testing, embedded |
| **SQLite** | Single-node production, edge deployment |
| **PostgreSQL** | Multi-node production with strong ACID guarantees |
| **Neo4j** | Graph-heavy workloads (knowledge graphs) |
| **MongoDB** | Flexible schema for evolving concept types |

All backends implement the same `StoreLayer` interface, enabling seamless switching.

### 3.3 : Service-Oriented Composition

The Services Layer is decomposed into 8 service modules:

1. **Concept Service** : Concept lifecycle management
2. **Relationship Service** : Relationship declaration and traversal
3. **Assertion Service** : Assertion submission and lifecycle
4. **Identity Service** : Namespace registration and CURIE resolution
5. **Validation Service** : SHACL validation of representations
6. **Inference Service** : OWL 2 RL entailment and explanation
7. **Query Service** : Pattern, graph, semantic, fulltext queries
8. **Audit Service** : Audit trail record and query

Each service is a TypeScript class with a single responsibility. Services communicate via the Store Layer (not directly with each other).

### 3.4 : Type System as Documentation

The TypeScript type system serves as machine-readable documentation:

- All 38 concepts are typed (`Concept` interface)
- All 12 relationship kinds are typed (`RelationshipKind` enum)
- All 6 semantic status values are typed (`SemanticStatus` enum)
- All 11 representation formats are typed (`RepresentationFormat` enum)

The types are the **canonical interface** for any WSF-compatible implementation.

### 3.5 : Engine Result Envelope

All service operations return `EngineResult<T>`:

```typescript
interface EngineResult<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string; details?: unknown };
  meta?: { timestamp: string; execution_time_ms: number; actor?: CURIE };
}
```

This pattern:

- Forces explicit success/failure handling
- Provides structured error information
- Includes execution metadata for observability
- Avoids thrown exceptions for normal control flow

## 4. Data Model

The engine stores 7 core collections per ADR-WSF-24 §5.2:

1. **concepts** : All concept definitions
2. **relationships** : Typed relationships between concepts
3. **assertions** : Assertions about the world
4. **identities** : Identifier mappings and namespaces
5. **provenance** : Audit trail entries
6. **evidence** : Evidence file references
7. **versions** : Concept version history

Each collection has a JSON `data` field for forward-compatible schema evolution.

## 5. Query Patterns

The engine supports 4 query types:

1. **Pattern queries** : Match concepts by name or semantic_id prefix
2. **Graph queries** : Cypher-like traversal of relationships
3. **Semantic queries** : SPARQL-like RDF graph queries
4. **Fulltext queries** : Match concepts by text search

In v0.1.0, pattern queries are fully implemented. Graph, semantic, and fulltext queries are scaffolded for v0.2.0.

## 6. Validation

The engine applies SHACL shapes to all entities:

- **ConceptShape** : Validates Concept structure (CURIE patterns, required fields, status enum)
- **RelationshipShape** : Validates Relationship structure
- **AssertionShape** : Validates Assertion structure
- **ProvenanceShape** : Validates Provenance metadata
- **ValidityShape** : Validates Validity periods
- **PropositionShape** : Validates Proposition modality
- **EvidenceShape** : Validates Evidence references

SHACL shapes are externalised in [wsf-spec/shacl/](../wsf-spec/shacl/wsf-shapes.ttl) so any conformant implementation can validate against them.

## 7. Performance Considerations

The engine optimises for:

- **Concept lookup** : O(1) via semantic_id index (unique)
- **Relationship traversal** : O(log n) via composite index on (subject, type, object)
- **Assertion queries** : O(log n) via temporal index on asserted_at
- **Audit queries** : O(log n) via timestamp index

For production workloads with > 100K concepts, the PostgreSQL or Neo4j backend is recommended.

## 8. Deployment Modes

The engine supports 3 deployment modes:

### 8.1 : Embedded Mode

The engine runs in-process with the consuming application. Suitable for:

- Single-user applications
- Edge deployments
- Testing

```typescript
import { SemanticEngine } from '@wsf/semantic-engine';
const engine = new SemanticEngine({ store_backend: 'memory' });
```

### 8.2 : Library Mode

The engine runs as a shared library across multiple processes on the same host. Suitable for:

- Microservice architectures
- Multi-tenant applications

```typescript
import { SemanticEngine } from '@wsf/semantic-engine';
const engine = new SemanticEngine({ store_backend: 'sqlite', path: '/var/lib/wsf.db' });
```

### 8.3 : Service Mode

The engine runs as a standalone service accessible via REST/gRPC. Suitable for:

- Distributed systems
- Multi-host deployments

```typescript
import { SemanticEngine, startRESTServer } from '@wsf/semantic-engine';
const engine = new SemanticEngine({ store_backend: 'postgresql' });
await engine.initialise();
await startRESTServer(engine, { port: 8080 });
```

## 9. Security

The engine implements security via:

- **OAuth 2.0 + OpenID Connect** for authentication
- **RBAC** for authorisation (scope-based)
- **CURIE validation** to prevent injection attacks
- **SHACL validation** to prevent malformed data
- **Audit trail** for all state changes

## 10. Observability

The engine provides observability via:

- **Health check endpoint** (`GET /v1/health`)
- **Execution metadata** in all responses (`meta.timestamp`, `meta.execution_time_ms`)
- **Audit trail** for state change tracking
- **Error codes** in failure responses (e.g., `CONCEPT_NOT_FOUND`)

## 11. Future Roadmap

| Version | Focus | Status |
|---|---|---|
| 0.1.0 | Foundation (3 layers, 8 services, 7 schemas) | Complete |
| 0.2.0 | Graph queries (Cypher), full SHACL validation | Planned |
| 0.3.0 | Full-text search, advanced inference | Planned |
| 1.0.0 | Production hardening, observability, federation | Planned |

## Cross-References

- [ADR-WSF-24 : WSF Software Architecture](../wsf-governance/ADR/ADR-WSF-24-WSF-Software-Architecture.md)
- [ARCHITECTURE.md](../wsf-software/docs/ARCHITECTURE.md) : Implementation status
- [REST API Specification](../wsf-spec/openapi/wsf-semantic-engine.openapi.yaml)
- [JSON Schemas](../wsf-software/schemas/json/)

---

*Architecture deep-dive. Status: Baseline.*