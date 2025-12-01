# 📦 CP-VTON+ Checkpoints Links

## 🔗 Google Drive Links (محدثة)

### GMM Checkpoint
```
https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing
```
- **الملف:** `gmm_final.pth`
- **الحجم:** ~76 MB

### TOM Checkpoint
```
https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing
```
- **الملف:** `tom_final.pth`
- **الحجم:** ~85 MB

---

## 📥 طريقة التحميل

### Option 1: من المتصفح (سهلة)

1. **GMM:**
   - افتح: https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing
   - اضغط تحميل (Download)
   - احفظ باسم: `gmm_final.pth`

2. **TOM:**
   - افتح: https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing
   - اضغط تحميل (Download)
   - احفظ باسم: `tom_final.pth`

---

### Option 2: باستخدام gdown (للتحميل التلقائي)

#### تثبيت gdown:
```bash
pip install gdown
```

#### تحميل GMM:
```bash
gdown "https://drive.google.com/uc?id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT" -O gmm_final.pth
```

#### تحميل TOM:
```bash
gdown "https://drive.google.com/uc?id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing" -O tom_final.pth
```

---

### Option 3: wget (إذا الملفات public)

```bash
# GMM
wget --no-check-certificate \
  'https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT' \
  -O gmm_final.pth

# TOM
wget --no-check-certificate \
  'https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing' \
  -O tom_final.pth
```

---

## ✅ بعد التحميل

### تحقق من الأحجام:
```bash
ls -lh *.pth
```

**المتوقع:**
```
gmm_final.pth  ~76 MB
tom_final.pth  ~85 MB
```

---

## 📤 رفع على RunPod Network Storage

### الخطوات:

1. **اذهب إلى:** https://www.runpod.io/console/storage

2. **افتح Volume:** `cpvton-checkpoints`

3. **أنشئ Structure:**
   ```
   /checkpoints/
     ├── GMM/
     └── TOM/
   ```

4. **ارفع الملفات:**
   - `gmm_final.pth` → `/checkpoints/GMM/`
   - `tom_final.pth` → `/checkpoints/TOM/`

5. **اربط بالـ Endpoint:**
   ```
   Mount Path: /app/checkpoints
   Volume: cpvton-checkpoints
   ```

---

## 🎯 الخطوات الكاملة

### 1. تحميل من Google Drive ✅
- [x] حمّلت gmm_final.pth (76 MB)
- [x] حمّلت tom_final.pth (85 MB)

### 2. رفع على RunPod
- [ ] أنشأت Network Volume
- [ ] أنشأت folders: `/checkpoints/GMM/` و `/TOM/`
- [ ] رفعت الملفات

### 3. ربط بالـ Endpoint
- [ ] Mount Path: `/app/checkpoints`
- [ ] Volume: `cpvton-checkpoints`
- [ ] حفظت التغييرات

### 4. اختبار
- [ ] أعدت تشغيل workers
- [ ] جرّبت request
- [ ] نجح! ✅

---

## 📚 للتفاصيل

- [AFTER_BUILD.md](AFTER_BUILD.md) - الخطوات الكاملة
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل المشاكل

---

## 🔗 الروابط الأصلية (OneDrive)

للمرجعية، الروابط الأصلية من الـ repo:
```
https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g
```

---

**✅ الملفات جاهزة! الخطوة التالية: رفعهم على RunPod!**

