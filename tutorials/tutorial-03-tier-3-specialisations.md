# Tutorial 3 : The 16 Tier 3 Specialisation Concepts

> **A step-by-step tutorial covering the 16 Tier 3 specialisation concepts through the OTCHERE Inc enterprise context.**

## Learning Objectives

By the end of this tutorial, you will understand:

1. Why Tier 3 concepts are needed (and when to use them)
2. Each of the 16 Tier 3 concepts
3. The middle-layer capability chain
4. How Tier 3 concepts apply to OTCHERE Inc

## Prerequisites

- Completion of [Tutorial 1](./tutorial-01-tier-1-foundations.md) and [Tutorial 2](./tutorial-02-tier-2-supporting-constructs.md)
- Familiarity with the 12 Tier 1 concepts and 9 Tier 2 constructs

## Part 1 : Why Tier 3?

Tier 1 and Tier 2 cover the abstract foundation. Tier 3 covers the **specific kinds of things** that exist in real enterprises. The 16 Tier 3 concepts are:

- Common across most enterprises (not domain-specific)
- Specialisations of Tier 1 concepts
- Useful for analysing concrete entities (people, organisations, systems, processes)

Without Tier 3, real-world scenarios would be modelled at the abstract Tier 1 level only, missing the specificity needed for actionable analysis.

## Part 2 : The 16 Tier 3 Concepts

### 2.1 : Role

`wsf:Role` is a contextualised identity that an Entity assumes within a specific context, defining the Entity's expected behaviour, responsibilities, and relationships.

**OTCHERE Example** : Kwesi holds the **Enterprise Architect Role** within OTCHERE Inc. The role carries expectations (design semantic models) and rights (approve architecture decisions).

### 2.2 : Process

`wsf:Process` is a structured, repeatable, ordered sequence of Activities that transforms inputs into outputs according to defined rules.

**OTCHERE Example** : The **Order Fulfillment Process** has stages (Order Received, Payment Confirmed, Inventory Allocated, Order Picked, Order Shipped, Delivery Confirmed). Each execution is an Event; each stage is an Activity.

### 2.3 : Function

`wsf:Function` is a purposeful kind of Activity enabled by Capability.

**OTCHERE Example** : **Order Fulfillment Function** is the kind of work that the Order Fulfillment Capability enables. Individual Activities instance this Function.

### 2.4 : Activity

`wsf:Activity` is an actual occurrence of a Function by an Entity at a specific time.

**OTCHERE Example** : **Order #12345 fulfillment on 2026-08-29** is a specific Activity. It has a timestamp, executor (OTCHERE OMS), inputs (order details), and outputs (delivery confirmation).

### 2.5 : Outcome

`wsf:Outcome` is the result produced by an Activity or Process.

**OTCHERE Example** : **Order #12345 delivered on 2026-08-30** is the Outcome of the Order Fulfillment Process. The Outcome is measurable (delivery time, accuracy).

### 2.6 : Resource

`wsf:Resource` is an Entity consumed, used, or produced by an Activity or Process.

**OTCHERE Example** : **OTCHERE DC-01** is a Resource consumed by digital Processes. **Order #12345** is a Resource produced by the Order Fulfillment Process.

### 2.7 : System

`wsf:System` is an Entity composed of interacting Components with defined Functions, Boundaries, and Interfaces.

**OTCHERE Example** : **OTCHERE DC-01** is a System composed of compute, storage, and networking Components. The System has internal structure and external interfaces.

### 2.8 : Organisation

`wsf:Organisation` is an Entity composed of multiple Actors pursuing shared Goals through coordinated Activities, with defined Roles, Authorities, and Processes.

**OTCHERE Example** : **OTCHERE Inc** is an Organisation composed of Actors (employees, contractors, customers), with Roles (Employer, Employee), Authorities (Architecture Board), and Goals (Order Fulfillment Excellence).

### 2.9 : Service

`wsf:Service` is a Function exposed by an Entity for consumption by other Entities, with defined Interfaces, SLAs, and operational characteristics.

**OTCHERE Example** : **OTCHERE Order Fulfillment Service** is an exposed Function with API, SLA (24-hour fulfillment), and operational characteristics.

### 2.10 : Goal

`wsf:Goal` is a desired Outcome expressed as a Proposition, defining a target State that an Entity intends to reach through Activities and Resource allocation.

