# Systems and product UI

Use this reference for product shells, dashboards, settings, forms, onboarding, dense operational interfaces, components, and design-system work.

## Preserve or choose the system deliberately

Before importing anything, inspect the framework, package manifest, component library, tokens, state management, routing, validation, analytics, localization, and testing setup.

Prefer the incumbent system when it can satisfy the contract. Choose an official system when platform or ecosystem consistency is a requirement. Choose accessible primitives when the product needs custom expression. Build from native HTML when an abstraction adds no value.

Never mix multiple design systems casually. Verify package existence, version, licence, maintenance, bundle impact, SSR behavior, and accessibility before use.

## Experience architecture

Map every primary journey:

- entry and permission context;
- information required to decide;
- progressive disclosure;
- action and validation;
- pending state;
- success confirmation;
- failure diagnosis;
- retry, undo, cancellation, and recovery;
- persistence across refresh, history navigation, or reconnection.

Navigation labels, routes, field names, analytics events, and legal text are contracts. Do not change them silently during visual work.

## State completeness

For every component or flow, mark each state applicable or not applicable:

- default, hover, focus-visible, active, selected, expanded;
- disabled with explanation when needed;
- loading and skeleton that preserve final geometry;
- empty with a truthful next action;
- partial, stale, delayed, and offline;
- validation, field error, form error, and system error;
- pending and optimistic state;
- success, undo, cancellation, and destructive confirmation;
- unauthorized, forbidden, expired, and re-authentication;
- first-run, returning, and migrated states.

Do not use color as the only state signal. Keep status announcements available to assistive technology.

## Information density

Choose density from task frequency, expertise, risk, and display context.

- Low-frequency or high-risk tasks need explanation, clear grouping, and confirmation.
- High-frequency expert tools need scanability, keyboard paths, stable geometry, and compact controls.
- Dense data belongs in tables, trees, timelines, canvases, or charts with explicit semantics, not a field of decorative cards.
- Long lists need search, filter, grouping, pagination, virtualization, or disclosure based on actual use.

Preserve user position and selections during refresh or mutation when safe.

## Component contract

Each reusable component defines:

- semantic element and accessible name;
- data and event interface;
- controlled/uncontrolled ownership;
- variants tied to meaning, not arbitrary appearance;
- complete states;
- keyboard and pointer behavior;
- focus entry, containment, restoration, and escape;
- responsive behavior and content limits;
- localization and bidi behavior;
- loading and rendering cost;
- testable acceptance conditions.

Prefer composition over a prop matrix that allows invalid combinations.

## Forms

- Use visible labels; placeholders are examples, never labels.
- Match input types, autocomplete values, virtual keyboards, and validation timing to the data.
- Validate at a point where the user can recover without interruption.
- Place field errors beside the field and summarize errors when a long form needs navigation.
- Preserve entered data after recoverable failure.
- Distinguish optional from required consistently.
- Confirm destructive effects and irreversible scope in concrete language.

## Feedback and micro-behavior

Use the least disruptive feedback that communicates state:

- immediate local change for direct manipulation;
- inline pending state for bounded actions;
- optimistic updates only with safe rollback or undo;
- status regions for asynchronous completion;
- toasts for transient cross-surface events, not validation or durable errors;
- dialogs only when the task truly blocks the underlying surface.

Hover cannot own essential information. Focus feedback appears immediately. Active feedback is tactile but does not shift layout.

## Design tokens

Use semantic tokens for:

- color and contrast roles;
- typography roles;
- spacing and container scales;
- radii and shape families;
- borders, elevation, and material;
- motion duration and easing;
- z-index layers;
- breakpoints and responsive containers;
- data visualization roles.

Token names express purpose. Component aliases may reference global semantic tokens. Raw values remain at the source layer.

## Component documentation

A component is not complete until documentation shows:

- purpose and non-purpose;
- anatomy;
- variants and states;
- content rules;
- keyboard and assistive behavior;
- responsive examples;
- do/don't guidance;
- code example;
- tests and known limitations.

Use a preview or story surface that renders all states together when practical.

## Product-UI quality gate

- Primary tasks are findable without decorative explanation.
- Status and system ownership are clear.
- Dense surfaces remain scannable at 200% zoom and narrow widths.
- Keyboard users can complete the same work.
- Empty and error states preserve context and provide recovery.
- Mutations expose pending, success, and rollback behavior.
- Tables and charts have semantic alternatives where needed.
- Focus survives routing, dialogs, and optimistic updates.
- Analytics and content contracts remain intact.
