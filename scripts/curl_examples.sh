#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "1) List lessons"
curl -s "${BASE_URL}/tenants/1/users/10/lessons" | jq .

echo
echo "2) Get lesson workspace"
curl -s "${BASE_URL}/tenants/1/users/10/lessons/100" | jq .

echo
echo "3) Mark block 202 as seen"
curl -s -X PUT "${BASE_URL}/tenants/1/users/10/lessons/100/progress" \
  -H "content-type: application/json" \
  -d '{"block_id":202,"status":"seen"}' | jq .

echo
echo "4) Mark block 202 as completed"
curl -s -X PUT "${BASE_URL}/tenants/1/users/10/lessons/100/progress" \
  -H "content-type: application/json" \
  -d '{"block_id":202,"status":"completed"}' | jq .
