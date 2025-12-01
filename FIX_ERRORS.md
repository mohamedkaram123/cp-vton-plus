# 🔧 إصلاح الأخطاء - Fix Current Errors

## ❌ الأخطاء الحالية

### Error 1: Checkpoints غير موجودة
```
[تحذير] checkpoint غير موجود: /app/checkpoints/GMM/gmm_final.pth
[تحذير] checkpoint غير موجود: /app/checkpoints/TOM/tom_final.pth
```

### Error 2: NumPy Version Conflict
```
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.2.6
```

---

## ✅ الحل الكامل (خطوة بخطوة)

### الخطوة 1: إصلاح NumPy Version ✅

**تم الإصلاح!** تم تحديث `requirements_runpod.txt`

الآن محتاج تعيد build الـ Docker image:

```bash
# في terminal
cd /home/momo/dev/cp-vton-plus

# Commit التغيير
git add requirements_runpod.txt
git commit -m "Fix: NumPy version conflict - force numpy<2.0.0"
git push

# GitHub Actions هيبني الimage تلقائياً!
```

**انتظر 5-10 دقائق** حتى ينتهي الـ build على GitHub.

---

### الخطوة 2: رفع Checkpoints (الأهم!) 🎯

**هذا السبب الرئيسي للخطأ!**

#### 2a. حمّل Checkpoints

إذا لم تحملهم بعد:

**تحميل تلقائي (wget):**
```bash
# GMM
wget -O gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"

# TOM
wget -O tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

#### 2b. اذهب إلى RunPod Storage

```
https://www.runpod.io/console/storage
```

#### 2c. أنشئ/افتح Network Volume

- إذا موجود: افتح `cpvton-checkpoints`
- إذا مش موجود: اضغط **"Create Network Volume"**
  ```
  Name: cpvton-checkpoints
  Size: 10 GB
  Region: اختر الأقرب
  ```

#### 2d. أنشئ Structure

اضغط **"Browse Files"** ثم:

```
1. New Folder → checkpoints
2. ادخل جوا checkpoints/
3. New Folder → GMM
4. New Folder → TOM
```

**البنية المطلوبة:**
```
/checkpoints/
  ├── GMM/
  │   └── gmm_final.pth  (76 MB)
  └── TOM/
      └── tom_final.pth  (85 MB)
```

#### 2e. ارفع الملفات

1. **ادخل:** `checkpoints/GMM/`
   - **اضغط:** Upload Files
   - **اختر:** `gmm_final.pth`
   - **انتظر:** حتى ينتهي Upload (~1-2 دقيقة)

2. **ارجع:** `checkpoints/TOM/`
   - **اضغط:** Upload Files
   - **اختر:** `tom_final.pth`
   - **انتظر:** حتى ينتهي Upload (~1 دقيقة)

#### 2f. تحقق من الرفع

في File Browser تأكد:
```
✅ /checkpoints/GMM/gmm_final.pth (76 MB)
✅ /checkpoints/TOM/tom_final.pth (85 MB)
```

---

### الخطوة 3: ربط Network Storage بالـ Endpoint

#### 3a. اذهب إلى Endpoint

```
https://www.runpod.io/console/serverless
```

#### 3b. Edit Endpoint

1. **اضغط** على endpoint بتاعك
2. **اضغط:** Edit (أو ⚙️ Settings)
3. **scroll down لـ:** Advanced Settings

#### 3c. اربط Network Storage

```
Network Storage:
  ☑ Enable Network Storage
  
  Mount Path: /app/checkpoints
  Select Volume: cpvton-checkpoints
```

**⚠️ مهم جداً:** Mount Path لازم يكون **بالضبط**: `/app/checkpoints`

#### 3d. احفظ

- **اضغط:** Save / Update Endpoint

---

### الخطوة 4: انتظر الـ Docker Build

بعد ما push التغييرات:

1. **اذهب:** https://github.com/YOUR_USERNAME/YOUR_REPO/actions
2. **شوف:** Workflow بيشتغل؟
3. **انتظر:** حتى ينتهي (✅ green checkmark)

---

### الخطوة 5: Update Endpoint بالـ Image الجديد

إذا الimage القديم كان مخزن cache:

1. **في Endpoint Settings**
2. **اضغط:** "Force Pull Latest Image" (إذا موجود)
3. **أو:** Stop All Workers → سينزل الimage الجديد تلقائياً

---

### الخطوة 6: اختبار! 🧪

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

---

## ✅ النتيجة المتوقعة

### Before (الحالي):
```json
{
  "status": "FAILED",
  "error": "الموديل غير محمل بشكل صحيح"
}
```

### After (بعد الإصلاح):
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

## 🔍 تحقق من Logs

بعد الإصلاح، الـ logs لازم تقول:

### ✅ Logs صحيحة:
```
🚀 بدء تحميل CP-VTON+ Model...
[CPVTONPlus] تحميل GMM من /app/checkpoints/GMM/gmm_final.pth
initialization method [normal]
[CPVTONPlus] تحميل TOM من /app/checkpoints/TOM/tom_final.pth
initialization method [normal]
✅ تم تحميل الموديل بنجاح!
```

**بدون تحذيرات!** ❌ لا "checkpoint غير موجود"

---

## 📋 Checklist النهائي

### NumPy Fix:
- [x] عدّلت `requirements_runpod.txt`
- [ ] commit + push
- [ ] GitHub Actions build نجح
- [ ] Endpoint pull الimage الجديد

### Checkpoints Fix:
- [ ] حمّلت `gmm_final.pth` (76 MB)
- [ ] حمّلت `tom_final.pth` (85 MB)
- [ ] أنشأت Network Volume: `cpvton-checkpoints`
- [ ] رفعت في `/checkpoints/GMM/` و `/checkpoints/TOM/`
- [ ] ربطت Network Storage بالـ endpoint
- [ ] Mount Path: `/app/checkpoints` ✅
- [ ] حفظت التغييرات

### Testing:
- [ ] شفت logs جديدة (بدون تحذيرات)
- [ ] جرّبت request
- [ ] نجح! ✅

---

## ⏱️ الوقت المتوقع

- NumPy fix + rebuild: **10 دقائق**
- رفع Checkpoints: **5 دقائق**
- ربط Network Storage: **2 دقيقة**
- **Total: ~15-20 دقيقة**

---

## 🎯 الخطوة التالية

**ابدأ الآن:**

### 1. Commit + Push
```bash
git add requirements_runpod.txt
git commit -m "Fix NumPy version conflict"
git push
```

### 2. رفع Checkpoints
اذهب: https://www.runpod.io/console/storage

### 3. اربط بالـ Endpoint
Mount: `/app/checkpoints`

### 4. اختبر!
```bash
curl -X POST ...
```

---

**💡 Tip:** الأهم هو رفع الcheckpoints! بدونها الموديل مش هيشتغل حتى مع NumPy fix.

---

## 📞 لو محتاج مساعدة

- [AFTER_BUILD.md](AFTER_BUILD.md) - خطوات مفصلة
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل المشاكل
- [CHECKPOINTS_LINKS.md](CHECKPOINTS_LINKS.md) - الروابط

---

**🚀 Let's fix it!**

