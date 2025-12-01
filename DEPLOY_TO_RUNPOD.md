# 🚀 Deploy مباشرة على RunPod Serverless (بدون Local)

## الطريقة السريعة - GitHub → RunPod

---

## ✅ الخطوات الكاملة

### 1️⃣ رفع على GitHub

```bash
# في terminal الخاص بك
cd /home/momo/dev/cp-vton-plus

# Initialize git (إذا لم يكن موجود)
git init

# Add all files
git add .

# Commit
git commit -m "CP-VTON+ RunPod Serverless ready"

# أضف remote (عدّل USERNAME و REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push
git branch -M main
git push -u origin main
```

---

### 2️⃣ Build Docker على GitHub (تلقائي)

الكود جاهز بـ GitHub Actions! بمجرد الـ push، GitHub هيبني الـ Docker image تلقائياً.

**الـ image سيكون:**
```
ghcr.io/USERNAME/REPO_NAME:latest
```

**أو استخدم Docker Hub يدوياً:**

1. اذهب إلى https://hub.docker.com
2. أنشئ repository جديد: `cpvton-runpod`
3. اربط GitHub repo بـ Docker Hub (Automated Builds)
4. أو استخدم GitHub Actions (موجود جاهز)

---

### 3️⃣ تحميل Checkpoints على RunPod Network Storage

**⚠️ مهم جداً:** Checkpoints ضروري للموديل!

#### Option A: استخدام RunPod Network Storage (مُفضَّل)

1. **اذهب إلى RunPod Console:**
   https://www.runpod.io/console/storage

2. **أنشئ Network Volume:**
   - Name: `cpvton-checkpoints`
   - Size: 10 GB
   - Region: اختر قريب منك

3. **رفع Checkpoints:**
   
   **3a. حمّل Checkpoints محلياً أولاً:**
   ```bash
   # تحميل مباشر من Google Drive:
   # wget "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_" -O gmm_final.pth
   # wget "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT" -O tom_final.pth
   
   mkdir -p checkpoints/GMM checkpoints/TOM
   # ضع gmm_final.pth في checkpoints/GMM/
   # ضع tom_final.pth في checkpoints/TOM/
   ```

   **3b. استخدم RunPod File Manager لرفعهم:**
   - من RunPod Console → Network Storage → Browse
   - أنشئ folders: `/checkpoints/GMM` و `/checkpoints/TOM`
   - ارفع `gmm_final.pth` و `tom_final.pth`

   **أو استخدم `rsync`/`scp` (إذا مفعّل SSH):**
   ```bash
   # RunPod سيعطيك SSH command
   rsync -avz checkpoints/ runpod@xxx:/workspace/checkpoints/
   ```

#### Option B: استخدام Public URL

إذا حطيت الcheckpoints على cloud storage (Google Drive, S3, etc.):

عدّل `Dockerfile`:
```dockerfile
# قبل CMD، أضف:
RUN wget -O /app/checkpoints/GMM/gmm_final.pth https://YOUR_URL/gmm_final.pth
RUN wget -O /app/checkpoints/TOM/tom_final.pth https://YOUR_URL/tom_final.pth
```

---

### 4️⃣ إنشاء RunPod Serverless Endpoint

1. **اذهب إلى:**
   https://www.runpod.io/console/serverless

2. **اضغط "New Endpoint"**

3. **املأ البيانات:**

   ```
   Endpoint Name: cpvton-plus
   
   Container Image:
     ghcr.io/USERNAME/REPO_NAME:latest
     (أو your-dockerhub-user/cpvton-runpod:latest)
   
   Container Disk: 15 GB
   
   GPU Types:
     ☑ RTX 3090 (24GB) - جيد جداً
     ☑ RTX 4090 (24GB) - الأفضل
     ☑ A4000 (16GB) - متوسط
   
   Scaling:
     Min Workers: 0
     Max Workers: 3
     Idle Timeout: 5 seconds
     GPU Utilization: 80%
   
   Advanced:
     ☑ Enable FlashBoot (للسرعة)
   ```

4. **إذا استخدمت Network Storage:**
   - في Advanced → Network Storage
   - Mount Path: `/app/checkpoints`
   - Select Volume: `cpvton-checkpoints`

5. **Environment Variables (اختياري):**
   ```
   GMM_CHECKPOINT=/app/checkpoints/GMM/gmm_final.pth
   TOM_CHECKPOINT=/app/checkpoints/TOM/tom_final.pth
   DEVICE=cuda
   ```

6. **اضغط "Deploy"**

---

### 5️⃣ احصل على API Credentials

1. بعد Deploy، انسخ **Endpoint ID**:
   ```
   مثال: abc123xyz-serverless
   ```

2. اذهب إلى Settings → API Keys
   