**OTCHERE Example** : **OTCHERE Inc Goal: 99% on-time order delivery** is a Goal evaluated against actual Outcomes.

### 2.11 : Policy

`wsf:Policy` is a Rule governing Entity behaviour within an Organisation, expressing Goals, Constraints, and Authorities in actionable form.

**OTCHERE Example** : **OTCHERE Data Privacy Policy** expresses the Goal (privacy protection) as actionable Constraints (data minimisation, retention limits) and Authorities (DPO authority).

### 2.12 : Rule

`wsf:Rule` is a normative Constraint on Entity behaviour or State, expressed as a logical condition.

**OTCHERE Example** : **Rule: Orders over $10,000 require manager approval** has logical form (when/then), is machine-evaluable, and carries consequences.

### 2.13 : Constraint

`wsf:Constraint` is a limiting condition on an Entity, Activity, or State.

**OTCHERE Example** : **OTCHERE warehouse capacity constraint: max 50,000 SKUs** constrains inventory storage.

### 2.14 : Objective

`wsf:Objective` is a Goal with explicit success criteria and time-bound target.

**OTCHERE Example** : **OTCHERE Q3 2026 Objective: ship 95% of orders within 24 hours** is an Objective with measurable success criteria and time bound.

### 2.15 : Measure

`wsf:Measure` is a Proposition expressing a quantitative or qualitative observation of an Entity, Activity, or State.

**OTCHERE Example** : **OTCHERE Order Fulfillment Latency Measure: average time from order receipt to delivery** is a Measure with units (hours), method (timestamp diff), and aggregation (mean).

### 2.16 : Actor

`wsf:Actor` is an Entity that performs Activities, makes Assertions, or bears Responsibilities.

**OTCHERE Example** : **Kwesi** is an Actor (individual) at OTCHERE Inc, holding Roles and performing Activities.

## Part 3 : The Middle-Layer Capability Chain

The most important Tier 3 chain is the **middle-layer capability chain**:

```
Entity → Role → Capacity → Ability → Capability → Function → Outcome → Value
```

This chain is the operational core of capability modelling:

1. **Entity** : The entity (person, organisation, system)
2. **Role** : The role the entity holds
3. **Capacity** : The broad area in which the entity operates
4. **Ability** : A specific capability within the capacity
5. **Capability** : A demonstrated competence
6. **Function** : The kind of work the capability enables
7. **Outcome** : The result of performing the function
8. **Value** : The worth of the outcome

In OTCHERE Inc:
- Kwesi (Entity) holds Enterprise Architect Role
- In Enterprise Architecture capacity
- With Architecture Design ability
- Possessing Architecture Capability
- Enabling Design Function
- Producing Architecture Outcomes
- Creating Business Value

## Part 4 : Inheritance Patterns

The 16 Tier 3 concepts specialise Tier 1 concepts as follows:

| Tier 3 | Specialises |
|---|---|
| Role, Resource, System, Organisation, Actor | Entity |
| Process, Activity | Event |
| Outcome | State |
| Function, Capability | Disposition |
| Service | Function |
| Goal, Constraint, Measure | Proposition |
| Rule | Constraint |
| Policy | Rule |
| Objective | Goal |

This inheritance is reflected in the [concept hierarchy diagram](../wsf-visuals/conceptual/concept-hierarchy.md).

## Part 5 : Hands-On Exercise

For the OTCHERE Order Fulfillment scenario, model:

1. The Order Fulfillment **Process** and its 5 stages
2. The Order Fulfillment **Capability** that enables it
3. A specific **Activity** (Order #12345)
4. The **Outcome** of that Activity
5. The **Measure** that evaluates the Outcome against the Goal
6. The **Actor** responsible for the Activity

## Next Tutorial

[Tutorial 4 : Building Your First WSF Knowledge Graph](./tutorial-04-first-knowledge-graph.md) — hands-on with the WSF Semantic Engine.

## Cross-References

- [Tutorial 1 : Tier 1 Foundations](./tutorial-01-tier-1-foundations.md)
- [Tutorial 2 : Tier 2 Supporting Constructs](./tutorial-02-tier-2-supporting-constructs.md)
- [Tier 3 Concepts Catalog](../wsf/concepts/)
- [Capability Tier 3 Example](../wsf/concepts/capability.md)

---

*Tutorials series. Status: Baseline.*