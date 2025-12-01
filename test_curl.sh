#!/bin/bash
# Test CP-VTON+ RunPod Endpoint باستخدام cURL

# ==================== Configuration ====================
# عدّل هنا بعد الـ deployment
ENDPOINT_ID="your-endpoint-id"        # من RunPod Console
API_KEY="your-api-key"                 # من RunPod Settings → API Keys

# ==================== Test Images ====================
PERSON_IMAGE="person.jpg"  # عدّل المسار
CLOTH_IMAGE="cloth.jpg"    # عدّل المسار

# ==================== Colors ====================
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== Functions ====================

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# ==================== Test 1: Sync Request ====================

test_sync() {
    print_header "Test 1: Synchronous Request"
    
    echo -e "${YELLOW}Endpoint:${NC} $ENDPOINT_ID"
    echo -e "${YELLOW}Images:${NC} $PERSON_IMAGE, $CLOTH_IMAGE"
    echo ""
    
    # تحويل الصور لـ Base64
    PERSON_B64=$(base64 -w 0 "$PERSON_IMAGE" 2>/dev/null || base64 "$PERSON_IMAGE")
    CLOTH_B64=$(base64 -w 0 "$CLOTH_IMAGE" 2>/dev/null || base64 "$CLOTH_IMAGE")
    
    echo -e "${BLUE}Sending request...${NC}"
    
    # إرسال request
    RESPONSE=$(curl -s -X POST \
        "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"input\": {
                \"person_image\": \"${PERSON_B64}\",
                \"cloth_image\": \"${CLOTH_B64}\",
                \"output_format\": \"PNG\"
            }
        }")
    
    # عرض النتيجة
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
    
    # حفظ النتيجة إذا نجح
    STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null)
    if [ "$STATUS" = "COMPLETED" ]; then
        SUCCESS=$(echo "$RESPONSE" | jq -r '.output.success' 2>/dev/null)
        if [ "$SUCCESS" = "true" ]; then
            echo ""
            echo -e "${GREEN}✅ Success!${NC}"
            
            # استخراج وحفظ الصورة
            RESULT_B64=$(echo "$RESPONSE" | jq -r '.output.result_image' 2>/dev/null)
            if [ -n "$RESULT_B64" ] && [ "$RESULT_B64" != "null" ]; then
                echo "$RESULT_B64" | base64 -d > result_curl.png
                echo -e "${GREEN}💾 Result saved to: result_curl.png${NC}"
            fi
        else
            ERROR=$(echo "$RESPONSE" | jq -r '.output.error' 2>/dev/null)
            echo -e "${RED}❌ Error: $ERROR${NC}"
        fi
    else
        echo -e "${RED}❌ Request failed${NC}"
    fi
}

# ==================== Test 2: Async Request ====================

test_async() {
    print_header "Test 2: Asynchronous Request"
    
    echo -e "${YELLOW}Endpoint:${NC} $ENDPOINT_ID"
    echo ""
    
    # تحويل الصور لـ Base64
    PERSON_B64=$(base64 -w 0 "$PERSON_IMAGE" 2>/dev/null || base64 "$PERSON_IMAGE")
    CLOTH_B64=$(base64 -w 0 "$CLOTH_IMAGE" 2>/dev/null || base64 "$CLOTH_IMAGE")
    
    echo -e "${BLUE}Starting async job...${NC}"
    
    # بدء job
    RESPONSE=$(curl -s -X POST \
        "https://api.runpod.ai/v2/${ENDPOINT_ID}/run" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"input\": {
                \"person_image\": \"${PERSON_B64}\",
                \"cloth_image\": \"${CLOTH_B64}\"
            }
        }")
    
    JOB_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
    
    if [ -n "$JOB_ID" ] && [ "$JOB_ID" != "null" ]; then
        echo -e "${GREEN}Job ID: $JOB_ID${NC}"
        echo ""
        echo -e "${BLUE}Polling for result...${NC}"
        
        # Poll للنتيجة
        MAX_TRIES=30
        SLEEP_TIME=2
        
        for i in $(seq 1 $MAX_TRIES); do
            echo -ne "\rAttempt $i/$MAX_TRIES..."
            
            STATUS_RESPONSE=$(curl -s -X GET \
                "https://api.runpod.ai/v2/${ENDPOINT_ID}/status/${JOB_ID}" \
                -H "Authorization: Bearer ${API_KEY}")
            
            STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status' 2>/dev/null)
            
            if [ "$STATUS" = "COMPLETED" ]; then
                echo ""
                echo -e "${GREEN}✅ Job completed!${NC}"
                echo "$STATUS_RESPONSE" | jq . 2>/dev/null
                break
            elif [ "$STATUS" = "FAILED" ]; then
                echo ""
                echo -e "${RED}❌ Job failed${NC}"
                echo "$STATUS_RESPONSE" | jq . 2>/dev/null
                break
            fi
            
            sleep $SLEEP_TIME
        done
    else
        echo -e "${RED}❌ Failed to start job${NC}"
        echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
    fi
}

# ==================== Test 3: Health Check ====================

test_health() {
    print_header "Test 3: Health Check"
    
    echo -e "${BLUE}Checking endpoint health...${NC}"
    
    RESPONSE=$(curl -s -X GET \
        "https://api.runpod.ai/v2/${ENDPOINT_ID}/health" \
        -H "Authorization: Bearer ${API_KEY}")
    
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
}

# ==================== Main ====================

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq not found. Installing...${NC}"
    echo "Run: sudo apt install jq  (Ubuntu/Debian)"
    echo "Or:  brew install jq      (macOS)"
fi

if ! command -v base64 &> /dev/null; then
    echo -e "${RED}❌ base64 not found${NC}"
    exit 1
fi

# Check config
if [ "$ENDPOINT_ID" = "your-endpoint-id" ]; then
    echo -e "${RED}❌ Please set ENDPOINT_ID in the script${NC}"
    exit 1
fi

if [ "$API_KEY" = "your-api-key" ]; then
    echo -e "${RED}❌ Please set API_KEY in the script${NC}"
    exit 1
fi

# Check images
if [ ! -f "$PERSON_IMAGE" ]; then
    echo -e "${RED}❌ Person image not found: $PERSON_IMAGE${NC}"
    exit 1
fi

if [ ! -f "$CLOTH_IMAGE" ]; then
    echo -e "${RED}❌ Cloth image not found: $CLOTH_IMAGE${NC}"
    exit 1
fi

# Run tests
print_header "CP-VTON+ RunPod Test Suite"

# اختر test
if [ "$1" = "sync" ]; then
    test_sync
elif [ "$1" = "async" ]; then
    test_async
elif [ "$1" = "health" ]; then
    test_health
else
    echo "Usage:"
    echo "  ./test_curl.sh sync    - Test synchronous request"
    echo "  ./test_curl.sh async   - Test asynchronous request"
    echo "  ./test_curl.sh health  - Health check"
    echo ""
    echo "Running sync test by default..."
    echo ""
    test_sync
fi

echo ""
print_header "Done!"

