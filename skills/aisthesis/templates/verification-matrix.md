# Verification matrix

| Profile | Engine | Theme | Motion | Route/state | Input | Assertions | Evidence | Result |
|---|---|---|---|---|---|---|---|---|
| 320 mobile | Chromium | | full | | touch/keyboard | | | |
| 375 mobile | Firefox-derived | | full | | wheel/keyboard | | | |
| 414 mobile | Chromium | | reduce | | touch | | | |
| 768 tablet | Chromium | | full | | keyboard | | | |
| 1280 desktop | Firefox-derived | | full | | wheel/keyboard | | | |
| wide | Chromium | | full | | wheel | | | |

## State completeness

| State | Applicable | Verification | Result |
|---|---|---|---|
| Loading | | | |
| Empty | | | |
| Partial/offline | | | |
| Error/retry | | | |
| Unauthorized | | | |
| Success | | | |
| Destructive confirmation | | | |
| Focus/hover/active/disabled | | | |
| Refresh/deep-link/back-forward | | | |

## Global gates

- [ ] Build and source tests
- [ ] Console/page/network errors
- [ ] Horizontal overflow
- [ ] Keyboard, focus, touch, zoom
- [ ] Automated accessibility plus manual checks
- [ ] Responsive source selection
- [ ] Reduced motion
- [ ] Performance
- [ ] Four Aisthesis visual passes
- [ ] Preview parity
