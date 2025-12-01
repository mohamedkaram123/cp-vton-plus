# 🎯 بعد الـ Build - الخطوات التالية

## ✅ أنت الآن هنا

لقد رفعت الكود على GitHub والـ Docker image اتبنى تلقائياً!

**Docker Image:** `ghcr.io/YOUR_USERNAME/YOUR_REPO:latest`

---

## 📋 الخطوات التالية (بالترتيب)

---

### الخطوة 1: تحميل Checkpoints 📦

**⚠️ مهم جداً:** الموديل مش هيشتغل بدون checkpoints!

#### 1a. حمّل Checkpoints على جهازك

**GMM Checkpoint (تحميل مباشر):**
```bash
wget -O gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"
```

**TOM Checkpoint (تحميل مباشر):**
```bash
wget -O tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

**الملفات المطلوبة:**
- `gmm_final.pth` (~76 MB)
- `tom_final.pth` (~85 MB)

حمّلهم على جهازك في أي مكان مؤقتاً.

---

#### 1b. أنشئ Network Storage على RunPod

1. **اذهب إلى:**
   ```
   https://www.runpod.io/console/storage
   ```

2. **اضغط:** "Create Network Volume"

3. **املأ:**
   ```
   Name: cpvton-checkpoints
   Size: 10 GB
   Region: اختر الأقرب ليك
   ```

4. **اضغط:** "Create"

---

#### 1c. ارفع Checkpoints على RunPod

بعد إنشاء الـ Network Volume:

1. **في صفحة Storage، اضغط:** "Browse Files" على الـ volume بتاعك

2. **أنشئ Folders:**
   - اضغط "New Folder" → اسمها `checkpoints`
   - ادخل جوا `checkpoints`
   - أنشئ folder اسمها `GMM`
   - أنشئ folder اسمها `TOM`

3. **ارفع الملفات:**
   - ادخل جوا `checkpoints/GMM/`
   - اضغط "Upload" → اختر `gmm_final.pth`
   - ارجع لـ `checkpoints/TOM/`
   - اضغط "Upload" → اختر `tom_final.pth`

**البنية النهائية:**
```
/checkpoints/
  ├── GMM/
  │   └── gmm_final.pth
  └── TOM/
      └── tom_final.pth
```

✅ **خلصنا الـ Checkpoints!**

---

### الخطوة 2: إنشاء Serverless Endpoint 🚀

#### 2a. اذهب إلى RunPod Serverless

```
https://www.runpod.io/console/serverless
```

#### 2b. اضغط "New Endpoint"

#### 2c. املأ البيانات

**📝 Basic Configuration:**

```yaml
Endpoint Name: cpvton-plus

Container Image: 
  ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
  
  # استبدل YOUR_USERNAME و YOUR_REPO بتاعك
  # مثال: ghcr.io/momo/cp-vton-plus:latest

Container Disk: 15 GB

Docker Command: (اتركها فاضية - default)
```

**🎮 GPU Selection:**

اختر واحد أو أكثر:
```
☑ RTX 3090 (24GB) - موصى به
☑ RTX 4090 (24GB) - الأسرع
☑ A4000 (16GB) - متوسط
☐ A6000 (48GB) - غالي (مش ضروري)
```

**📊 Scaling Configuration:**

```yaml
Workers Configuration:
  Min Workers: 0        # يبدأ من صفر (توفير تكلفة)
  Max Workers: 3        # أقصى عدد workers

Idle Timeout: 5 seconds  # وقت الـ idle قبل الـ shutdown

Advanced Scaling:
  GPU Utilization: 80%
  Request Rate Throttling: Off (عادي)
```

**⚙️ Advanced Settings:**

1. اضغط **"Advanced"**

2. **Network Storage (مهم!):**
   ```yaml
   Mount Path: /app/checkpoints
   Select Volume: cpvton-checkpoints
   ```

3. **Environment Variables (اختياري):**
   ```yaml
   GMM_CHECKPOINT: /app/checkpoints/GMM/gmm_final.pth
   TOM_CHECKPOINT: /app/checkpoints/TOM/tom_final.pth
   DEVICE: cuda
   ```

4. **FlashBoot (اختياري):**
   ```
   ☑ Enable FlashBoot (للسرعة)
   ```

#### 2d. اضغط "Deploy"

انتظر شوية... الـ endpoint هيبدأ deployment.

✅ **Endpoint جاهز!**

---

### الخطوة 3: احصل على Credentials 🔑

بعد الـ deployment:

#### 3a. Endpoint ID

في صفحة الـ endpoint، انسخ الـ **Endpoint ID**:

```
مثال: abc123xyz-serverless
```

احفظه في مكان آمن!

#### 3b. API Key

1. اذهب إلى: **Settings** (في القائمة العلوية)

2. اضغط: **API Keys**

3. انسخ الـ **API Key**:
   ```
   مثال: 1234567890abcdef...
   ```

احفظه في مكان آمن!

✅ **عندك الـ credentials!**

---

### الخطوة 4: اختبار الـ Endpoint 🧪

الآن جرب الـ endpoint!

#### Option 1: استخدام cURL (سريع)

```bash
# عدّل ENDPOINT_ID و API_KEY
ENDPOINT_ID="your-endpoint-id"
API_KEY="your-api-key"

# Test
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

**للتفاصيل:** [CURL_EXAMPLES.md](CURL_EXAMPLES.md)

