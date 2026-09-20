#!/usr/bin/env bash
set -euo pipefail

API="${API:-http://localhost:8000}"

psql_q() {
  docker compose exec -T postgres psql -U minecore -d minecore -t -A -c "$1" | tr -d '[:space:]'
}

echo "==> Resolving test data from database"

ORG_ID="$(psql_q "SELECT id FROM organizations WHERE code='demo'")"
[ -n "$ORG_ID" ] || { echo "No demo organization. Did 'make seed' run?" >&2; exit 1; }

USER_ID="$(psql_q "SELECT id FROM users WHERE email='admin@demo.local'")"
[ -n "$USER_ID" ] || { echo "No demo user. Did 'make seed' run?" >&2; exit 1; }

SITE_ID="$(psql_q "SELECT id FROM mine_sites WHERE organization_id='${ORG_ID}' LIMIT 1")"
[ -n "$SITE_ID" ] || SITE_ID="$(psql_q "INSERT INTO mine_sites (organization_id, code, name, status) VALUES ('${ORG_ID}', 'SMOKE-1', 'Smoke Site', 'active') RETURNING id")"

PIT_ID="$(psql_q "SELECT id FROM pits WHERE organization_id='${ORG_ID}' LIMIT 1")"
[ -n "$PIT_ID" ] || PIT_ID="$(psql_q "INSERT INTO pits (organization_id, mine_site_id, code, name, status) VALUES ('${ORG_ID}', '${SITE_ID}', 'SMOKE-PIT-1', 'Smoke Pit', 'active') RETURNING id")"

MATERIAL_ID="$(psql_q "SELECT id FROM materials WHERE organization_id='${ORG_ID}' LIMIT 1")"
[ -n "$MATERIAL_ID" ] || MATERIAL_ID="$(psql_q "INSERT INTO materials (organization_id, code, name, status) VALUES ('${ORG_ID}', 'SMOKE-MAT-1', 'Smoke Material', 'active') RETURNING id")"

echo "  ORG_ID      = $ORG_ID"
echo "  USER_ID     = $USER_ID"
echo "  SITE_ID     = $SITE_ID"
echo "  PIT_ID      = $PIT_ID"
echo "  MATERIAL_ID = $MATERIAL_ID"
echo

H_ORG="X-Organization-Id: $ORG_ID"
H_USR="X-User-Id: $USER_ID"

echo "==> GET /health"
curl -sS "$API/health" | jq
echo

echo "==> POST /api/mining-operations (create draft)"
CREATE=$(curl -sS -X POST "$API/api/mining-operations" -H "$H_ORG" -H "$H_USR" -H "Content-Type: application/json" -d "{\"mine_site_id\":\"$SITE_ID\",\"pit_id\":\"$PIT_ID\",\"material_id\":\"$MATERIAL_ID\",\"operation_date\":\"2026-01-15\",\"quantity\":\"100.5000\",\"operator_name\":\"Smoke Tester\",\"notes\":\"created by smoke_mining.sh\"}")
echo "$CREATE" | jq
OP_ID=$(echo "$CREATE" | jq -r '.id // empty')
[ -n "$OP_ID" ] && [ "$OP_ID" != "null" ] || { echo; echo "STOP: create failed."; exit 1; }
echo

echo "==> GET /api/mining-operations/$OP_ID"
curl -sS "$API/api/mining-operations/$OP_ID" -H "$H_ORG" | jq
echo

echo "==> PATCH (still draft — update quantity)"
curl -sS -X PATCH "$API/api/mining-operations/$OP_ID" -H "$H_ORG" -H "$H_USR" -H "Content-Type: application/json" -d '{"quantity":"150.0000"}' | jq
echo

echo "==> POST /record (draft -> recorded)"
curl -sS -X POST "$API/api/mining-operations/$OP_ID/record" -H "$H_ORG" -H "$H_USR" | jq
echo

echo "==> PATCH after record (expect 409)"
curl -sS -o /tmp/smoke_patch.json -w "HTTP %{http_code}\n" -X PATCH "$API/api/mining-operations/$OP_ID" -H "$H_ORG" -H "$H_USR" -H "Content-Type: application/json" -d '{"quantity":"999"}'
jq < /tmp/smoke_patch.json
echo

echo "==> POST /approve (recorded -> approved)"
curl -sS -X POST "$API/api/mining-operations/$OP_ID/approve" -H "$H_ORG" -H "$H_USR" | jq
echo

echo "==> POST /cancel after approve (expect 409)"
curl -sS -o /tmp/smoke_cancel.json -w "HTTP %{http_code}\n" -X POST "$API/api/mining-operations/$OP_ID/cancel" -H "$H_ORG" -H "$H_USR" -H "Content-Type: application/json" -d '{"reason":"should fail"}'
jq < /tmp/smoke_cancel.json
echo

echo "==> GET /audit"
curl -sS "$API/api/mining-operations/$OP_ID/audit" -H "$H_ORG" | jq
echo

echo "==> GET /api/mining-operations (list)"
curl -sS "$API/api/mining-operations" -H "$H_ORG" | jq 'map({operation_number, status, quantity})'
echo

echo "==> Smoke test complete. OP_ID=$OP_ID"
