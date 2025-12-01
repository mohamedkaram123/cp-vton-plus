# 🔧 Troubleshooting - حل المشاكل

## ❌ الخطأ: "الموديل غير محمل بشكل صحيح"

```json
{
  "error": "الموديل غير محمل بشكل صحيح. تحقق من logs.",
  "status": "FAILED"
}
```

---

## 🎯 السبب الرئيسي

**Checkpoints مش موجودة أو المسار غلط!**

---

## ✅ الحل خطوة بخطوة

### الخطوة 1: تحقق من Logs

1. **اذهب إلى RunPod Console:**
   ```
   https://www.runpod.io/console/serverless
   ```

2. **اضغط على endpoint بتاعك**

3. **اذهب لـ "Logs" tab**

4. **ابحث عن:**
   ```
   [CPVTONPlus] تحميل GMM من...
   [CPVTONPlus] تحميل TOM من...
   ```

5. **شوف الأخطاء:**
   - `checkpoint غير موجود`
   - `No such file or directory`
   - `/app/checkpoints/GMM/gmm_final.pth`

---

### الخطوة 2: تحقق من Network Storage

#### 2a. افتح Network Storage

```
https://www.runpod.io/console/storage
```

#### 2b. اضغط "Browse Files" على volume بتاعك

#### 2c. تأكد من البنية:

```
✅ الصحيح:
/checkpoints/
  ├── GMM/
  │   └── gmm_final.pth  (~80MB)
  └── TOM/
      └── tom_final.pth  (~180MB)

❌ الخطأ (مثال):
/GMM/
  └── gmm_final.pth
/TOM/
  └── tom_final.pth
```

**المسار الكامل لازم يكون:**
- `/checkpoints/GMM/gmm_final.pth`
- `/checkpoints/TOM/tom_final.pth`

---

### الخطوة 3: تحقق من Mount Path

في Endpoint Settings:

1. **اذهب لـ endpoint**
2. **Edit Settings**
3. **Advanced → Network Storage**
4. **تأكد من:**
   ```
   Mount Path: /app/checkpoints
   Select Volume: cpvton-checkpoints
   ```

**⚠️ مهم:** Mount Path لازم يكون `/app/checkpoints` (مش `/checkpoints`)

---

### الخطوة 4: أعد رفع Checkpoints (إذا لزم)

#### 4a. حمّل Checkpoints من Google Drive

**GMM Checkpoint:**
```
https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing
```

**TOM Checkpoint:**
```
https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing
```

الملفات:
- `gmm_final.pth` (~80 MB)
- `tom_final.pth` (~180 MB)

#### 4b. امسح القديمة وارفع جديدة

في Network Storage:

1. **امسح:** `/checkpoints/` folder
2. **أنشئ جديدة:** `/checkpoints/GMM/` و `/checkpoints/TOM/`
3. **ارفع:**
   - `gmm_final.pth` في `/checkpoints/GMM/`
   - `tom_final.pth` في `/checkpoints/TOM/`

#### 4c. تحقق من الأحجام

```
gmm_final.pth: حوالي 80 MB
tom_final.pth: حوالي 180 MB
```

إذا الأحجام مختلفة، معناها الملفات تالفة!

---

### الخطوة 5: أعد تشغيل Endpoint

بعد تصحيح الـ checkpoints:

1. **في Endpoint Settings**
2. **اضغط:** "Stop All Workers"
3. **انتظر دقيقة**
4. **Request جديد** - Worker جديد هيبدأ

---

## 🔍 Checklist للتحقق

- [ ] Checkpoints محملة من Google Drive (الأحجام صحيحة: GMM ~76MB, TOM ~85MB)
- [ ] Network Volume موجود: `cpvton-checkpoints`
- [ ] البنية صحيحة: `/checkpoints/GMM/` و `/checkpoints/TOM/`
- [ ] Mount Path في Endpoint: `/app/checkpoints`
- [ ] Network Storage مربوط بالـ endpoint
- [ ] Endpoint تم restart بعد التغييرات

---

## 📊 أمثلة Logs

### ✅ Logs صحيحة (شغال)

