# 🏗️ بنية المشروع - CP-VTON+ RunPod

## 📂 هيكل الملفات

```
cp-vton-plus/
│
├── 📦 الكود الأصلي (CP-VTON+)
│   ├── networks.py              # GMM & TOM models
│   ├── cp_dataset.py            # Dataset loader
│   ├── train.py                 # Training script
│   ├── test.py                  # Testing script
│   ├── visualization.py         # Visualization utilities
│   └── grid.png                 # Grid image للـ GMM
│
├── 🚀 الكود الجديد (RunPod Integration)
│   ├── cpvton_infer.py          # ⭐ كلاس wrapper للموديل
│   ├── handler.py               # ⭐ RunPod serverless handler
│   ├── client_example.py        # ⭐ أمثلة استخدام API
│   └── runpod_test.py          # ⭐ اختبار محلي
│
├── 🐳 Docker & Dependencies
│   ├── Dockerfile               # ⭐ Docker image definition
│   ├── requirements_runpod.txt  # ⭐ Python dependencies
│   ├── .dockerignore           # ⭐ Docker build exclusions
│   └── .env.example            # ⭐ Environment variables template
│
├── 🛠️ Scripts & Automation
│   ├── build_and_push.sh       # ⭐ Build & push Docker image
│   └── download_checkpoints.sh # ⭐ Download model checkpoints
│
├── 📚 التوثيق
│   ├── README.md               # README الأصلي لـ CP-VTON+
│   ├── RUN_ME_FIRST.md         # ⭐ نقطة البداية
│   ├── QUICKSTART.md           # ⭐ بداية سريعة
│   ├── README_RUNPOD.md        # ⭐ دليل شامل
│   ├── DEPLOYMENT_SUMMARY.md   # ⭐ ملخص التطبيق
│   └── PROJECT_STRUCTURE.md    # ⭐ هذا الملف
│
├── 📁 Data & Checkpoints
│   ├── data/                   # Dataset (train/test)
│   │   ├── train/
│   │   └── test/
│   │       ├── image/          # Person images
│   │       ├── cloth/          # Cloth images
│   │       ├── image-parse/    # Parsing maps
│   │       ├── pose/           # Pose keypoints
│   │       └── cloth-mask/     # Cloth masks
│   │
│   └── checkpoints/            # Model checkpoints (محتاج تحميل)
│       ├── GMM/
│       │   └── gmm_final.pth   # ~80MB
│       └── TOM/
│           └── tom_final.pth   # ~180MB
│
└── 📄 Other
    ├── LICENSE                 # License
    ├── CITATION.cff           # Citation info
    └── requirements.txt       # Original requirements
```

---

## 🎯 الملفات الرئيسية

### 1️⃣ cpvton_infer.py
**الغرض:** تغليف CP-VTON+ في كلاس Python بسيط

**الوظائف الرئيسية:**
- `CPVTONPlusModel.__init__()` - تحميل GMM & TOM
- `try_on(person_img, cloth_img)` - Virtual try-on
- `try_on_batch()` - Batch processing

**الاستخدام:**
```python
model = CPVTONPlusModel()
result = model.try_on(person_img, cloth_img)
```

---

### 2️⃣ handler.py
**الغرض:** RunPod Serverless handler

**الوظيفة الرئيسية:**
- `handler(event)` - معالجة RunPod requests

**Input:**
```json
{
  "input": {
    "person_image": "<base64>",
    "cloth_image": "<base64>"
  }
}
```

**Output:**
```json
{
  "result_image": "<base64>",
  "success": true
}
```

---

### 3️⃣ Dockerfile
**الغرض:** بناء Docker image للـ deployment

**الخطوات:**
1. Base image: `nvidia/cuda:11.8.0`
2. تثبيت Python & dependencies
3. نسخ الكود
4. تحديد entrypoint: `handler.py`

**البناء:**
```bash
docker build -t your-user/cpvton-runpod:latest .
```

---

