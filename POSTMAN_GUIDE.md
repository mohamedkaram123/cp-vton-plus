# 🚀 اختبار CP-VTON+ API في Postman

دليل كامل لاختبار RunPod Endpoint باستخدام Postman

---

## 📥 Setup Postman

### 1. تحميل Postman (إذا مش موجود)

```
https://www.postman.com/downloads/
```

أو استخدم **Postman Web** مباشرة:
```
https://web.postman.co/
```

---

## 🎯 طريقة 1: Request بسيط (Sync)

### الخطوة 1: إنشاء Request جديد

1. افتح Postman
2. اضغط **"New"** → **"HTTP Request"**
3. أو اضغط **"+"** لفتح tab جديد

---

### الخطوة 2: ضبط Request

#### 📍 URL

```
Method: POST
URL: https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
```

**عدّل `YOUR_ENDPOINT_ID`** بالـ endpoint ID بتاعك من RunPod!

مثال:
```
https://api.runpod.ai/v2/abc123xyz-serverless/runsync
```

---

#### 🔑 Headers

اضغط **"Headers"** tab وأضف:

| Key | Value |
|-----|-------|
| `Authorization` | `Bearer YOUR_API_KEY` |
| `Content-Type` | `application/json` |

**عدّل `YOUR_API_KEY`** بالـ API key بتاعك من RunPod!

مثال:
```
Authorization: Bearer 1234567890abcdef...
Content-Type: application/json
```

---

#### 📄 Body

اضغط **"Body"** tab ثم:
1. اختر **"raw"**
2. اختار **"JSON"** من القائمة المنسدلة

**الكود:**

```json
{
  "input": {
    "person_image": "BASE64_PERSON_IMAGE_HERE",
    "cloth_image": "BASE64_CLOTH_IMAGE_HERE",
    "output_format": "PNG"
  }
}
```

---

### الخطوة 3: تحويل الصور لـ Base64

⚠️ **مهم:** لازم تحول الصور لـ Base64 أولاً!

#### Option A: استخدام Terminal

```bash
# Linux/Mac
base64 -w 0 person.jpg
base64 -w 0 cloth.jpg

# Windows (PowerShell)
[Convert]::ToBase64String([IO.File]::ReadAllBytes("person.jpg"))
```

#### Option B: استخدام Online Tool

```
https://www.base64-image.de/
```

1. Upload صورة
2. انسخ Base64 output
3. الصقه في JSON

#### Option C: استخدام Pre-request Script في Postman

في tab **"Pre-request Script"**:

```javascript
// ملاحظة: هذا مثال - Postman لا يدعم قراءة ملفات محلية مباشرة
// استخدم Terminal أو Online tool أفضل
```

---

### الخطوة 4: مثال كامل

**Body (JSON):**

```json
{
  "input": {
    "person_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "cloth_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
    "output_format": "PNG"
  }
}
```

*(هذه صور dummy صغيرة جداً - استبدلها بصورك الحقيقية)*

---

### الخطوة 5: إرسال Request

1. اضغط **"Send"**
2. انتظر النتيجة (5-15 ثانية)
3. شوف الـ Response في الأسفل

---

### الخطوة 6: قراءة Response

**Success Response:**

```json
{
  "status": "COMPLETED",
  "output": {
    "success": true,
    "result_image": "iVBORw0KGg...(base64 صورة النتيجة)",
    "output_size": [192, 256],
    "output_format": "PNG",
    "message": "Virtual try-on completed successfully"
  },
  "id": "job-id-here"
}
```

**Error Response:**

```json
{
  "status": "COMPLETED",
  "output": {
    "success": false,
    "error": "Error message here"
  }
}
```

---

### الخطوة 7: حفظ النتيجة

لحفظ الصورة من Base64:

1. **انسخ** الـ `result_image` من Response
2. استخدم **Online Decoder:**
   ```
   https://www.base64-image.de/
   ```
3. الصق Base64 وحمّل الصورة

أو استخدم **Terminal:**

```bash
# احفظ Base64 في ملف
echo "BASE64_HERE" > result.txt

# حوله لصورة
base64 -d result.txt > result.png
```

---

## 🎯 طريقة 2: استخدام Postman Collection

### إنشاء Collection

1. اضغط **"Collections"** في الـ sidebar
2. اضغط **"+"** → **"Create Collection"**
3. اسمها: `CP-VTON+ API`

---

### إضافة Variables

في الـ Collection settings:

1. اضغط **"..."** على الـ collection
2. اختر **"Edit"**
3. اذهب لـ **"Variables"** tab
4. أضف:

| Variable | Initial Value | Current Value |
|----------|--------------|---------------|
| `endpoint_id` | `your-endpoint-id` | `your-endpoint-id` |
| `api_key` | `your-api-key` | `your-api-key` |
| `base_url` | `https://api.runpod.ai/v2` | `https://api.runpod.ai/v2` |

---

### إنشاء Request في Collection

الآن في الـ Request:

**URL:**
```
{{base_url}}/{{endpoint_id}}/runsync
```

