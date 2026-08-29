# Tutorial 1 : WSF Concepts from First Principles

> **A step-by-step tutorial introducing the 38 WSF concepts through the OTCHERE Inc enterprise context.**

This tutorial is the entry point for understanding WSF. It walks through the foundational concepts using a real enterprise scenario.

## Learning Objectives

By the end of this tutorial, you will understand:

1. The 3-tier concept hierarchy (Tier 1, Tier 2, Tier 3)
2. The 6-stage semantic status model
3. The 12 relationship kinds
4. How concepts apply to real-world entities
5. The OTCHERE Inc canonical example

## Prerequisites

- Familiarity with enterprise architecture concepts
- Basic understanding of ontology and knowledge graphs
- No prior WSF knowledge required

## Part 1 : The Tier 1 Foundational Concepts

The 12 Tier 1 concepts form the irreducible foundation of WSF.

### Step 1.1 : Entity

`wsf:Entity` is the most general concept. Anything that exists, has identity, and can be referenced.

In OTCHERE Inc, examples of Entities include:
- **Kwesi** : An individual (a person)
- **OTCHERE Inc** : An organisation
- **OTCHERE DC-01** : A data centre (a physical asset)
- **Order #12345** : An order (an information entity)

All entities have **identity** — they are distinct from other entities.

### Step 1.2 : Concept

`wsf:Concept` is a unit of meaning; a class or category.

Examples in OTCHERE Inc:
- **Customer** : A concept unifying all customers
- **Order** : A concept unifying all orders
- **DataCentre** : A concept unifying all data centres

Concepts unify instances. Kwesi is an instance of the Person concept; OTCHERE Inc is an instance of the Organisation concept.

### Step 1.3 : Relationship

`wsf:Relationship` is a typed association between concepts or entities.

Examples in OTCHERE Inc:
- **Kwesi** `is employed by` **OTCHERE Inc**
- **OTCHERE DC-01** `is operated by` **OTCHERE Inc**
- **Order #12345** `was placed by` **Customer #789**

Relationships are typed (not just "associated with"). The 12 relationship kinds per ADR-WSF-19 cover all needed associations.

### Step 1.4 : Event

`wsf:Event` is an occurrence in time.

Examples:
- **Order Received** event (Order #12345)
- **Payment Confirmed** event
- **Delivery Completed** event

Events have timestamps and participants. They differ from Entities (which persist) in that they occur.

### Step 1.5 : State

`wsf:State` is a condition of an entity at a point in time.

Examples:
- Order is in "Pending" state
- Order is in "Shipped" state
- Order is in "Delivered" state

States are time-bounded observations of an entity's condition.

### Step 1.6 : Disposition

`wsf:Disposition` is an intrinsic tendency or capability of an entity.

Examples:
- OTCHERE Inc has the disposition "Order Fulfillment Capability"
- Kwesi has the disposition "Architecture Design Capability"

Dispositions are what an entity CAN do or IS, as opposed to what it IS DOING (Activity) or HAS (State).

### Step 1.7 : Proposition

`wsf:Proposition` is a statement about concepts or entities.

Example:
- "Kwesi is an Enterprise Architect at OTCHERE Inc" is a Proposition
- "Order Fulfillment is a Capability of OTCHERE Inc" is a Proposition

Propositions are independent of any particular assertion about them.

### Step 1.8 : Assertion

`wsf:Assertion` is a claim about a relationship, with full provenance and evidence.

Example:
- Kwesi asserts: "OTCHERE Inc possesses Order Fulfillment Capability" (Assertion)
- This assertion has provenance (Kwesi made it on date X) and evidence (document Y)

Assertions are the actionable form of propositions. Every assertion has provenance.

### Step 1.9 : Identity

`wsf:Identity` is the persistent self-same-ness of an entity over time.

Examples:
- Kwesi remains Kwesi even as he changes roles, ages, or relocates
- OTCHERE Inc remains OTCHERE Inc even as employees change

Identity is what makes an entity the same entity across time and contexts.

### Step 1.10 : Context

`wsf:Context` is the surrounding circumstances that give meaning to a concept.

Example:
- "Customer" in OTCHERE Inc's context is different from "Customer" in a retail store's context
- The same Role (Employee) has different meanings in different Organisations

Contexts bound and qualify the meaning of concepts.

### Step 1.11 : Time

`wsf:Time` is the dimension along which events are ordered.

Examples:
- Order #12345 received at 2026-08-29T14:30:00Z
- Delivery completed at 2026-08-30T10:15:00Z

Time provides the ordering and duration for events and states.

### Step 1.12 : Space

`wsf:Space` is the dimension in which entities are located.

Examples:
- OTCHERE DC-01 is located in Singapore
- Kwesi is based in Accra

Space provides the location dimension for entities.

## Part 2 : Inheritance Chains

The 12 Tier 1 concepts relate to each other through inheritance and specialisation. See the concept hierarchy diagram in [wsf-visuals/conceptual/concept-hierarchy.md](../wsf-visuals/conceptual/concept-hierarchy.md).

Key inheritance chains:

1. **Entity** is the most general concept; everything specialises it
2. **Concept** specialises Entity (a concept is an entity)
3. **Identity** specialises Entity (identity is an entity)
4. **Disposition** leads to the capability chain (Tier 3 Function, Service, Capability)

## Part 3 : Hands-On Exercise

Using the OTCHERE Inc scenario, identify:

1. 5 Entities in OTCHERE Inc
2. 3 Concepts that unify those entities
3. 2 Relationships between entities
4. 1 Event that occurred recently

Check your answers against the canonical example: [OTCHERE Inc](../wsf-examples/enterprise/otchere-inc.md).

## Next Tutorial

[Tutorial 2 : The 9 Tier 2 Supporting Constructs](./tutorial-02-tier-2-supporting-constructs.md) — covers Identifier, Reference, Namespace, Term, Definition, Validity, Evidence, Provenance, and Authority.

## Cross-References

- [12 Foundational Principles](../conceptual/FOUNDATIONAL-PRINCIPLES.md)
- [Concept Catalog](../wsf/concepts/) : all 38 concepts
- [Concept Hierarchy Diagram](../wsf-visuals/conceptual/concept-hierarchy.md)
- [OTCHERE Inc example](../wsf-examples/enterprise/otchere-inc.md)

---

*Tutorials series. Status: Baseline.*