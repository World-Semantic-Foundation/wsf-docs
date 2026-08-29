# 12 Foundational Principles of WSF

> **The governing principles that shape every architectural decision in the World Semantic Foundation.**

These principles establish the design specification for WSF. They are reflected throughout the architectural decision records, the concept definitions, the implementation specifications, and the governance model.

---

## 1. Semantic Primacy

**Meaning precedes representation.**

The semantic commitment is the authoritative statement. Representations (RDF, OWL, JSON-LD, YAML, database schemas) implement the semantic commitment; they do not define it.

A change in representation does not constitute a change in semantics. The semantic identity persists across representation transformations.

## 2. Minimal Foundation

**The architecture provides the smallest sufficiently expressive foundation.**

WSF does not define every domain concept. It establishes a minimal set of semantic primitives from which all domain semantics can be derived through composition and specialization.

Concepts are admitted to the foundation only when their semantics cannot be adequately derived from other WSF primitives without loss of meaning.

## 3. Explicit Specialization

**Domain and enterprise concepts specialize; they do not silently redefine foundational concepts.**

Specialization is the only path from foundational concepts to specialized ones. Specializations identify their parent concept, preserve inherited meaning, declare added semantics, declare constraints, and remain semantically conformant.

Silent redefinition is architecturally prohibited.

## 4. Versioned Evolution

**Semantic changes are governed through the lifecycle.**

Semantic evolution records the change to meaning, identity, constraints, relationships, scope, or authority. The architecture distinguishes semantic change, representation change, and repository change ; these are not equivalent.

Every semantic change moves through the 8-stage Change Control Lifecycle with explicit governance.

## 5. Authoritative Provenance

**Sources are tracked for every semantic artifact.**

Every concept, assertion, and decision carries provenance metadata: source, asserted-by, authority, asserted-at, method, derivation chain.

Provenance provides the basis for trust evaluation and is preserved through versioning.

## 6. Governance First

**Architecture precedes implementation.**

No implementation proceeds without an explicitly authorized architectural decision (ADR) and change request (CR). The architectural baseline is established before implementation work begins.

The architecture is the source of truth; implementation is its expression.

## 7. Layered Realization

**Multiple levels, distinct concerns.**

The architecture is organized in layers:

- Foundational semantics (Tier 1)
- Domain concepts (Tier 2)
- Specialized concepts (Tier 3)
- Contextual specializations
- Assertions
- Evidence and provenance
- Formal representations

Each layer has distinct responsibilities. The architecture does not collapse layers into a single abstraction.

## 8. Traceable Rationale

**Decisions document their reasoning.**

Every architectural decision record captures the context, drivers, considered alternatives, and rationale. Every change request documents the scope and justification.

The reasoning is the foundation for future evolution. Decisions are reviewable.

## 9. Constrained Extensibility

**Extensions follow the governance model.**

Extensions to the foundation are allowed but follow the same governance discipline as foundational concepts: investigation, decision, and implementation.

Uncontrolled extension is architecturally prohibited; controlled extension is enabled.

## 10. Verifiable Conformance

**Claims are demonstrable.**

A specialization demonstrates conformance to its parent. An assertion demonstrates validity against its semantic context. A semantic artifact demonstrates alignment with its specification.

Conformance is a verifiable property, not an asserted one.

## 11. Identity by Meaning

**Identity persists through compatible evolution.**

A semantic artifact is identified by its meaning, not its name, label, representation, or location. Identity persists through representation changes, context changes, version evolution, and naming changes.

Identity and version are distinct concepts. A new identity is required only when the meaning itself has materially changed.

## 12. Investigation-Driven

**Architectural decisions follow research.**

Every architectural decision traces back to documented investigation. The investigation record is preserved as the research lineage of the foundation.

Architectural decisions are evidence-based.

---

## Application

These 12 principles apply to:

- Every architectural decision record
- Every concept definition
- Every implementation choice
- Every governance action
- Every cross-system integration
- Every evolution of the foundation

The principles are the specification. They are not aspirational; they are architectural constraints.

---

## Cross-Reference

The principles are realized through:

- **ADRs**: Each ADR cites the principles it implements.
- **Concept definitions**: Each concept specifies which principles it embodies.
- **Implementation CRs**: Each CR demonstrates adherence to applicable principles.
- **Governance documents**: The lifecycle and status models implement the principles.

---

*These principles are the architectural specification of the World Semantic Foundation.*
