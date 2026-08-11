# Responsive, state, and accessibility contract

Target **WCAG 2.2 Level AA** unless the product has a stricter legal or contractual requirement. Record the target, browsers, assistive technologies and exceptions before implementation.

## Responsive matrix

Minimum profiles:

- 320 CSS px wide at 400% browser zoom or equivalent reflow;
- 375 and 390/414 mobile widths;
- landscape mobile and short-height desktop;
- 768 tablet/intermediate width;
- 1280 and 1440 desktop;
- one authored ultrawide profile when composition expands;
- 1x and high-DPR media behavior where raster quality matters;
- Day/Night or light/dark themes;
- forced colors;
- reduced motion and reduced data where supported.

At each relevant profile verify no page overflow, text clipping, unreachable controls, crop damage, state loss or hidden recovery paths. Test intermediate widths by resizing continuously; breakpoints are not proof of the space between them.

Responsive art must expose protected regions, focal points, crop rules and a semantic fallback. Verify the selected `<picture>` source from `currentSrc`, intrinsic dimensions and network requests rather than assuming the media query won.

## Success-criterion evidence

Map each finding to a WCAG success criterion when applicable. At minimum evaluate:

- **1.1.1:** text alternatives and decorative-media exclusion;
- **1.3.1/1.3.2:** semantic relationships and meaningful sequence;
- **1.4.3/1.4.11:** text contrast and non-text contrast;
- **1.4.4/1.4.10/1.4.12:** resizing, 320-CSS-pixel reflow and text spacing;
- **1.4.13:** hover/focus content dismissal, persistence and hoverability;
- **2.1.1/2.1.2:** keyboard operation and no trap;
- **2.2.1/2.2.2:** time limits and pause/stop/hide;
- **2.3.1:** flashing threshold;
- **2.4.3/2.4.7/2.4.11:** focus order, visible focus and no focus occlusion;
- **2.5.3/2.5.7/2.5.8:** label in name, dragging alternatives and target size;
- **3.2.1/3.2.2/3.3.1–3.3.4:** predictable change and error prevention/recovery;
- **4.1.2/4.1.3:** accessible name/role/value and status messages.

Do not claim conformance from a subset. Record `pass`, `fail`, `not applicable`, or `not tested` with reason.

## Semantics and accessible names

- Use HTML landmarks, headings, lists, tables, labels and native controls before ARIA.
- Every control needs a stable accessible name that includes its visible label.
- Icon-only controls require a name and visible tooltip or equivalent discovery where the icon is unfamiliar.
- Associate help and errors with the field using native semantics or `aria-describedby`.
- Expose current, expanded, selected, checked, pressed, busy and invalid state accurately.
- Keep DOM and visual reading order aligned.

Inspect the accessibility tree for representative states. A name visible in the DOM is not proof that assistive technology receives it.

## Keyboard and focus

Run the complete primary and recovery journeys with keyboard only:

- logical tab and reading order;
- activation with platform-standard keys;
- visible focus with at least a 24 by 24 CSS px perimeter equivalent and sufficient contrast;
- no focus hidden by sticky UI;
- focus restored to the invoking control after overlays;
- roving tabindex only for composite widgets that require it;
- shortcuts documented, disableable when character keys are used, and unavailable inside text input unless intended.

### Dialog and overlay contract

A modal dialog requires a label, optional description, initial focus chosen by task risk, contained tab sequence, Escape behavior unless unsafe, background inertness, scroll containment and focus return. Popovers and menus need outside dismissal without stealing ordinary text selection or browser gestures.

## Screen-reader and assistive-technology matrix

Choose combinations supported by the product and record versions. A practical minimum is:

- NVDA with Firefox or Chrome on Windows;
- VoiceOver with Safari on macOS or iOS;
- one Android/TalkBack path when mobile is in scope.

Check landmarks, headings, names, descriptions, state changes, table relationships, form errors, live status, dialogs and route/page-title changes. Do not require identical announcements across tools; require equivalent meaning and operation.

## Zoom, reflow and text spacing

At 200% and 400% zoom verify content and controls remain present and operable without two-dimensional scrolling except for intrinsically two-dimensional content. Apply the WCAG text-spacing override and check that labels, buttons and instructions remain readable. Do not disable browser zoom.

## Forced colors, contrast and color independence

Test `forced-colors: active`. Preserve control boundaries, selected state and focus without background images or color alone. Use the applicable WCAG contrast thresholds: normally 4.5:1 for text, 3:1 for large text and 3:1 for required component boundaries and state indicators. Record sampled foreground/background values and method.

## Motion, input and touch

- Preserve meaning under reduced motion; replace spatial travel with immediate or low-motion state changes.
- Offer pause/stop for nonessential moving content that starts automatically and persists.
- Provide keyboard and pointer alternatives for drag, pinch, hover and precision gestures.
- Use pointer capture only while needed and release it on cancel, completion, blur and teardown.
- Target at least 24 by 24 CSS px under WCAG 2.2; prefer 44 by 44 for touch-critical controls.

## Automated checks

Use the host project's pinned tooling. Typical commands are:

```bash
npx axe http://127.0.0.1:4173 --exit
npx pa11y-ci
npx lighthouse http://127.0.0.1:4173 --only-categories=accessibility --output=json --output-path=artifacts/lighthouse-a11y.json
```

Do not install unpinned packages in a release gate. Run scans after dynamic states and route changes, not only at initial load. Preserve rule ID, impact, target, state, screenshot and remediation decision.

Automated zero violations is not proof of accessibility. Manual keyboard, reflow, forced-colors and assistive-technology evidence remain required.

## State completeness

Mark each state implemented, not applicable with reason, or blocked:

- initial, loading and skeleton;
- empty and zero-results;
- partial, stale and offline;
- validation and server error;
- unauthorized and forbidden;
- success and confirmation;
- destructive confirmation and undo;
- focus, hover, active, selected and disabled;
- long content, localization and untrusted content;
- refresh, back/forward, deep link and retry.