3. انسخ **API Key**:
   ```
   مثال: 1234567890abcdef...
   ```

---

### 6️⃣ اختبار من أي مكان

**Python Client:**

```python
import requests
import base64
from PIL import Image
import io

ENDPOINT_ID = "abc123xyz-serverless"  # عدّل هنا
API_KEY = "your-api-key-here"          # عدّل هنا

def test_tryon():
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
    
    print("🚀 إرسال request...")
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if result.get("status") == "COMPLETED":
        output = result["output"]
        if output.get("success"):
            # حفظ النتيجة
            img_data = base64.b64decode(output["result_image"])
            img = Image.open(io.BytesIO(img_data))
            img.save("result.png")
            print("✅ نجح! النتيجة في result.png")
        else:
            print(f"❌ خطأ: {output.get('error')}")
    else:
        print(f"❌ فشل: {result}")

test_tryon()
```

**cURL Test:**

```bash
# عدّل ENDPOINT_ID و API_KEY
ENDPOINT_ID="your-endpoint-id"
API_KEY="your-api-key"

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

## 📊 متابعة الـ Endpoint

### مراقبة الأداء

في RunPod Console → Serverless → Your Endpoint:

- **Requests:** عدد الطلبات
- **Duration:** متوسط وقت المعالجة
- **Errors:** نسبة الأخطاء
- **Cost:** التكلفة

### Logs

```
Console → Serverless → Your Endpoint → Logs
```

شوف logs الworkers للـ debugging.

---

## 🔧 Troubleshooting

### "Container failed to start"

**السبب:** غالباً الcheckpoints مش موجودة

**الحل:**
1. تأكد من mount الـ Network Storage صح
2. تأكد من الpaths:
   ```
   /app/checkpoints/GMM/gmm_final.pth
   /app/checkpoints/TOM/tom_final.pth
   ```

### "CUDA out of memory"

**الحل:**
- استخدم GPU أكبر (RTX 3090 بدلاً من A4000)
- قلل batch size

### "Request timeout"

**الحل:**
- زود timeout في client
- استخدم async API بدلاً من sync

### "Model inference is slow"

**الحل:**
- فعّل FlashBoot
- استخدم Active Workers (بدلاً من 0)
- استخدم GPU أسرع

---

## 💰 تقدير التكلفة

### RTX 3090 (~$0.40/hour)

| Requests/Day | GPU Time | Cost/Day | Cost/Month |
|-------------|----------|----------|------------|
| 100         | ~0.14h   | $0.06    | $1.80      |
| 1,000       | ~1.4h    | $0.56    | $16.80     |
| 10,000      | ~14h     | $5.60    | $168       |

**ملاحظة:** مع auto-scaling من 0، تدفع فقط عند الاستخدام!

---

## 📝 Checklist

قبل Deploy:

- [ ] رفعت الكود على GitHub
- [ ] حمّلت checkpoints على Network Storage
- [ ] أنشأت Endpoint على RunPod
- [ ] ربطت Network Storage بالـ endpoint
- [ ] نسخت Endpoint ID و API Key
- [ ] اختبرت API

---

## 🎯 Next Steps

### للإنتاج الحقيقي:

1. **أضف Authentication:**
   ```python
   # في handler.py
   def verify_api_key(event):
       api_key = event.get("api_key")
       if api_key != "your-secret-key":
           return {"error": "Unauthorized"}
   ```

2. **أضف Rate Limiting:**
   استخدم Redis أو RunPod built-in features

3. **أضف Monitoring:**
   - Integrate مع Datadog/NewRelic
   - Track metrics (latency, errors, usage)

4. **حسّن الجودة:**
   - أضف CIHP_PGN للـ parsing
   - أضف OpenPose للـ pose detection

---

## 🆘 الدعم

**عندك مشكلة؟**

1. شوف Logs في RunPod Console
2. اختبر Container محلياً (اختياري):
   ```bash
   docker run --gpus all \
     -v /path/to/checkpoints:/app/checkpoints \
     ghcr.io/username/repo:latest
   ```
3. افتح Issue على GitHub
4. تواصل RunPod Discord

---

## 🎉 خلصنا!

الآن CP-VTON+ شغال على RunPod Serverless!

**الخطوات كانت:**
1. ✅ Push على GitHub
2. ✅ Docker image built تلقائياً
3. ✅ رفع checkpoints على Network Storage
4. ✅ Deploy Endpoint على RunPod
5. ✅ اختبار API

**جاهز للاستخدام! 🚀**

---

## 🔗 روابط مفيدة

- [RunPod Console](https://www.runpod.io/console)
- [RunPod Docs](https://docs.runpod.io/)
- [GitHub Actions](https://docs.github.com/actions)
- [Docker Hub](https://hub.docker.com/)

---

*Built with ❤️ - جاهز للإنتاج!*


