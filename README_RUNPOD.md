# 🚀 CP-VTON+ على RunPod Serverless

دليل كامل لـ deployment CP-VTON+ على RunPod Serverless للاستخدام في production.

---

## 📋 جدول المحتويات

1. [نظرة عامة](#نظرة-عامة)
2. [البنية](#البنية)
3. [المتطلبات](#المتطلبات)
4. [الإعداد المحلي](#الإعداد-المحلي)
5. [بناء Docker Image](#بناء-docker-image)
6. [Deployment على RunPod](#deployment-على-runpod)
7. [استخدام الـ API](#استخدام-الـ-api)
8. [تحسينات للإنتاج](#تحسينات-للإنتاج)
9. [المشاكل الشائعة](#المشاكل-الشائعة)

---

## 🎯 نظرة عامة

تم تحويل CP-VTON+ إلى **serverless worker** يعمل على RunPod، مما يتيح:

- ✅ **Scalability**: يتوسع تلقائياً حسب الطلب
- ✅ **Pay-per-use**: تدفع فقط عند الاستخدام
- ✅ **GPU Access**: استخدام GPUs قوية بدون تكلفة ثابتة
- ✅ **REST API**: استدعاء بسيط من أي backend

---

## 📁 البنية

```
cp-vton-plus/
├── cpvton_infer.py          # كلاس wrapper للموديل
├── handler.py               # RunPod serverless handler
├── Dockerfile               # Docker image config
├── requirements_runpod.txt  # Python dependencies
├── download_checkpoints.sh  # script لتحميل checkpoints
├── runpod_test.py          # اختبار محلي
├── README_RUNPOD.md        # هذا الملف
│
├── networks.py             # CP-VTON+ networks (أصلي)
├── visualization.py        # Visualization utilities (أصلي)
├── grid.png               # Grid image (مطلوب للـ GMM)
│
└── checkpoints/           # يجب تحميلهم
    ├── GMM/
    │   └── gmm_final.pth
    └── TOM/
        └── tom_final.pth
```

---

## 🔧 المتطلبات

### 1. Software

- Docker (>= 20.10)
- Python 3.8+ (للاختبار المحلي)
- حساب على [RunPod](https://runpod.io)
- حساب Docker Hub أو GitHub Container Registry

### 2. Hardware (للتشغيل المحلي)

- GPU مع CUDA support (مفضل)
- 8GB+ RAM
- 10GB+ مساحة تخزين

### 3. Checkpoints

يجب تحميل checkpoints من Google Drive:

**تحميل مباشر:**
```bash
# GMM
wget "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_" \
  -O gmm_final.pth

# TOM
wget "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT" \
  -O tom_final.pth
```

الملفات المطلوبة:
- `checkpoints/GMM/gmm_final.pth` (~80MB)
- `checkpoints/TOM/tom_final.pth` (~180MB)

---

## 🏠 الإعداد المحلي

### 1. تحميل Checkpoints

```bash
# طريقة 1: يدوياً
# افتح الرابط وحمل الملفات وضعهم في checkpoints/

# طريقة 2: باستخدام script
chmod +x download_checkpoints.sh
./download_checkpoints.sh
```

### 2. تثبيت Dependencies

```bash
pip install -r requirements_runpod.txt
```

### 3. اختبار محلي

```bash
# اختبار بسيط بصور dummy
python runpod_test.py

# اختبار بصور حقيقية
python runpod_test.py path/to/person.jpg path/to/cloth.jpg
```

---

## 🐳 بناء Docker Image

### 1. Build

```bash
# بناء الimage
docker build -t your-username/cpvton-runpod:latest .

# أو مع tag محدد
docker build -t your-username/cpvton-runpod:v1.0.0 .
```

**ملاحظة:** يجب استبدال `your-username` باسم المستخدم على Docker Hub.

### 2. Test محلياً

```bash
# تشغيل الcontainer محلياً (مع GPU)
docker run --gpus all -p 8000:8000 \
  -v $(pwd)/checkpoints:/app/checkpoints \
  your-username/cpvton-runpod:latest

# بدون GPU (للاختبار فقط)
docker run -p 8000:8000 \
  -v $(pwd)/checkpoints:/app/checkpoints \
  -e DEVICE=cpu \
  your-username/cpvton-runpod:latest
```

### 3. Push إلى Registry

```bash
# تسجيل دخول
docker login

# رفع الimage
docker push your-username/cpvton-runpod:latest
```

---

## ☁️ Deployment على RunPod

### 1. رفع Checkpoints

**الطريقة المفضلة:** استخدام RunPod Network Storage

1. اذهب إلى RunPod Dashboard → Storage
2. أنشئ Network Volume جديد (10GB كافي)
3. ارفع checkpoints:

```bash
# Mount Network Storage محلياً (حسب تعليمات RunPod)
rsync -avz checkpoints/ /path/to/mounted/storage/checkpoints/
```

**بديل:** دمج checkpoints في Docker image (يزيد الحجم):

```dockerfile
# في Dockerfile، uncomment:
RUN wget -O /app/checkpoints/GMM/gmm_final.pth https://your-url/gmm_final.pth
RUN wget -O /app/checkpoints/TOM/tom_final.pth https://your-url/tom_final.pth
```

### 2. إنشاء Serverless Endpoint

1. اذهب إلى [RunPod Console](https://www.runpod.io/console/serverless)
2. اضغط **"New Endpoint"**
3. املأ البيانات:

   - **Name:** `cpvton-plus`
   - **Select GPU:**
     - **مبتدئ:** RTX 4000 (8GB VRAM) - ~$0.20/hr
     - **متوسط:** RTX 3090 (24GB VRAM) - ~$0.40/hr
     - **متقدم:** A4000 (16GB VRAM) - ~$0.60/hr
   - **Container Image:** `your-username/cpvton-runpod:latest`
   - **Container Disk:** 15GB
   - **Environment Variables:** (اختياري)
     ```
     GMM_CHECKPOINT=/app/checkpoints/GMM/gmm_final.pth
     TOM_CHECKPOINT=/app/checkpoints/TOM/tom_final.pth
     DEVICE=cuda
     ```

4. **Scaling Settings:**
   - **Workers:** 0 (auto-scale من صفر)
   - **Max Workers:** 3-5 (حسب الحاجة)
   - **Idle Timeout:** 5 seconds
   - **GPU Utilization:** 80%

5. إذا استخدمت Network Storage:
   - في **"Advanced"** → **"Network Storage"**
   - اختر الvolume
   - Mount path: `/app/checkpoints`

6. اضغط **"Create Endpoint"**

### 3. الحصول على API Key

1. اذهب إلى **Settings** → **API Keys**
2. انسخ API Key (تحتاجه للاستدعاءات)

---

## 📡 استخدام الـ API

### Format

```
POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

### Python Example

```python
import requests
import base64

ENDPOINT_ID = "your-endpoint-id"
API_KEY = "your-api-key"

def to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# تجهيز الصور
person_b64 = to_base64("person.jpg")
cloth_b64 = to_base64("cloth.jpg")

# Request payload
payload = {
    "input": {
        "person_image": person_b64,
        "cloth_image": cloth_b64,
        "output_format": "PNG"
    }
}

# إرسال Request
url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

# حفظ النتيجة
if result.get("status") == "COMPLETED":
    output = result["output"]
    if output.get("success"):
        result_b64 = output["result_image"]
        with open("result.png", "wb") as f:
            f.write(base64.b64decode(result_b64))
        print("✅ نجح!")
    else:
        print(f"❌ خطأ: {output.get('error')}")
else:
    print(f"❌ فشل: {result}")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');
const fs = require('fs');

const ENDPOINT_ID = 'your-endpoint-id';
const API_KEY = 'your-api-key';

async function tryOn(personPath, clothPath) {
  // قراءة الصور كـ Base64
  const personB64 = fs.readFileSync(personPath, 'base64');
  const clothB64 = fs.readFileSync(clothPath, 'base64');

  // Request
  const response = await axios.post(
    `https://api.runpod.ai/v2/${ENDPOINT_ID}/runsync`,
    {
      input: {
        person_image: personB64,
        cloth_image: clothB64,
        output_format: 'PNG'
      }
    },
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  );

  // معالجة النتيجة
  if (response.data.status === 'COMPLETED') {
    const output = response.data.output;
    if (output.success) {
      const resultB64 = output.result_image;
      fs.writeFileSync('result.png', Buffer.from(resultB64, 'base64'));
      console.log('✅ نجح!');
    } else {
      console.error('❌ خطأ:', output.error);
    }
  }
}

tryOn('person.jpg', 'cloth.jpg');
```

### cURL Example

```bash
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'",
      "output_format": "PNG"
    }
  }'
```

---

## 🎯 تحسينات للإنتاج

### 1. إضافة Parsing & Pose Detection

لنتائج أفضل، يجب إضافة:

**A. Human Parsing (CIHP_PGN / Graphonomy)**

```python
# في cpvton_infer.py
def parse_person(self, person_img):
    # استخدم CIHP_PGN أو Graphonomy
    # لتوليد parsing map
    pass
```

**B. Pose Estimation (OpenPose)**

```python
def detect_pose(self, person_img):
    # استخدم OpenPose COCO-18
    # لتوليد keypoints
    pass
```

راجع [CP-VTON+ README](README.md) في قسم "Testing with custom images".

### 2. Caching & Optimization

```python
# في cpvton_infer.py
from functools import lru_cache

@lru_cache(maxsize=100)
def preprocess_cached(self, image_hash):
    # Cache معالجة الصور المتكررة
    pass
```

### 3. Batch Processing

```python
# في handler.py
def handler(event):
    inp = event.get("input", {})
    
    # دعم batch
    if "batch" in inp:
        person_images = [decode_image(b64) for b64 in inp["batch"]["person_images"]]
        cloth_images = [decode_image(b64) for b64 in inp["batch"]["cloth_images"]]
        
        results = model.try_on_batch(person_images, cloth_images)
        return {"results": [encode_image(r) for r in results]}
```

### 4. Monitoring

استخدم RunPod Metrics + Custom Logging:

```python
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(event):
    start_time = time.time()
    
    try:
        # ... معالجة
        
        duration = time.time() - start_time
        logger.info(f"Request completed in {duration:.2f}s")
        
        return {"result": ..., "duration": duration}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

---

## 🐛 المشاكل الشائعة

### 1. "Model not loaded properly"

**السبب:** Checkpoints غير موجودة أو تالفة.

**الحل:**
```bash
# تحقق من وجود الملفات
ls -lh checkpoints/GMM/gmm_final.pth
ls -lh checkpoints/TOM/tom_final.pth

# تحقق من حجم الملفات
# GMM: ~80MB, TOM: ~180MB
```

### 2. CUDA Out of Memory

**السبب:** GPU صغيرة أو batch size كبير.

**الحل:**
- استخدم GPU أكبر (A4000 بدلاً من RTX 4000)
- قلل batch size
- استخدم `torch.cuda.empty_cache()`

### 3. Slow Inference

**السبب:** Cold start أو preprocessing بطيء.

**الحل:**
- استخدم RunPod "Active Workers" (بدلاً من auto-scale من 0)
- Cache preprocessing results
- استخدم mixed precision: `torch.cuda.amp`

### 4. Poor Quality Results

**السبب:** استخدام dummy parsing/pose بدلاً من الحقيقي.

**الحل:**
- أضف CIHP_PGN / Graphonomy للـ parsing
- أضف OpenPose للـ pose detection
- راجع [CP-VTON+ README](README.md)

---

## 💰 تقدير التكلفة

### مثال: 1000 request/يوم

**GPU:** RTX 3090 (~$0.40/hr)

- **Inference time:** ~5 seconds/request
- **Cold start:** ~30 seconds (مرة واحدة)
- **Total GPU time:** (1000 × 5s + 30s) / 3600 ≈ **1.4 hours/day**

**التكلفة:**
- **يومياً:** 1.4 × $0.40 = **$0.56**
- **شهرياً:** $0.56 × 30 = **$16.80**

**مع Scaling:**
- إذا كان الطلب غير منتظم، التكلفة أقل (pay-per-use)
- مع cold start optimization، يمكن تقليل التكلفة 20-30%

---

## 📚 موارد إضافية

- [CP-VTON+ Paper](https://minar09.github.io/cpvtonplus/)
- [RunPod Docs](https://docs.runpod.io/)
- [PyTorch CUDA Guide](https://pytorch.org/docs/stable/cuda.html)
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- [CIHP_PGN](https://github.com/Engineering-Course/CIHP_PGN)

---

## 🤝 المساهمة

إذا عندك تحسينات أو fixes:

1. Fork الريبو
2. إنشاء branch (`git checkout -b feature/improvement`)
3. Commit التغييرات
4. Push وإنشاء Pull Request

---

## 📄 License

نفس license الأصلي للـ CP-VTON+. راجع [LICENSE](LICENSE).

---

## ✉️ الدعم

- GitHub Issues: للمشاكل التقنية
- RunPod Discord: لمشاكل الـ deployment

---

**تم بناؤه بـ ❤️ للـ CP-VTON+ Community**