#### Option 2: استخدام Python

```python
import requests
import base64
from PIL import Image
import io

ENDPOINT_ID = "your-endpoint-id"
API_KEY = "your-api-key"

# تحويل صورة لـ Base64
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Request
url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "input": {
        "person_image": img_to_b64("person.jpg"),
        "cloth_image": img_to_b64("cloth.jpg")
    }
}

print("🚀 Sending request...")
response = requests.post(url, json=payload, headers=headers)
result = response.json()

# معالجة النتيجة
if result["status"] == "COMPLETED":
    output = result["output"]
    if output["success"]:
        # حفظ الصورة
        img_data = base64.b64decode(output["result_image"])
        img = Image.open(io.BytesIO(img_data))
        img.save("result.png")
        print("✅ Success! Result: result.png")
    else:
        print(f"❌ Error: {output['error']}")
else:
    print(f"❌ Failed: {result}")
```

**للأمثلة الكاملة:** [client_example.py](client_example.py)

#### Option 3: استخدام Test Script

```bash
# عدّل ENDPOINT_ID و API_KEY في test_curl.sh
nano test_curl.sh

# Run
./test_curl.sh sync
```

✅ **الاختبار نجح!**

---

### الخطوة 5: مراقبة الأداء 📊

#### في RunPod Console

اذهب إلى: **Serverless** → **Your Endpoint**

**ستجد:**

1. **Metrics:**
   - Request Count
   - Average Duration
   - Error Rate
   - Total Cost

2. **Logs:**
   - Worker logs
   - Request logs
   - Error logs

3. **Workers:**
   - Active workers
   - Idle workers
   - Starting workers

#### مراقبة مباشرة

```bash
# شوف logs
# في RunPod Console → Your Endpoint → Logs

# أو استخدم API
curl -X GET "https://api.runpod.ai/v2/${ENDPOINT_ID}/status" \
  -H "Authorization: Bearer ${API_KEY}"
```

✅ **Monitoring فعال!**

---

## 🎯 Checklist

تأكد من إنك عملت:

- [ ] حمّلت checkpoints من Google Drive
- [ ] أنشأت Network Volume على RunPod
- [ ] رفعت checkpoints على الـ volume
- [ ] أنشأت Serverless Endpoint
- [ ] ربطت Network Storage بالـ endpoint
- [ ] حصلت على Endpoint ID و API Key
- [ ] اختبرت الـ endpoint (نجح!)
- [ ] شفت الـ logs والـ metrics

---

## 🎉 خلصنا!

**CP-VTON+ شغال على RunPod Serverless!**

### الخطوات كانت:

1. ✅ Build Docker image (GitHub Actions)
2. ✅ رفع checkpoints على Network Storage
3. ✅ Deploy Serverless Endpoint
4. ✅ اختبار API
5. ✅ مراقبة الأداء

---

## 📚 الخطوات التالية (اختياري)

### للاستخدام من Backend

استخدم الـ API في تطبيقك:

```python
# في backend بتاعك
from cpvton_client import CPVTONClient

client = CPVTONClient(
    endpoint_id=ENDPOINT_ID,
    api_key=API_KEY
)

result = client.try_on(person_img, cloth_img)
```

**راجع:** [client_example.py](client_example.py)

### للتحسين

1. **أضف Monitoring:**
   - Integrate مع Datadog / NewRelic
   - Track custom metrics

2. **أضف Caching:**
   - Cache متكرر requests
   - استخدم Redis

3. **حسّن الجودة:**
   - أضف human parsing (CIHP_PGN)
   - أضف pose detection (OpenPose)

**راجع:** [README_RUNPOD.md](README_RUNPOD.md) → Optimization

---

## 🐛 مشاكل شائعة

### "Worker failed to start"
→ تأكد من:
- الـ image موجود: `ghcr.io/username/repo:latest`
- Network Storage متربط صح
- Checkpoints موجودة في `/checkpoints/GMM/` و `/checkpoints/TOM/`

### "Model not loaded"
→ شوف الـ logs:
```
RunPod Console → Your Endpoint → Logs
```
ابحث عن "Model loading" errors

### "CUDA out of memory"
→ استخدم GPU أكبر (RTX 3090 أو RTX 4090)

### "Request timeout"
→ أول request ممكن ياخد وقت (cold start)
→ استخدم async request

**للمزيد:** [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) → Troubleshooting

---

## 💰 التكلفة الفعلية

### مع Auto-Scaling (0 → 3 workers)

**تدفع فقط عند الاستخدام!**

| Usage | Cost/Month |
|-------|-----------|
| 100 req/day | ~$2 |
| 1,000 req/day | ~$17 |
| 10,000 req/day | ~$170 |

**Cold Start:** أول request بعد idle قد ياخد 30-60s

**Solution:** استخدم Min Workers = 1 (للسرعة، بس بتدفع أكتر)

---

## 📞 الدعم

**عندك مشكلة؟**

1. شوف الـ **Logs** في RunPod Console
2. راجع [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md)
3. راجع [CURL_EXAMPLES.md](CURL_EXAMPLES.md)
4. افتح Issue على GitHub
5. تواصل RunPod Discord

---

## 🎊 مبروك!

**CP-VTON+ الآن live على RunPod Serverless!**

**استخدمه من أي تطبيق عبر REST API! 🚀**

---

*Need more help? Read [README_RUNPOD.md](README_RUNPOD.md)*

