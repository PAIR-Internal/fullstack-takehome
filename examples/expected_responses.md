# Example responses (from the seed database)

These examples show **shape** and **key fields**. JSON key ordering does not matter.

## 1) GET /tenants/1/users/10/lessons

Expected highlights:

- returns one lesson for Acme user `10`
- lesson `100` is `in_progress`
- `next_block_id = 201`
- progress summary:
  - `total_blocks = 3`
  - `seen_blocks = 2`
  - `completed_blocks = 1`
  - `last_seen_block_id = 201`
  - `completed = false`

Example (abridged):

```json
{
  "lessons": [
    {
      "id": 100,
      "slug": "ai-basics",
      "title": "AI Basics",
      "status": "in_progress",
      "next_block_id": 201,
      "progress_summary": {
        "total_blocks": 3,
        "seen_blocks": 2,
        "completed_blocks": 1,
        "last_seen_block_id": 201,
        "completed": false
      }
    }
  ]
}
```

## 2) GET /tenants/1/users/10/lessons/100

Expected highlights:

- 3 blocks with positions `[1, 2, 3]`
- block `200` uses the tenant override (`tenant_id = 1`)
- progress:
  - block `200` = `completed`
  - block `201` = `seen`
  - block `202` = `null`

Example (abridged):

```json
{
  "lesson": { "id": 100, "slug": "ai-basics", "title": "AI Basics" },
  "blocks": [
    {
      "id": 200,
      "type": "markdown",
      "position": 1,
      "variant": {
        "id": 1100,
        "tenant_id": 1,
        "data": {
          "markdown": "Welcome Acme team — this intro is customised for your organisation."
        }
      },
      "user_progress": "completed"
    },
    {
      "id": 201,
      "type": "quiz",
      "position": 2,
      "variant": {
        "id": 1001,
        "tenant_id": null,
        "data": {
          "question": "In one sentence, what is a neural network?"
        }
      },
      "user_progress": "seen"
    },
    {
      "id": 202,
      "type": "markdown",
      "position": 3,
      "variant": {
        "id": 1002,
        "tenant_id": null,
        "data": {
          "markdown": "Summary: You have completed the basics. (Default summary)"
        }
      },
      "user_progress": null
    }
  ],
  "progress_summary": {
    "total_blocks": 3,
    "seen_blocks": 2,
    "completed_blocks": 1,
    "last_seen_block_id": 201,
    "completed": false
  }
}
```

## 3) PUT /tenants/1/users/10/lessons/100/progress with {"block_id":202,"status":"seen"}

Expected highlights:

- `stored_status = "seen"`
- `seen_blocks` becomes `3`
- `last_seen_block_id` becomes `202`

## 4) PUT /tenants/1/users/10/lessons/100/progress with {"block_id":202,"status":"completed"}

Expected highlights:

- `stored_status = "completed"`
- `completed_blocks` becomes `2`
- a later `PUT` with status `seen` should **not** downgrade it
