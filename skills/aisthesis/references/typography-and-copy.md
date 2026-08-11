# Typography and interface copy

## Typography is part of the information architecture

1. Inventory the content: display statements, section titles, body, labels, data, code and annotations.
2. Choose type roles before fonts. A role defines tone, density, weight range, case and behavior.
3. Select the smallest family set that can express those roles. One variable family plus a mono face is often enough; contrast must be intentional when using more.
4. Define a fluid scale with bounded `clamp()` values. Test long words, localization, browser zoom and narrow containers.
5. Set body measure deliberately: usually 45–75 characters depending on type and context. Dense operational UI may be shorter; long-form reading should not span the viewport.
6. Set line height from actual glyphs and measure, not a universal number. Check ascenders, diacritics, code and multiline links.
7. Load only required subsets and weights, use `font-display`, and verify fallback metrics do not create disruptive shift.

## Type proof

Render one page containing:

- every heading level;
- paragraphs at short and long measures;
- mixed case, numerals, punctuation and diacritics;
- links, buttons, labels, helper text, errors and disabled text;
- tabular values and code;
- the longest realistic title and translated expansion where relevant;
- 200% and 400% zoom states.

Reject a type system that needs per-page exceptions to remain legible.

## Interface language

Use the user's vocabulary, not the implementation's. Keep one term for each object and action across navigation, headings, buttons, errors and help.

### Action labels

- Name the outcome: `Create report`, `Save permissions`, `Retry upload`.
- Distinguish destructive actions from dismissal: `Delete key` versus `Cancel`.
- Avoid `Submit`, `OK`, `Yes` and `Continue` where the result can be named.
- Match labels to actual scope: a button that publishes must not say `Save`.

### Status and feedback

Every async operation needs a perceivable start, progress or pending state, completion, failure and retry/recovery path. Preserve the user's input after failure unless security requires otherwise.

### Empty states

Explain:

1. what belongs here;
2. why it is empty;
3. the next available action;
4. any permission or filtering condition that caused the state.

Do not use empty states as decorative marketing inside operational tools.

### Errors

- Place field errors next to the field and summarize when several exist.
- State what happened, what remains safe, and one recovery action.
- Preserve stable identifiers for support without exposing internals or secrets.
- Announce dynamic errors through an appropriate live region and move focus only when necessary.

### Confirmation and destructive work

Use confirmation when the cost is high or the action is surprising, not for every change. Name the object and consequence. Prefer undo for fast reversible actions.

## Copy QA

Search the rendered product for:

- inconsistent object names;
- placeholder text and lorem ipsum;
- implementation language, unexplained acronyms and passive ambiguity;
- title case used as decoration rather than convention;
- punctuation drift;
- truncated labels and clipped localization;
- generic AI language such as “unlock,” “seamless,” “revolutionary,” or claims with no evidence;
- promises the product cannot substantiate.

Copy acceptance belongs to the same state matrix as visual and functional acceptance.