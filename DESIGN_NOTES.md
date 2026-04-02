# Full-Stack Take-Home Design Notes

This note explains the reasoning behind the full-stack exercise in `fullstack/`.

## Why this exercise exists

The March 2026 role description is for a product-focused full-stack engineer who will:

- build end-to-end features across backend and frontend
- work closely with product and design
- improve quality, usability, and performance
- operate pragmatically in a small team

The exercise therefore needs to test more than backend correctness. It should show whether a candidate can ship a small, coherent product slice.

## Why this shape

The chosen task is a small learner workflow:

- list lessons
- open a lesson
- read ordered content
- update progress

This gives enough room to observe:

- API design
- relational data handling
- frontend state and rendering
- user-facing judgement

without turning the task into a mini product build.

## Why reuse the existing content model

Reusing the same schema and seed data as the backend exercise has a few advantages:

- less repo overhead
- easier calibration between exercises
- consistent reviewer context
- enough relational complexity to test correctness without inventing a new domain

The main extra signal comes from the UI and from the requirement to connect the full flow.

## Why the 2-hour scope can be fair

The main scope controls are deliberate:

- only three endpoints
- a small dataset
- no authentication
- no schema changes
- no deployment requirement
- single-page frontend allowed
- hardcoded seed learner context allowed
- refetch-after-mutation allowed

Those shortcuts make it realistic for a strong candidate to finish a clear vertical slice in about 90 minutes and stop within 2 hours.

## How it differs from the backend senior exercise

The backend senior exercise in the repo is better for testing:

- API correctness under tighter time pressure
- SQL and data-modelling judgement
- back-end-oriented implementation clarity

This full-stack exercise shifts the emphasis to:

- end-to-end ownership
- frontend judgement
- coherence of the user journey
- ability to simplify without losing the essentials

## Reviewer intent

Reviewers should reward:

- correct core behaviour
- a usable interface
- sensible trade-offs
- clear communication

Reviewers should not reward unnecessary scope expansion on its own.
