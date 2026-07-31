#!/bin/bash

# ============================================================
# FILE:
# backend/scripts/set_test_tokens.sh
#
# PURPOSE:
# Login as ADMIN, MODERATOR and USER and export JWT tokens
# into the current shell session.
#
# USAGE:
#
# source scripts/set_test_tokens.sh
#
# ============================================================

set -e

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL="${BASE_URL:-http://localhost:8000}"
LOGIN_URL="${BASE_URL}/api/v1/auth/login"

# ------------------------------------------------------------
# Change these credentials to your actual test users
# ------------------------------------------------------------

ADMIN_EMAIL="${ADMIN_EMAIL:-superadmin@example.com}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-123@Account}"

MODERATOR_EMAIL="${MODERATOR_EMAIL:-moderator@example.com}"
MODERATOR_PASSWORD="${MODERATOR_PASSWORD:-123@Account}"

USER_EMAIL="${USER_EMAIL:-user@example.com}"
USER_PASSWORD="${USER_PASSWORD:-123@Account}"


# ============================================================
# HELPER
# ============================================================

get_token() {
    local email="$1"
    local password="$2"
    local role="$3"

    echo ""
    echo "============================================================"
    echo "Logging in as ${role}..."
    echo "============================================================"

    RESPONSE=$(curl -sS \
        -X POST "${LOGIN_URL}" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=${email}" \
        -d "password=${password}")

    # Check whether access_token exists
    TOKEN=$(echo "$RESPONSE" | python -c '
import sys
import json

try:
    data = json.load(sys.stdin)

    token = data.get("access_token")

    if not token:
        print("ERROR")
        sys.exit(1)

    print(token)

except Exception:
    print("ERROR")
    sys.exit(1)
')

    if [ "$TOKEN" = "ERROR" ]; then
        echo ""
        echo "❌ Failed to login as ${role}"
        echo ""
        echo "Server response:"
        echo "$RESPONSE"
        echo ""
        return 1
    fi

    echo "✅ ${role} login successful"

    # Export variable dynamically
    case "$role" in
        ADMIN)
            export ADMIN_TOKEN="$TOKEN"
            ;;
        MODERATOR)
            export MODERATOR_TOKEN="$TOKEN"
            ;;
        USER)
            export USER_TOKEN="$TOKEN"
            ;;
    esac
}


# ============================================================
# GET TOKENS
# ============================================================

get_token \
    "$ADMIN_EMAIL" \
    "$ADMIN_PASSWORD" \
    "ADMIN"

get_token \
    "$MODERATOR_EMAIL" \
    "$MODERATOR_PASSWORD" \
    "MODERATOR"

get_token \
    "$USER_EMAIL" \
    "$USER_PASSWORD" \
    "USER"


# ============================================================
# DISPLAY RESULT
# ============================================================

echo ""
echo "============================================================"
echo "✅ TEST TOKENS SET"
echo "============================================================"

echo "ADMIN_TOKEN     : ${ADMIN_TOKEN:0:25}..."
echo "MODERATOR_TOKEN : ${MODERATOR_TOKEN:0:25}..."
echo "USER_TOKEN      : ${USER_TOKEN:0:25}..."

echo ""
echo "You can now run:"
echo ""
echo "    pytest tests/test_auth_permissions.py -v"
echo ""
echo "or:"
echo ""
echo "    pytest -v"
echo ""