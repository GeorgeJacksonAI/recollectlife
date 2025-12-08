#!/bin/bash
# Phase 6 Frontend Integration - Verification Script
# Tests authentication flow and story management

set -e

API_BASE="http://localhost:8000"
FRONTEND_URL="http://localhost:8081"

echo "=== Phase 6 Frontend Integration Verification ==="
echo ""

# Test 1: Backend health check
echo "✓ Test 1: Backend Health Check"
curl -s $API_BASE/health | jq .
echo ""

# Test 2: Frontend is accessible
echo "✓ Test 2: Frontend Accessibility"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" $FRONTEND_URL
echo ""

# Test 3: Register new user
echo "✓ Test 3: User Registration"
REGISTER_RESPONSE=$(curl -s -X POST $API_BASE/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_'$(date +%s)'@example.com",
    "password": "testpass123",
    "display_name": "Test User"
  }')
echo $REGISTER_RESPONSE | jq .
TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.access_token')
echo "Token: $TOKEN"
echo ""

# Test 4: Login with user
echo "✓ Test 4: User Login"
LOGIN_RESPONSE=$(curl -s -X POST $API_BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }')
echo $LOGIN_RESPONSE | jq .
echo ""

# Test 5: Get current user
echo "✓ Test 5: Get Current User (with token)"
if [ ! -z "$TOKEN" ]; then
  curl -s -X GET $API_BASE/api/auth/me \
    -H "Authorization: Bearer $TOKEN" | jq .
else
  echo "Skipped - no token from registration"
fi
echo ""

# Test 6: Create story
echo "✓ Test 6: Create Story"
if [ ! -z "$TOKEN" ]; then
  STORY_RESPONSE=$(curl -s -X POST $API_BASE/api/stories/ \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Test Story",
      "description": "Integration test story"
    }')
  echo $STORY_RESPONSE | jq .
  STORY_ID=$(echo $STORY_RESPONSE | jq -r '.id')
  echo "Story ID: $STORY_ID"
else
  echo "Skipped - no token"
fi
echo ""

# Test 7: Get user stories
echo "✓ Test 7: Get User Stories"
if [ ! -z "$TOKEN" ]; then
  curl -s -X GET $API_BASE/api/stories/ \
    -H "Authorization: Bearer $TOKEN" | jq .
else
  echo "Skipped - no token"
fi
echo ""

# Test 8: Send interview message
echo "✓ Test 8: Send Interview Message"
if [ ! -z "$TOKEN" ] && [ ! -z "$STORY_ID" ]; then
  curl -s -X POST $API_BASE/api/interview/$STORY_ID \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "message": "I grew up in a small town."
    }' | jq .
else
  echo "Skipped - no token or story"
fi
echo ""

echo "=== Verification Complete ==="
echo ""
echo "Manual Testing Checklist:"
echo "1. Navigate to $FRONTEND_URL"
echo "2. Click 'Sign Up' and register a new account"
echo "3. Verify redirect to /dashboard after registration"
echo "4. Create a new story"
echo "5. Start interview and send messages"
echo "6. Verify messages persist across page refresh"
echo "7. Logout and login again"
echo "8. Verify auth state persists in localStorage"
