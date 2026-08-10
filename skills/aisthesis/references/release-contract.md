# Functional, performance, security, and release contract

## Dogfood pass

Exercise the interface as a visitor: fresh entry, primary task, alternate path, keyboard-only path, touch path, invalid input, slow and failed network, refresh, deep link, back/forward, retry, cancellation, undo, logout and permission boundary where relevant, and route teardown. Preserve URLs, screenshots, console output, and exact reproductions for defects.

Test real content extremes: shortest, longest, missing, localized, untrusted, and high-volume values. Confirm analytics, consent, and legal behavior only from actual implementation evidence.

## Accessibility gate

Run automated checks and manual keyboard/semantics review. Verify focus order and restoration, names/roles/states, headings and landmarks, zoom/reflow, contrast, touch targets, error association, live announcements, reduced motion, themes, and assistive alternatives for charts, canvas, drag, and rich media.

Automated tools find candidates; they do not prove usability.

## Security and privacy gate

Review the exact frontend trust boundaries:

- untrusted HTML, markdown, URLs, SVG, images, and rich text;
- DOM injection and unsafe rendering APIs;
- authentication and authorization assumptions exposed in UI logic;
- tokens, secrets, source maps, logs, analytics, and error payloads;
- cross-origin requests, redirects, downloads, uploads, and file previews;
- dependency integrity, licence, known vulnerabilities, and bundle provenance;
- consent, tracking, storage, clipboard, camera, microphone, location, and notification use;
- clickjacking, opener relationships, external links, and embedded third-party content.

Client-side hiding is never authorization. Do not include secrets in frontend bundles. Sensitive actions require server-side enforcement and clear human scope.

## Performance pass

Measure loading and runtime separately. Capture:

- Core Web Vitals or equivalent field/lab evidence;
- transferred bytes and request count by type;
- responsive-image and font selection;
- rendering, hydration, long tasks, memory, and layout shifts;
- animation frame stability and scroll responsiveness;
- third-party, analytics, canvas, video, and WebGL cost;
- cache, compression, preloading, and route-splitting behavior.

Fix source ownership before compressing symptoms. Performance optimization cannot silently lower visual fidelity, remove content, or regress accessibility.

## Cross-browser matrix

Choose browsers from audience and risk. For high-risk interaction, scrolling, media, forms, or new platform APIs, include Chromium and Firefox-derived engines plus WebKit where supported. Distinguish product failure, browser variance, harness failure, and unsupported capability.

Use real input for critical behavior. Synthetic DOM mutation is not evidence that keyboard, pointer, touch, wheel, drag, clipboard, upload, or focus behavior works.

## Preview gate

1. Freeze and identify the candidate.
2. Build locally from a clean environment.
3. Deploy an isolated immutable preview.
4. Run the complete required browser/evidence matrix against the exact preview URL.
5. Inspect rendered screenshots at full resolution.
6. Compare served asset hashes with the verified build when practical.
7. Treat any code, configuration, content, dependency, or asset change as a new candidate requiring rerun.

## Independent review

For material changes, request a review of the exact commit, tree, immutable build, or deployment. Ask for concrete blockers with reproductions, not generic impressions. Reproduce returned findings on current files before editing; stale line numbers and older candidates are not evidence about the current artifact.

## Production gate

Deploy only the verified candidate. Read back the production route, settings, assets, headers, and critical user journey. Confirm custom-domain and DNS targets where applicable. Verify rollback or previous deployment availability. Never report deployment success from command exit alone.

## Release evidence minimum

- exact revision, tree/build, environment, lock state, and deployment identity;
- commands and exit results;
- routes, browsers, profiles, themes, locale, and states covered;
- screenshots, traces, reports, and hashes where useful;
- functional, accessibility, security, and performance results;
- console, network, overflow, hydration, and resource status;
- known limitations and blocked decisions;
- preview and production URLs with read-back evidence;
- rollback path;
- human acceptance status stated explicitly, never inferred.
