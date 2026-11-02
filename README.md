# WSF Documentation

> **Conceptual, tutorial, and implementation documentation for WSF.**

This repository (`wsf-docs/`) contains human-readable documentation that makes WSF accessible to architects, developers, modelers, and stakeholders.

---

## Repository Structure

```
wsf-docs/
├── README.md (this file)
├── conceptual/        ← Conceptual documentation (what WSF is, why)
├── implementation/    ← Implementation documentation (how to use WSF)
├── tutorials/         ← Step-by-step guides
├── conformance/       ← Conformance documentation
└── glossary/          ← Term definitions
```

---

## Conceptual Documentation (`conceptual/`)

For architects, decision-makers, and those new to WSF:

- **FOUNDATIONAL-PRINCIPLES.md** : The 12 Foundational Principles
- **WSF-OVERVIEW.md** : What WSF is, why it exists (to be added)
- **SEMANTIC-MODEL.md** : The 3-Foundation WSF model (to be added)
- **EXAMPLE-CONVENTION.md** : OTCHERE/Kwesi canonical example (to be added)
- **DISTINCTIONS.md** : 12 epistemic distinctions (to be added)

---

## Implementation Documentation (`implementation/`)

For developers and integrators:

- **WSF-API-GUIDE.md** (to be added : after Engine implementation)
- **INTEGRATION-GUIDE.md** (to be added)
- **NAMESPACE-GUIDE.md** (to be added : after ADR-WSF-21)
- **IDENTITY-GUIDE.md** (to be added : after ADR-WSF-18)

---

## Tutorials (`tutorials/`)

Step-by-step learning resources:

- **MODELING-YOUR-FIRST-ENTITY.md** (to be added)
- **CREATING-YOUR-FIRST-CAPABILITY.md** (to be added)
- **BUILDING-A-DIGITAL-TWIN.md** (to be added)
- **SIMULATING-A-PROCESS.md** (to be added)

---

## Conformance Documentation (`conformance/`)

How to claim WSF conformance:

- **CONFORMANCE-OVERVIEW.md** (to be added : after ADR)
- **SEMANTIC-CONFORMANCE.md** (to be added)
- **IDENTITY-CONFORMANCE.md** (to be added)
- **REFERENCE-CONFORMANCE.md** (to be added)
- **RELATIONSHIP-CONFORMANCE.md** (to be added)
- **ASSERTION-CONFORMANCE.md** (to be added)
- **PROVENANCE-CONFORMANCE.md** (to be added)
- **SPECIALIZATION-CONFORMANCE.md** (to be added)
- **API-CONFORMANCE.md** (to be added : after Engine)
- **SERIALIZATION-CONFORMANCE.md** (to be added)

---

## Glossary (`glossary/`)

Term definitions for WSF vocabulary:

- **GLOSSARY.md** (to be added)
- **12-EPITEMIC-DISTINCTIONS.md** (to be added)
- **4-FORMS-OF-RELATION.md** (to be added)
- **9-CATEGORY-TAXONOMY.md** (to be added)
- **3-FOUNDATION-MODEL.md** (to be added)

---

## Example Convention

All examples in WSF docs use:

- **Enterprise**: OTCHERE Inc (or OTCHERE)
- **Individual**: Kwesi
- **System**: OTCHERE DC-01

**ACME is prohibited.**

---

## Documentation Standards

Per CR-WSF-17 Rev.1 §6, documentation shall distinguish:

- **Investigation Finding** : Research observation
- **Architectural Decision** : Formal ADR position
- **Implementation** : Executed work

These categories shall NOT be conflated in documentation.

---

## Status

This repository is being established per CR-WSF-17 Rev.1. **Most documentation is placeholders awaiting subsequent ADRs and implementation work.**

The **FOUNDATIONAL-PRINCIPLES.md** document has been completed as the foundational reference.

---

## Related Repositories

- [wsf/](../wsf/) : Canonical semantic assets
- [wsf-spec/](../wsf-spec/) : Normative specifications
- [wsf-governance/](../wsf-governance/) : ADRs, CRs, investigation record
- [wsf-examples/](../wsf-examples/) : Reference applications

---

*Documentation makes WSF accessible. New documentation requires explicit decision through the ADR process.*


---

## Concept Reference Site

`scripts/build-site.py` generates a static concept reference site (one page per concept in `wsf/concepts/`, plus tutorials and the foundational principles) into `_site/`. The [Site workflow](./.github/workflows/site.yml) builds it on every push and PR (sibling checkout of `wsf` required) and publishes it to GitHub Pages from `main`.

Run locally with the `wsf` repository checked out as a sibling:

```bash
python3 scripts/build-site.py
```