**Headers:**
```
Authorization: Bearer {{api_key}}
Content-Type: application/json
```

---

## 🔄 طريقة 3: Async Request

### Start Job

**URL:**
```
POST https://api.runpod.ai/v2/{{endpoint_id}}/run
```

**Body:**
```json
{
  "input": {
    "person_image": "BASE64_HERE",
    "cloth_image": "BASE64_HERE"
  }
}
```

**Response:**
```json
{
  "id": "job-123-abc",
  "status": "IN_QUEUE"
}
```

احفظ الـ `id`!

---

### Check Status

**URL:**
```
GET https://api.runpod.ai/v2/{{endpoint_id}}/status/JOB_ID
```

استبدل `JOB_ID` بالـ ID من Response السابق.

**Response:**
```json
{
  "status": "COMPLETED",
  "output": {
    "success": true,
    "result_image": "..."
  }
}
```

---

## 🛠️ Pre-request Script لتحويل الصور

### في Postman Pre-request Script

**⚠️ للأسف Postman لا يدعم قراءة ملفات محلية!**

**Workaround:**

1. **استخدم Base64 Environment Variable:**

```javascript
// في Pre-request Script
pm.environment.set("person_b64", "YOUR_BASE64_HERE");
pm.environment.set("cloth_b64", "YOUR_BASE64_HERE");
```

2. **في Body:**
```json
{
  "input": {
    "person_image": "{{person_b64}}",
    "cloth_image": "{{cloth_b64}}"
  }
}
```

---

## 📝 Tests Script (للتحقق التلقائي)

في **"Tests"** tab:

```javascript
// تحقق من Status Code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// تحقق من Success
pm.test("Request completed", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql("COMPLETED");
});

pm.test("Virtual try-on succeeded", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.output.success).to.be.true;
});

// حفظ Result Image كـ Environment Variable
var jsonData = pm.response.json();
if (jsonData.output && jsonData.output.result_image) {
    pm.environment.set("result_image", jsonData.output.result_image);
    console.log("✅ Result image saved to environment");
}
```

---

## 📦 Export/Import Postman Collection

### Export

1. اضغط **"..."** على الـ collection
2. **"Export"**
3. اختر **"Collection v2.1"**
4. احفظ الملف

### Share

شارك الـ JSON file مع فريقك!

---

## 🎨 مثال Collection JSON

```json
{
  "info": {
    "name": "CP-VTON+ API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Virtual Try-On (Sync)",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{api_key}}"
          },
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"input\": {\n    \"person_image\": \"{{person_b64}}\",\n    \"cloth_image\": \"{{cloth_b64}}\",\n    \"output_format\": \"PNG\"\n  }\n}"
        },
        "url": {
          "raw": "{{base_url}}/{{endpoint_id}}/runsync",
          "host": ["{{base_url}}"],
          "path": ["{{endpoint_id}}", "runsync"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "https://api.runpod.ai/v2"
    },
    {
      "key": "endpoint_id",
      "value": "your-endpoint-id"
    },
    {
      "key": "api_key",
      "value": "your-api-key"
    }
  ]
}
```

احفظ هذا في ملف `cpvton-postman-collection.json` وافتحه في Postman!

---

## 🐛 Troubleshooting

### "401 Unauthorized"
→ تحقق من API Key في Headers

### "404 Not Found"
→ تحقق من Endpoint ID في URL

### "400 Bad Request"
→ تحقق من:
- Body format (لازم JSON صحيح)
- Base64 encoding صحيح
- Keys: `person_image`, `cloth_image`

### Response بطيء
→ عادي! أول request قد ياخد 30-60s (cold start)

---

## 💡 Tips

1. **حفظ Base64 في Environment:**
   - عشان ما تكبر الـ request
   - سهل التعديل

2. **استخدام Collection Variables:**
   - endpoint_id
   - api_key
   - base_url

3. **Tests Scripts:**
   - للتحقق التلقائي من النتائج

4. **Save Response:**
   - Postman يحفظ history تلقائياً
   - يمكنك مراجعة requests سابقة

---

## 📸 Quick Reference

### Request Template

```
POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync

Headers:
  Authorization: Bearer YOUR_API_KEY
  Content-Type: application/json

Body (JSON):
{
  "input": {
    "person_image": "BASE64_PERSON",
    "cloth_image": "BASE64_CLOTH",
    "output_format": "PNG"
  }
}
```

---

## 🔗 موارد مفيدة

- [Base64 Encoder/Decoder](https://www.base64-image.de/)
- [Postman Learning Center](https://learning.postman.com/)
- [JSON Validator](https://jsonlint.com/)

---

## ✅ Checklist

قبل إرسال Request:

- [ ] عدّلت `endpoint_id` في URL
- [ ] عدّلت `api_key` في Headers
- [ ] حولت الصور لـ Base64
- [ ] الصقت Base64 في Body
- [ ] اخترت POST method
- [ ] اخترت JSON في Body

---

**🎉 جاهز! اضغط Send!**

---

*Need help? Check [CURL_EXAMPLES.md](CURL_EXAMPLES.md) for cURL alternatives*

