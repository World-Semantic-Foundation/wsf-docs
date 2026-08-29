# Tutorial 2 : The 9 Tier 2 Supporting Constructs

> **A step-by-step tutorial covering the 9 Tier 2 supporting constructs that operationalise the Tier 1 foundations.**

## Learning Objectives

By the end of this tutorial, you will understand:

1. Why Tier 2 constructs are needed alongside Tier 1
2. Each of the 9 Tier 2 constructs and their role
3. How Tier 2 supports governance, provenance, and interoperability
4. How to apply Tier 2 constructs in OTCHERE Inc scenarios

## Prerequisites

- Completion of [Tutorial 1 : Tier 1 Foundations](./tutorial-01-tier-1-foundations.md)
- Familiarity with the 12 Tier 1 concepts

## Part 1 : Why Tier 2?

Tier 1 concepts define **what exists** (Entity, Concept, Relationship, etc.). But to operationalise these concepts in real systems, we need supporting constructs that handle:

- **Identification** : Stable, persistent references to concepts (Identifier, Namespace)
- **Definition** : Formal, normative specifications of meaning (Term, Definition)
- **Validation** : Time-bounded, rule-checked conformance (Validity)
- **Trust** : Evidence and provenance for claims (Evidence, Provenance, Authority)

These 9 constructs form the supporting layer that makes Tier 1 concepts **actionable** in knowledge systems.

## Part 2 : The 9 Tier 2 Constructs

### 2.1 : Identifier

`wsf:Identifier` is a stable, persistent, machine-readable label that uniquely references a single concept across all representations, contexts, and time.

In OTCHERE Inc:
- **`wsf:Entity`** : the CURIE-form identifier for the Entity concept
- **`wsf:Kwesi`** : the identifier for the Kwesi actor
- **`schema:Organization`** : the Schema.org CURIE for organisations

Identifiers use the CURIE syntax: `prefix:LocalName`. Common prefixes: `wsf`, `schema`, `skos`, `tmforum`, `opendea`.

### 2.2 : Reference

`wsf:Reference` is a directed, typed association from one concept to another, expressing a navigable semantic relationship that supports both graph traversal and targeted lookup.

In OTCHERE Inc:
- **`wsf:Kwesi`** `references` **`wsf:OTCHERE-Inc`** (via employment reference)
- **`wsf:Order-Fulfillment-Capability`** `references` **`wsf:Process`**

References are typed (using the 12 relationship kinds) and support graph traversal.

### 2.3 : Namespace

`wsf:Namespace` is a governed administrative scope that groups related identifiers under a common authority, enabling prefix-based shorthand (CURIE) and federation across independent semantic ecosystems.

In OTCHERE Inc, the namespaces are:
- **`wsf`** : World Semantic Foundation
- **`schema`** : Schema.org Community
- **`skos`** : W3C Simple Knowledge Organization System
- **`tmforum`** : TM Forum
- **`opendea`** : OpenDEA Consortium

Each namespace has a registered authority and IRIs for its terms.

### 2.4 : Term

`wsf:Term` is a human-readable, language-bound linguistic label that designates a concept in natural language use, distinct from the concept's identifier and definition.

In OTCHERE Inc:
- The English term for `wsf:Entity` is "Entity"
- The French term might be "Entité"
- The Twi term might be "Nnoba"

Terms are language-bound and may vary across languages; the underlying concept is universal.

### 2.5 : Definition

`wsf:Definition` is a formal, normative specification of a concept's meaning, expressed as a structured prose statement that establishes necessary and sufficient conditions for concept application.

In WSF:
- The definition of `wsf:Entity` is "Anything that exists, has identity, and can be referenced."
- The definition of `wsf:Capability` is "The middle-layer chain: Entity : Role : Capacity : Ability : Capability : Function : Outcome : Value."

Definitions are normative (authoritative) and structured (testable).

### 2.6 : Validity

`wsf:Validity` is the state of an assertion, representation, or semantic construct conforming to its governing rules at a point in time. It is a time-bounded, evaluable property distinct from truth.

In OTCHERE Inc:
- An assertion "Kwesi is employed by OTCHERE Inc" is valid from 2024-01-01 to 2026-12-31
- After Kwesi leaves, the assertion becomes invalid (status: expired)

Validity has a status enum: active, suspended, expired, revoked.

### 2.7 : Evidence

`wsf:Evidence` is a referenceable artifact (observation, document, measurement, or other empirical input) that supports the truth claim underlying an assertion.

In OTCHERE Inc, evidence for the assertion "Kwesi is an Enterprise Architect" includes:
- HR records (document)
- Architecture responsibility assignment (observation)
- KWESI's signed employment contract (document)
- Architecture decision records authored by Kwesi (derivation)

Evidence types: document, observation, measurement, expert_judgement, derivation.

### 2.8 : Provenance

`wsf:Provenance` is the complete, traceable record of how an assertion came to be: who created it, when, under what authority, with what evidence, and through what derivation chain.

Provenance for every assertion in WSF includes:
- **Actor** : Who made the assertion (e.g., Kwesi)
- **Authority** : Under whose authority (e.g., OTCHERE Architecture Board)
- **Timestamp** : When the assertion was made
- **Method** : How it was derived
- **Derived from** : Source assertions or data

Provenance enables audit trails and trust chains.

### 2.9 : Authority

`wsf:Authority` is the recognised right and capability of an entity to make, modify, validate, or retire semantic assertions within a specified domain, under governed rules.

In OTCHERE Inc, the authorities include:
- **OTCHERE Architecture Board** : authority over architecture assertions
- **OTCHERE HR Department** : authority over employment assertions
- **OTCHERE DPO** : authority over data privacy assertions

Authorities govern who can make which assertions in which domains.

## Part 3 : The Tier 2 Pattern

All 9 Tier 2 constructs follow a common pattern:

1. **Stable reference** (Identifier + Namespace) : uniquely identifies the concept
2. **Human label** (Term) : how humans refer to it
3. **Formal definition** (Definition) : what it means
4. **Time-bounded** (Validity) : when it applies
5. **Evidence-based** (Evidence) : supporting artifacts
6. **Tracked** (Provenance) : who, when, how
7. **Governed** (Authority) : who controls it
8. **Connected** (Reference) : to other concepts

This pattern ensures every Tier 1 concept can be operationalised in real systems.

## Part 4 : Hands-On Exercise

For the OTCHERE Inc canonical example, identify:

1. The Identifier for OTCHERE Inc
2. The Namespace in which OTCHERE Inc's identifier lives
3. The Term (human label) for OTCHERE Inc in English
4. The Definition of OTCHERE Inc (as an organisation)
5. The Validity period of OTCHERE Inc (when it was founded to now)
6. Evidence for OTCHERE Inc's existence
7. Provenance of the canonical enterprise description
8. The Authority that maintains the OTCHERE Inc description

## Next Tutorial

[Tutorial 3 : The 16 Tier 3 Specialisation Concepts](./tutorial-03-tier-3-specialisations.md) — covers Role, Process, Function, Activity, Outcome, Resource, System, Organisation, Service, Goal, Policy, Rule, Constraint, Objective, Measure, and Actor.

## Cross-References

- [Tutorial 1 : Tier 1 Foundations](./tutorial-01-tier-1-foundations.md)
- [Tier 2 Concepts Catalog](../wsf/concepts/) : Identifier, Reference, Namespace, Term, Definition, Validity, Evidence, Provenance, Authority
- [12 Foundational Principles](../conceptual/FOUNDATIONAL-PRINCIPLES.md)

---

*Tutorials series. Status: Baseline.*