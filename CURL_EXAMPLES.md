# 🧪 cURL Test Examples للـ RunPod

أمثلة جاهزة لاختبار CP-VTON+ RunPod Endpoint باستخدام cURL

---

## ⚙️ Setup

```bash
# عدّل هنا بعد الـ deployment
ENDPOINT_ID="your-endpoint-id"
API_KEY="your-api-key"
```

---

## 1️⃣ Synchronous Request (موصى به)

### Simple Test

```bash
curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'"
    }
  }' | jq .
```

### With Output Format

```bash
curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'",
      "output_format": "PNG"
    }
  }' | jq .
```

### Save Result Image

```bash
# إرسال request وحفظ response
RESPONSE=$(curl -s -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'"
    }
  }')

# استخراج وحفظ الصورة
echo $RESPONSE | jq -r '.output.result_image' | base64 -d > result.png

echo "✅ Result saved to result.png"
```

---

## 2️⃣ Asynchronous Request

### Start Job

```bash
# بدء job async
RESPONSE=$(curl -s -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/run" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'"
    }
  }')

# احصل على Job ID
JOB_ID=$(echo $RESPONSE | jq -r '.id')
echo "Job ID: $JOB_ID"
```

### Check Status

```bash
# استعلام عن حالة الjob
curl -X GET "https://api.runpod.ai/v2/${ENDPOINT_ID}/status/${JOB_ID}" \
  -H "Authorization: Bearer ${API_KEY}" | jq .
```

### Poll Until Complete

```bash
# انتظار حتى الانتهاء
while true; do
  RESPONSE=$(curl -s -X GET \
    "https://api.runpod.ai/v2/${ENDPOINT_ID}/status/${JOB_ID}" \
    -H "Authorization: Bearer ${API_KEY}")
  
  STATUS=$(echo $RESPONSE | jq -r '.status')
  
  if [ "$STATUS" = "COMPLETED" ]; then
    echo "✅ Job completed!"
    echo $RESPONSE | jq .
    break
  elif [ "$STATUS" = "FAILED" ]; then
    echo "❌ Job failed"
    echo $RESPONSE | jq .
    break
  fi
  
  echo "Status: $STATUS, waiting..."
  sleep 2
done
```

---

## 3️⃣ Health Check

```bash
curl -X GET "https://api.runpod.ai/v2/${ENDPOINT_ID}/health" \
  -H "Authorization: Bearer ${API_KEY}" | jq .
```

---

## 4️⃣ Using Script (أسهل!)

```bash
# عدّل ENDPOINT_ID و API_KEY في test_curl.sh أولاً
chmod +x test_curl.sh

# Sync test
./test_curl.sh sync

# Async test
./test_curl.sh async

# Health check
./test_curl.sh health
```

---

## 📝 Response Format

### Success Response

```json
{
  "status": "COMPLETED",
  "output": {
    "success": true,
    "result_image": "<base64_image>",
    "output_size": [192, 256],
    "output_format": "PNG",
    "message": "Virtual try-on completed successfully"
  },
  "id": "job-id-here"
}
```

### Error Response

```json
{
  "status": "COMPLETED",
  "output": {
    "success": false,
    "error": "Error message here"
  },
  "id": "job-id-here"
}
```

---

## 🐛 Troubleshooting

### "401 Unauthorized"
→ تحقق من API_KEY

### "404 Not Found"
→ تحقق من ENDPOINT_ID

### "Invalid base64"
→ تأكد من استخدام `base64 -w 0` (Linux) أو `base64` (macOS)

### "Request timeout"
→ استخدم async request بدلاً من sync

---

## 💡 Tips

1. **استخدم `jq`** لعرض JSON بشكل أفضل:
   ```bash
   sudo apt install jq  # Ubuntu
   brew install jq      # macOS
   ```

2. **للصور الكبيرة:** استخدم async request

3. **للتجربة السريعة:** استخدم sync request

4. **لحفظ النتيجة:**
   ```bash
   echo $RESPONSE | jq -r '.output.result_image' | base64 -d > result.png
   ```

---

## 📊 Performance

### Typical Response Times

| Request Type | Time |
|-------------|------|
| Sync | 5-15s |
| Async (start) | <1s |
| Async (total) | 5-15s |

### Cold Start

أول request بعد فترة idle قد يأخذ 30-60s (cold start).

---

## 🔗 روابط مفيدة

- [RunPod API Docs](https://docs.runpod.io/serverless/endpoints/api)
- [test_curl.sh](test_curl.sh) - Automated test script
- [client_example.py](client_example.py) - Python client

---

## 🎯 Quick Test

أسرع طريقة للاختبار:

```bash
# 1. عدّل المتغيرات
ENDPOINT_ID="your-endpoint-id"
API_KEY="your-api-key"

# 2. Test!
curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'"
    }
  }' | jq .
```

---

**Done! 🎉**