### 4️⃣ client_example.py
**الغرض:** أمثلة استخدام API من Backend

**الأمثلة:**
- `example_sync()` - Synchronous request
- `example_async()` - Asynchronous request
- `example_batch()` - Batch processing

**الاستخدام:**
```python
from client_example import CPVTONClient

client = CPVTONClient(endpoint_id, api_key)
result = client.try_on_sync(person, cloth)
```

---

## 🔄 كيف تعمل الأجزاء معاً؟

### Development Flow
```
1. تطوير/تعديل cpvton_infer.py
   ↓
2. اختبار محلي: python runpod_test.py
   ↓
3. بناء Docker: ./build_and_push.sh
   ↓
4. Deploy على RunPod
   ↓
5. اختبار API: python client_example.py
```

### Runtime Flow
```
Client Request (Base64 images)
   ↓
RunPod API
   ↓
handler.py (decode images)
   ↓
cpvton_infer.py (inference)
   ↓
GMM (geometric matching)
   ↓
TOM (try-on module)
   ↓
handler.py (encode result)
   ↓
Client Response (Base64 image)
```

---

## 📊 حجم الملفات

### الكود
- `cpvton_infer.py`: ~12 KB
- `handler.py`: ~6 KB
- `client_example.py`: ~9 KB
- `networks.py`: ~18 KB (أصلي)

### Docker Image
- Base (CUDA runtime): ~2 GB
- + Dependencies: ~500 MB
- + Checkpoints (optional): ~260 MB
- **Total:** ~2.7 GB

### Checkpoints
- GMM: ~80 MB
- TOM: ~180 MB
- **Total:** ~260 MB

---

## 🔧 التعديلات الممكنة

### للتحسين الفوري
1. **في `cpvton_infer.py`:**
   - استبدل `create_dummy_parse()` بـ parsing حقيقي
   - أضف `detect_pose()` باستخدام OpenPose

2. **في `handler.py`:**
   - أضف support لـ batch requests
   - أضف monitoring & metrics

3. **في `Dockerfile`:**
   - أضف multi-stage build لتصغير الحجم
   - دمج checkpoints في image

### للتحسين المتقدم
1. **Caching:**
   ```python
   @lru_cache(maxsize=100)
   def preprocess_cached(image_hash):
       ...
   ```

2. **Mixed Precision:**
   ```python
   with torch.cuda.amp.autocast():
       result = model.try_on(...)
   ```

3. **TorchScript:**
   ```python
   scripted_model = torch.jit.script(model)
   ```

---

## 📝 ملاحظات

### ما تم تطبيقه ✅
- ✅ Wrapper class كامل
- ✅ RunPod handler مع error handling
- ✅ Docker image + requirements
- ✅ Client examples
- ✅ Documentation شاملة

### ما يحتاج تحسين ⚠️
- ⚠️ Parsing & pose detection (dummy حالياً)
- ⚠️ Optimization (caching, batching)
- ⚠️ Monitoring & logging
- ⚠️ Rate limiting & auth

### للإنتاج الحقيقي 🎯
1. أضف CIHP_PGN / Graphonomy
2. أضف OpenPose COCO-18
3. استخدم RunPod Network Storage
4. فعّل monitoring
5. أضف authentication

---

## 🔗 الموارد

### داخلي
- [RUN_ME_FIRST.md](RUN_ME_FIRST.md) - ابدأ هنا
- [README_RUNPOD.md](README_RUNPOD.md) - الدليل الشامل
- [QUICKSTART.md](QUICKSTART.md) - بداية سريعة
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - ملخص

### خارجي
- [CP-VTON+ Paper](https://minar09.github.io/cpvtonplus/)
- [RunPod Docs](https://docs.runpod.io/)
- [CIHP_PGN](https://github.com/Engineering-Course/CIHP_PGN)
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

---

**Need help?** راجع [README_RUNPOD.md](README_RUNPOD.md) للتفاصيل الكاملة.





