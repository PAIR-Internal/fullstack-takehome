# PAIR Full-Stack Take-Home Exercise

This repository contains the full-stack take-home exercise plus an optional starter scaffold.

The goal is to get a realistic snapshot of how you build a small end-to-end product feature: a little backend API, a little frontend UI, and the judgement needed to keep the whole thing simple and usable.

This is a second-stage exercise for candidates who have already passed an initial application screen.

Timebox: a strong candidate should be able to complete the core requirements in about 90 minutes. Please stop after 2 hours. If you run out of time, prioritise one clear, working vertical slice over extra polish.

## Using this repo

You can implement the solution in the stack of your choice.

This repo includes an optional scaffold that mirrors our production stack:

- `WebUI/` - Vue 3 + TypeScript + Vite + Vuetify + Pinia
- `API/` - FastAPI with a light router/service/schema split

You are welcome to use that scaffold if it helps you move faster, but you do not need to use it. If you prefer different technologies or a different project structure, that is completely fine.

## Repository contents

This repository includes:

- `docker-compose.yml` - a Postgres database and optional Adminer UI
- `db/00-schema.sql` - schema
- `db/01-seed.sql` - seed data
- `db/DATA_MODEL.md` - quick reference for the content model
- `fullstack/openapi.yaml` - API contract for this exercise
- `fullstack/examples/expected_responses.md` - example response shapes
- `fullstack/scripts/curl_examples.sh` - quick ways to exercise your API
- `WebUI/` - optional frontend scaffold
- `API/` - optional backend scaffold

The scaffold distils the main PAIR repo into a smaller monorepo-shaped starter. The backend ships with a mock in-memory repository by default so it is immediately runnable, and it already contains a `PostgresLessonRepository` seam for swapping in the real exercise queries.

## What you are building

You will build a tiny learner-facing workspace for the PAIR platform.

It should let a learner:

- see the lessons available to them
- open a lesson
- view lesson content in the correct order
- see their progress
- mark blocks as `seen` or `completed`

You will build:

- a small HTTP API backed by Postgres
- a minimal frontend that consumes that API

The data model is CMS-like:

- A Lesson contains an ordered list of Blocks
- Each Block can have Variants
- A variant may be a default (`tenant_id = NULL`) or a tenant override (`tenant_id = X`)
- When returning a lesson for a tenant, you must choose the best variant for each block

We also track user progress per block in a lesson.

## Setup

### Run the database

```bash
docker compose up -d
```

Postgres will be available at:

- Host: `localhost`
- Port: `5432`
- Database: `pair_takehome`
- User: `pair`
- Password: `pair`

Connection string:

```text
postgresql://pair:pair@localhost:5432/pair_takehome
```

### Optional: inspect data via Adminer

Adminer is available at [http://localhost:8081](http://localhost:8081).

- System: `PostgreSQL`
- Server: `db` (if accessing from another container) or `localhost` (from your machine)
- Username: `pair`
- Password: `pair`
- Database: `pair_takehome`

### Optional: run the provided scaffold

Frontend:

```bash
npm install
npm run --workspace WebUI dev
```

The scaffolded UI expects the API at `http://localhost:8000`.

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r API/requirements.dev.txt
uvicorn inversity_api.main:app --reload --app-dir API
```

If you use your own stack instead, you can ignore the scaffold-specific instructions above.

## Requirements

Implement these three API endpoints:

1. `GET /tenants/{tenant_id}/users/{user_id}/lessons`
2. `GET /tenants/{tenant_id}/users/{user_id}/lessons/{lesson_id}`
3. `PUT /tenants/{tenant_id}/users/{user_id}/lessons/{lesson_id}/progress`

Please follow the response shapes in `fullstack/openapi.yaml`.

Then build a small frontend that lets a learner:

- see the lessons available to them
- understand whether a lesson is `not_started`, `in_progress`, or `completed`
- open a lesson
- see lesson blocks in the correct order
- see current progress summary
- mark a block as `seen` or `completed`
- see the UI update after progress changes

You can implement the frontend as:

- one small page with a lesson picker, or
- two small views/screens

Either approach is fine.

## Important simplifications

To keep this fair for a 2-hour exercise:

- You may hardcode the seed learner context in the frontend:
  - `tenant_id = 1`
  - `user_id = 10`
- You do not need authentication
- You do not need client-side routing if you would rather keep this as one page
- You may refresh data after each progress update instead of doing optimistic UI
- You do not need to deploy or containerise your app
- You do not need to modify the schema
- You do not need to build a design system or polished visual design

Reasonable shortcuts are part of the exercise. We care about judgement.

## Behaviour rules

### Tenant safety and validation

For all endpoints:

- the tenant must exist
- the user must exist and belong to the tenant

If not, return `404`.

For lesson-specific endpoints, additionally ensure:

- the lesson exists and belongs to the tenant

If not, return `404`.

For the `PUT` endpoint, also validate:

- `block_id` is part of that lesson

If not, return `400`.

### Lessons list endpoint

`GET /tenants/{tenant_id}/users/{user_id}/lessons`

Return all lessons for the tenant, each with:

- lesson metadata
- progress summary
- a derived lesson `status`
- `next_block_id`

Derived lesson status rules:

- `completed` if all blocks are completed
- `in_progress` if at least one block has progress but the lesson is not fully completed
- `not_started` if the user has no progress rows for that lesson

`next_block_id` should be:

- the first block in lesson order whose status is not `completed`
- `null` if the lesson is completed

### Lesson endpoint

`GET /tenants/{tenant_id}/users/{user_id}/lessons/{lesson_id}`

Return:

- lesson metadata
- blocks in the correct order
- the selected variant for each block (`tenant override > default`)
- the user's progress per block
- a summary of progress

### Block ordering

Blocks must be returned ordered by `lesson_blocks.position` ascending.

### Variant selection

For each block, select exactly one variant using this rule:

1. If a variant exists for `(block_id, tenant_id = {tenant_id})`, return that.
2. Otherwise return the default variant `(block_id, tenant_id IS NULL)`.

### Progress semantics

Progress is stored per block in `user_block_progress`.

- A block with status `completed` counts as both seen and completed
- A block with status `seen` counts as seen only
- A missing row means no progress for that block

For `PUT` upsert:

- repeating the same request should not create duplicates
- progress is monotonic
- if the existing status is `completed` and the request is `seen`, keep `completed`
- if the request is `completed`, store `completed`

## UI expectations

We are not looking for pixel-perfect design, but we are looking for sensible product choices.

Please include:

- loading state
- basic error state
- empty state for the lessons list if no lessons exist
- obvious affordances for marking progress

The UI can be simple. We care more about clarity, product judgement, and whether the feature hangs together cleanly.

## What we're looking for

- ability to build a small feature end to end
- pragmatic API and relational DB work
- thoughtful frontend structure and state handling
- clear, usable UI states
- good judgement about what to simplify in a timeboxed exercise
- clear instructions and communication

## What to submit

Please send us:

1. A link to a repo with your implementation
2. A short `NOTES.md` answering:
   - what you chose to simplify
   - any trade-offs you made
   - what you would improve with 2 more hours

## Suggested next steps if you use the scaffold

1. Replace `MockLessonRepository` with SQL-backed implementations in `API/inversity_api/services/postgres_repository.py`.
2. Keep the response DTOs in sync with `fullstack/openapi.yaml`.
3. Point the frontend at the real Postgres-backed API and remove the mock-data note from the UI.
