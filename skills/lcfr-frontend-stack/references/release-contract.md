# Functional, performance, and release contract

## Dogfood pass

Exercise the interface as a visitor: fresh entry, primary task, alternate path, keyboard-only path, touch path, invalid input, network failure, refresh, deep link, back/forward, retry, logout/permission boundary where relevant, and route teardown. Preserve URLs, screenshots, console output, and exact reproductions for defects.

## Performance pass

Measure both loading and runtime. Capture Core Web Vitals or equivalent, transferred bytes by type, responsive-image selection, long tasks, layout shifts, font behavior, animation frame stability, and third-party cost. Fix source ownership before compressing symptoms. Performance optimization cannot silently lower visual fidelity or remove accessibility behavior.

## Preview gate

1. Freeze and identify the candidate.
2. Build locally from a clean environment.
3. Deploy an isolated immutable preview.
4. Run the complete required browser/evidence matrix against the exact preview URL.
5. Compare served asset hashes with the verified build when practical.
6. Treat any change as a new candidate requiring rerun.

## Independent review

For material changes, request a review of the exact commit/tree or immutable build. Ask for concrete blockers with reproductions, not generic impressions. Reproduce returned findings on current files before editing; stale line numbers are not evidence.

## Production gate

Deploy only the verified candidate. Read back the production route, settings, assets, and critical user journey. Confirm custom-domain/DNS target where applicable. Never report deployment success from command exit alone.

## Release evidence minimum

- exact revision/build and environment;
- commands and exit results;
- routes, profiles, themes, and states covered;
- screenshots/reports and hashes where useful;
- accessibility and performance results;
- console/network/overflow status;
- known limitations and blocked decisions;
- preview and production URLs/read-back;
- human acceptance status stated explicitly, never inferred.
