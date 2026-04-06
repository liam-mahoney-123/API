# PDP Conversion Implementation Backlog (Initial)

## Priority legend

- **P0** = Required for first launch slice
- **P1** = High value follow-on
- **P2** = Optimization / experimentation

## Workstream A: PDP Media

### A1 (P0) Build upgraded media gallery module
- Implement gallery supporting mixed media types (image/video) with lazy loading.
- Add desktop hover zoom and mobile pinch zoom.
- Add media labeling taxonomy (`size`, `in_use`, `detail`, `included`).
- **Dependencies:** product media metadata availability.
- **Definition of done:**
  - Gallery handles at least 8 media assets without layout shift.
  - Accessibility checks pass for keyboard and screen readers.

### A2 (P1) Media quality guardrails in content pipeline
- Add validation for minimum required image set by category.
- Block publish or warn when required views are missing.
- **Dependencies:** category policy configuration.

## Workstream B: Specifications

### B1 (P0) Introduce quick specs strip
- Render 3-6 key specs in hero-adjacent region.
- Support configurable spec priority by category.
- **Dependencies:** canonical spec keys.

### B2 (P0) Build structured full specs table
- Group specs by category with mobile collapse behavior.
- Add explicit missing-value handling (`Not specified`).
- **Dependencies:** structured spec payload.

### B3 (P1) Compare-ready spec normalization
- Normalize units and add locale conversion helpers.
- Add client util for shared compare/spec rendering logic.

## Workstream C: Reviews and Q&A

### C1 (P0) Add trust summary module
- Display rating average, review count, and verification indicator.
- Ensure summary appears high on PDP.

### C2 (P0) Add review sort/filter controls
- Implement sorting and facet filtering with URL state persistence.
- Add searchable reviews input (client-side first-pass).

### C3 (P1) Q&A interaction enhancements
- Add search, helpful voting, and manufacturer-answer badge.
- Add abuse mitigation and basic moderation hooks.

## Workstream D: Compare Tool

### D1 (P0) Add compare selection and sticky tray
- Add compare checkbox on PDP and related-item cards.
- Persist compare state during session navigation.

### D2 (P0) Build compare table
- Render at least 2-4 products with core comparable attributes.
- Highlight differences by default.

### D3 (P2) Cross-session compare persistence
- Optionally save compare state for logged-in users.

## Workstream E: Accessories and Related

### E1 (P0) Separate recommendation modules by intent
- Split into `frequently_bought_together`, `compatible_accessories`, `alternatives`.
- Render compatibility badges where data exists.

### E2 (P0) Add quick-add UX for recommendations
- Inline add-to-cart from cards with explicit success/error states.
- Add reversibility (undo/remove).

### E3 (P1) Recommendation explanation and confidence
- Show "why recommended" rationale and compatibility confidence.

## Workstream F: Compliance Messaging

### F1 (P0) Add layered compliance surfaces
- Inline critical notice near CTA, plus detailed expandable section.
- Respect severity levels (`info`, `warning`, `blocking`).

### F2 (P0) Enforce blocking compliance logic
- Disable add-to-cart when blocking conditions are met.
- Provide user-readable reason and next-best action.

### F3 (P1) Region-aware compliance
- Resolve notices by locale/market and variant where applicable.

## Workstream G: Measurement

### G1 (P0) Instrument core PDP events
- Implement events listed in `pdp-conversion-draft.md`.
- Ensure event schema validation and payload consistency.

### G2 (P1) Build conversion diagnostics dashboard
- Add module-level funnel metrics (impression -> interaction -> ATC).
- Track uplift by category and device segment.

## Suggested release slicing

### Release slice 1 (MVP)
- A1, B1, B2, C1, C2, D1, D2, E1, E2, F1, F2, G1

### Release slice 2
- A2, B3, C3, E3, F3, G2

### Release slice 3 (experimentation)
- D3 + A/B test variants for:
  - review summary placement
  - compare call-to-action copy
  - compliance message style
