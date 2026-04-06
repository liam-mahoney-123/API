# PDP Conversion Improvement Draft (First Pass)

## Objective

Increase product detail page conversion by reducing decision friction and increasing trust:

- Make product suitability obvious in under 10 seconds
- Reduce uncertainty before add-to-cart
- Keep key compliance requirements visible without overwhelming the page

## Core PDP Information Architecture

Recommended module order (top to bottom):

1. **Primary purchase block (hero)**
   - Title, key variant selectors, price, stock, shipping, primary CTA
2. **Image and media gallery**
   - Zoom, alternate angles, context-of-use, short demo media
3. **Highlights + quick specs**
   - 4-6 scannable value bullets and critical specs snapshot
4. **Detailed specifications**
   - Structured, grouped specification table with "compare-friendly" fields
5. **Reviews and Q&A**
   - Rating summary, review facets, searchable Q&A
6. **Comparison tool entry**
   - Compare this product to similar alternatives
7. **Accessories and related items**
   - Compatibility-first cross-sell and substitute recommendations
8. **Compliance and safety messaging**
   - Surface high-impact compliance notices inline; full legal details expandable

---

## 1) Product Images and Media

### UX draft

- Use a sticky media rail on desktop and swipe gallery on mobile.
- Require image set coverage:
  - Front
  - Side/back
  - Scale/context shot
  - Key feature close-up(s)
  - Packaging/what's-in-box
- Add labeled media chips:
  - `Size`
  - `In use`
  - `Detail`
  - `What's included`
- Add optional short clip (10-30s) with muted autoplay only when in viewport.
- Support hover zoom (desktop) and pinch zoom (mobile) with clear loading states.

### Conversion rationale

- Better visual proof reduces hesitation and return risk.
- Labeled views reduce time spent hunting for key details.

### Acceptance criteria

- Gallery supports at least 8 media items with lazy loading.
- Every item has alt text and media type metadata.
- Zoom interactions keep frame rate and do not block CTA rendering.

### Events to instrument

- `pdp_media_viewed` (media_id, media_type, label)
- `pdp_zoom_used` (media_id, input_type)
- `pdp_video_played` (media_id, play_duration_seconds)

---

## 2) Detailed Specifications

### UX draft

- Add a two-tier spec experience:
  1. **Quick specs strip** near top (3-6 critical decision specs)
  2. **Full specs table** lower on page, grouped by category:
     - Dimensions
     - Performance
     - Materials
     - Compatibility
     - Warranty
- Include "copy spec" and "compare spec" affordances for high-intent users.
- Normalize units and add locale-aware conversions where relevant.

### Conversion rationale

- Shallow + deep spec access supports both quick and technical buyers.
- Structured specs enable reliable product comparison and reduced support load.

### Acceptance criteria

- Full specs render from structured key/value source (not unstructured HTML blobs only).
- Missing values are handled explicitly (e.g., `Not specified`).
- Spec categories are collapsible on mobile.

### Events to instrument

- `pdp_quick_specs_interaction` (spec_key, action)
- `pdp_full_specs_expanded` (category)
- `pdp_specs_copy_clicked` (spec_key)

---

## 3) Reviews and Q&A

### UX draft

- Display trust summary block:
  - Average rating
  - Number of reviews
  - Verified purchase % (if available)
  - Common pros/cons tags
- Add review controls:
  - Sort (most helpful, recent, highest, lowest)
  - Filter by rating and topic facets
  - Search within reviews
- Q&A section:
  - Search existing questions
  - Upvote useful answers
  - Mark "manufacturer answered"
- Add "Was this review helpful?" interactions with abuse throttling.

### Conversion rationale

- Better social proof and answer discovery reduces unresolved objections.

### Acceptance criteria

- Rating summary and review count appear above fold on desktop and near hero on mobile.
- Q&A search returns results client-side for first-pass data and server-side when API supports it.
- Reviews section degrades gracefully when no reviews exist.

### Events to instrument

- `pdp_reviews_filter_applied` (filter_type, value)
- `pdp_review_helpful_clicked` (review_id, vote)
- `pdp_qa_search` (query_length, result_count)
- `pdp_qa_submit_initiated` (has_existing_answer)

---

## 4) Comparison Tools

### UX draft

- Add "Compare" checkbox near title/price and in related-item cards.
- Sticky compare tray appears once at least one product is selected.
- Minimum viable compare table includes:
  - Price
  - Dimensions
  - Compatibility
  - Core performance metrics
  - Warranty
- Highlight differences by default and allow "show all specs" toggle.

### Conversion rationale

- Prevents off-site comparison journeys and keeps decisioning inside funnel.

### Acceptance criteria

- Compare selection persists across PDP/PLP navigation in current session.
- Compare table supports at least 4 products.
- Empty or unavailable spec cells are clearly indicated.

### Events to instrument

- `pdp_compare_add` (product_id, source_module)
- `pdp_compare_remove` (product_id)
- `pdp_compare_viewed` (product_count)
- `pdp_compare_difference_toggle` (enabled)

---

## 5) Accessories and Related Items

### UX draft

- Split recommendations into explicit modules:
  - **Frequently bought together** (bundle-first)
  - **Compatible accessories** (compatibility-validated)
  - **Alternative products** (substitutes if undecided)
- Surface compatibility badges:
  - `Guaranteed fit`
  - `Check size/model`
- Provide quick-add actions with inline variant pickers where required.
- For alternatives, show "Why consider this" one-liner.

### Conversion rationale

- Increases order value while preserving trust through fit clarity.
- Alternative recommendations reduce bounce when product confidence is low.

### Acceptance criteria

- Recommendation modules are independently configurable.
- Accessories module only shows compatibility-safe items when compatibility data exists.
- Quick-add success/failure states are explicit and reversible.

### Events to instrument

- `pdp_accessory_impression` (module, product_id, position)
- `pdp_accessory_quick_add` (module, product_id, success)
- `pdp_alternative_clicked` (product_id, reason_code)

---

## 6) Compliance Messaging

### UX draft

- Use layered compliance messaging:
  1. **Inline critical notices** near price/CTA (high impact only)
  2. **Section-level notices** inside specs/compliance module
  3. **Expandable legal details** for full policy text
- Show region-aware compliance when locale/market is known.
- Add icon + plain-language summary before legal text.
- Keep irreversible constraints near CTA (e.g., restricted shipping).

### Conversion rationale

- Prevents late-stage checkout surprises and compliance friction.
- Improves trust by presenting constraints clearly and early.

### Acceptance criteria

- Critical notices render without blocking add-to-cart flow when non-fatal.
- Fatal restrictions clearly disable CTA with explanatory message and fallback path.
- Compliance data has source attribution and last-updated metadata.

### Events to instrument

- `pdp_compliance_notice_viewed` (notice_type, severity)
- `pdp_compliance_expand_clicked` (notice_id)
- `pdp_compliance_blocked_atc` (reason_code)

---

## MVP vs Follow-on

### MVP slice

- Gallery upgrades (labels + zoom + required image set support)
- Quick specs + grouped full specs table
- Reviews summary + basic filters + Q&A search
- Compare tray with 2-4 products
- Compatibility-first accessories
- Critical compliance near CTA

### Follow-on slice

- Video enhancement and richer media analytics
- Advanced review NLP facets
- Dynamic bundle optimization
- Region-specific compliance personalization

---

## Content and Governance Notes

- Product, legal, and merchandising owners should co-own:
  - Required media checklist
  - Canonical spec keys
  - Compliance severity taxonomy
  - Recommendation eligibility rules
- Add a PDP quality gate in publishing workflow so products cannot publish without required critical data for target categories.
