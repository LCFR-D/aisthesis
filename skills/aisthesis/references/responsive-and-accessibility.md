# Responsive, state, and accessibility contract

## Required viewport matrix

Use 320, 375, 414, 768, 1280, and one authored wide profile when relevant. Add short-height desktop, landscape mobile, and device-pixel-ratio variants when they affect composition. Intermediate widths are first-class states, not interpolation assumptions.

At each profile verify:

- no document-level horizontal overflow;
- display text and controls do not clip or wrap unexpectedly;
- primary journeys and recovery paths remain available;
- focal art and landmarks survive the crop;
- touch targets are at least 44 by 44 CSS pixels where applicable;
- browser-selected media matches the authored composition;
- light/dark or Day/Night parity preserves geometry and hierarchy.

## Accessibility gate

- semantic landmarks, headings, lists, labels, names, roles, and values;
- keyboard order, operation, focus visibility, and no focus occlusion;
- contrast and non-color state communication;
- zoom and text reflow without loss of content or operation;
- touch and pointer parity;
- meaningful alternatives for informative media; decorative media hidden semantically;
- reduced-motion behavior that preserves information;
- live status/error feedback and recovery;
- automated accessibility scan after dynamic state changes, plus manual keyboard review.

Automated zero violations is not proof of accessibility. Preserve every violation ID and target in evidence; do not summarize failures away.

## State completeness

Mark each as implemented, not applicable with reason, or blocked:

- initial/loading/skeleton;
- empty/zero-results;
- partial/stale/offline;
- validation and server error;
- unauthorized/forbidden;
- success/confirmation;
- destructive confirmation/undo;
- focus/hover/active/disabled;
- long content, localization, and untrusted content;
- refresh, back/forward, deep link, and retry.