```
[CPVTONPlus] تحميل GMM من /app/checkpoints/GMM/gmm_final.pth
initialization method [normal]
[CPVTONPlus] تحميل TOM من /app/checkpoints/TOM/tom_final.pth
initialization method [normal]
[CPVTONPlus] تم تحميل الموديلات بنجاح!
✅ تم تحميل الموديل بنجاح!
```

### ❌ Logs خطأ (مش شغال)

```
[تحذير] checkpoint غير موجود: /app/checkpoints/GMM/gmm_final.pth
[تحذير] سيتم استخدام weights عشوائية!
[تحذير] checkpoint غير موجود: /app/checkpoints/TOM/tom_final.pth
❌ الموديل غير محمل بشكل صحيح
```

---

## 🛠️ حلول إضافية

### إذا المشكلة لسه موجودة:

#### Option 1: استخدم Environment Variables

في Endpoint Settings → Environment Variables:

```
GMM_CHECKPOINT=/app/checkpoints/GMM/gmm_final.pth
TOM_CHECKPOINT=/app/checkpoints/TOM/tom_final.pth
DEVICE=cuda
```

#### Option 2: دمج Checkpoints في Docker Image

عدّل `Dockerfile`:

```dockerfile
# قبل CMD، أضف:
COPY checkpoints/GMM/gmm_final.pth /app/checkpoints/GMM/
COPY checkpoints/TOM/tom_final.pth /app/checkpoints/TOM/
```

**⚠️ تحذير:** هيزود حجم الـ image (~260 MB)

ثم أعد build:

```bash
docker build -t your-user/cpvton-runpod:latest .
docker push your-user/cpvton-runpod:latest
```

وفي RunPod، استخدم الـ image الجديد.

#### Option 3: استخدم wget في Docker

في `Dockerfile`:

```dockerfile
# قبل CMD
RUN wget -O /app/checkpoints/GMM/gmm_final.pth https://YOUR_URL/gmm_final.pth
RUN wget -O /app/checkpoints/TOM/tom_final.pth https://YOUR_URL/tom_final.pth
```

(محتاج ترفع الـ checkpoints على cloud storage أول وتاخد public URLs)

---

## 🔄 Test بعد الإصلاح

### Test Request

```bash
curl -X POST "https://api.runpod.ai/v2/ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "'$(base64 -w 0 person.jpg)'",
      "cloth_image": "'$(base64 -w 0 cloth.jpg)'"
    }
  }' | jq .
```

### Expected Response

```json
{
  "status": "COMPLETED",
  "output": {
    "success": true,
    "result_image": "...",
    "message": "Virtual try-on completed successfully"
  }
}
```

---

## 💡 نصائح لتجنب المشكلة

1. **دائماً تحقق من Logs** بعد الـ deployment
2. **اختبر بـ Health Check** أولاً
3. **احفظ Checkpoints في مكان آمن** (backup)
4. **استخدم Network Storage** (أفضل من دمجها في image)
5. **تأكد من Mount Paths** قبل الـ deployment

---

## 📞 لو المشكلة لسه موجودة

### 1. شارك الـ Logs

انسخ logs كاملة من RunPod وشاركها.

### 2. تحقق من:

```
- Network Volume موجود؟
- Checkpoints موجودة جوا الـ volume؟
- Mount path صحيح؟
- Endpoint تم restart؟
```

### 3. جرب Clean Deployment

1. امسح Endpoint القديم
2. أنشئ endpoint جديد
3. اربط Network Storage من البداية
4. اختبر

---

## ✅ الحل السريع (TL;DR)

```bash
# 1. تأكد من checkpoints موجودة
# في Network Storage: /checkpoints/GMM/gmm_final.pth
#                     /checkpoints/TOM/tom_final.pth

# 2. تأكد من Mount Path
# في Endpoint: /app/checkpoints → cpvton-checkpoints

# 3. Restart Endpoint
# Stop All Workers → Request جديد

# 4. Test
curl -X POST "..." # كما أعلاه
```

---

**🎯 بعد الإصلاح، Request التالي هينجح! ✅**

---

*Need more help? Check logs in RunPod Console*

