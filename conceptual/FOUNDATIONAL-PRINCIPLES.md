# 12 Foundational Principles of WSF

> **The governing principles that shape every decision in the World Semantic Foundation.**

These principles are established by CR-WSF-17 Rev.1 §7 and reflect the investigation record preserved in the governance repository. They are **immutable governance principles** — any change requires an explicit ADR.

---

## Principle 1 — Semantic Primacy

> **Foundational semantics precede domain specialization.**

Meaning exists before representation. Domain specialization must inherit and constrain foundational semantics, not redefine them.

```
Meaning (foundational)
   ↓
Representation (domain-specific)
   ↓
Execution (implementation)
```

**Implications**:
- WSF establishes the meaning; downstream systems adapt the representation
- Specialized semantics must trace to foundational meaning
- Foundational changes propagate explicitly, not silently

---

## Principle 2 — Minimal Foundation

> **WSF shall seek the smallest sufficient foundational semantic vocabulary.**

WSF should NOT attempt to model every possible domain concept. It should establish the minimum authoritative semantic primitives necessary to support coherent semantic specialization.

**Implications**:
- 12 foundational candidates (Tier 1) + 9 supporting constructs (Tier 2) + 16+ derived (Tier 3)
- "Popularity does not establish foundational status"
- "Minimal but sufficient" — neither too narrow nor too broad

---

## Principle 3 — Explicit Specialization

> **Specialized semantic systems shall specialize foundational concepts rather than silently redefine them.**

```
WSF Capability
   ↓ specializes
OpenDEA Business Capability
```

**Implications**:
- WSF Capability means one thing across all contexts
- OpenDEA Business Capability is a CONTEXTUAL specialization
- The specialization MUST preserve the inherited meaning
- Silent redefinition = semantic violation

---

## Principle 4 — Identity Separation

> **Identity, Identifier, Name, Reference, and Representation shall remain conceptually distinct.**

| Concept | Purpose |
|---|---|
| **Identity** | Stable persistent identifier for the semantic artifact |
| **Identifier** | Concrete representation of identity (URI, UUID, etc.) |
| **Name** | Human-readable label |
| **Reference** | Pointer that requires resolution |
| **Representation** | Encoding/serialization of the artifact |

**Implications**:
- URI ≠ Identity (URI is one type of identifier)
- Name ≠ Identifier (names can collide, change)
- Same name does NOT mean same concept
- Different names does NOT mean different concept

---

## Principle 5 — Contextual Semantics

> **Meaning and applicability may depend upon context.**

```
Capability
   + Business Context → Business Capability
   + Operational Context → Operational Capability
   + Technical Context → Technical Capability
```

**Implications**:
- Context qualifies interpretation, not replaces it
- Contextual Assertion ≠ Contextual Concept
- A concept can be universal while its application is contextual

---

## Principle 6 — Assertion Separation

> **A Proposition shall remain distinguishable from an Assertion of that Proposition.**

```
Proposition:  Capability enables Function    (about the model)
Assertion:    OTCHERE Inc possesses Capability X    (about reality)
```

**Implications**:
- WSF needs to distinguish Foundational Semantic Assertion from Domain/Enterprise Assertion
- Validation ≠ Truth
- An assertion can be valid structurally but false semantically

---

## Principle 7 — Provenance

> **Authoritative semantic claims shall be traceable to their provenance.**

```
Assertion
   │
   ├── Source
   ├── Agent
   ├── Activity
   ├── Time
   ├── Method
   └── Derivation
```

**Implications**:
- Every authoritative claim must have provenance
- Provenance must be retained even when artifacts change
- Provenance ≠ Evidence (they are distinct)

---

## Principle 8 — Temporal Integrity

> **Truth, validity, currency, applicability, and lifecycle status shall not be conflated.**

```
Truth        → Does the proposition correspond to reality?
Validity     → Does the assertion apply under specified conditions?
Currency     → Is the assertion currently in effect?
Applicability → Does the assertion apply in this scope?
Lifecycle    → What is the governance status?
```

**Implications**:
- An assertion can be historically true but currently invalid
- Lifecycle status belongs to governance, not to Truth
- WSF must distinguish Temporal Semantic Validity from Lifecycle Status

---

## Principle 9 — Relationship First-Classness

> **Relationships shall be representable as first-class semantic constructs.**

Relationships are not merely implementation connectors. They carry semantic meaning.

**4 Forms of Relation**:
- **Structural** — Entity related-to Entity
- **Temporal** — Event A precedes Event B
- **Causal** — Event A causes Event B
- **Dispositional** — Capability enables Activity

**Implications**:
- Relationships have identity
- Relationships can have properties (relationship reification)
- Domain-specific relationships specialize the general mechanism

---

## Principle 10 — Lifecycle Independence

> **Downstream semantic systems shall retain their own governance and lifecycle.**

```
WSF ≠ OpenDEA ≠ Assessment-Models
```

**Implications**:
- WSF does NOT become the governance home for OpenDEA
- WSF does NOT become the assessment governance authority
- Each system has its own ADRs, CRs, and versioning
- Interaction through governed semantic interfaces, not absorption

---

## Principle 11 — Evidence-Based Evolution

> **Foundational semantic changes require explicit investigation and recorded rationale.**

```
Investigation
   ↓
Finding
   ↓
Synthesis
   ↓
ADR
   ↓
CR
   ↓
Implementation
   ↓
Validation
   ↓
Release
```

**Implications**:
- No implementation is interpreted as automatically creating a normative semantic decision
- Changes must be traceable to investigations
- Investigation record is preserved as a first-class asset

---

## Principle 12 — Open Specialization

> **WSF shall enable specialization without attempting to own every domain ontology.**

WSF provides the semantic space from which specialized concepts can be rigorously derived. WSF does NOT need to know every specialized form.

**Implications**:
- Domain ontologies extend WSF, not the reverse
- Specialization is encouraged
- WSF stays minimal and focused
- Downstream systems retain autonomy

---

## Summary Table

| # | Principle | Key Phrase |
|---|---|---|
| 1 | Semantic Primacy | Meaning precedes representation |
| 2 | Minimal Foundation | Smallest sufficient vocabulary |
| 3 | Explicit Specialization | Specialize, don't redefine |
| 4 | Identity Separation | Identity ≠ Identifier ≠ Name ≠ Reference ≠ Representation |
| 5 | Contextual Semantics | Meaning may depend on context |
| 6 | Assertion Separation | Proposition ≠ Assertion |
| 7 | Provenance | Authoritative claims traceable |
| 8 | Temporal Integrity | Truth ≠ Validity ≠ Currency ≠ Lifecycle |
| 9 | Relationship First-Classness | Relationships are semantic constructs |
| 10 | Lifecycle Independence | WSF ≠ OpenDEA ≠ Assessment-Models |
| 11 | Evidence-Based Evolution | Investigation → ADR → CR → Implementation |
| 12 | Open Specialization | Enable, don't own |

---

*These 12 principles are the governance foundation of WSF. Any deviation must be explicitly justified through the ADR process documented in `wsf-governance/`.*
