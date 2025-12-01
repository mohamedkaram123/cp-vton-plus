# ✅ تم تحديث الروابط - Links Updated

## 📦 الروابط الجديدة (Google Drive)

### GMM Checkpoint
```
https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing
```
- الملف: `gmm_final.pth`
- الحجم: ~76 MB

### TOM Checkpoint
```
https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing
```
- الملف: `tom_final.pth`
- الحجم: ~85 MB

---

## ✅ الملفات المُحدَّثة

تم تحديث الروابط في الملفات التالية:

### Documentation Files
- ✅ `TROUBLESHOOTING.md`
- ✅ `AFTER_BUILD.md`
- ✅ `START_HERE.md`
- ✅ `QUICK_DEPLOY.md`
- ✅ `DEPLOY_TO_RUNPOD.md`
- ✅ `RUN_ME_FIRST.md`
- ✅ `QUICKSTART.md`
- ✅ `README_AR.md`
- ✅ `README_RUNPOD.md`
- ✅ `DEPLOYMENT_SUMMARY.md`
- ✅ `CHECKPOINTS_LINKS.md`

### Scripts & Configuration
- ✅ `download_checkpoints.sh` (محدث مع دعم gdown)
- ✅ `Dockerfile`

### Not Changed (Original Project Files)
- ⚪ `README.md` (الملف الأصلي - لم يتم تغييره)

---

## 🎯 التغييرات الرئيسية

### من OneDrive إلى Google Drive

**قبل:**
```
https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g
```

**بعد:**
```
GMM: https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing
TOM: https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing
```

### تحديث الأحجام

**قبل:**
- GMM: ~80 MB
- TOM: ~180 MB

**بعد (الأحجام الفعلية):**
- GMM: ~76 MB ✅
- TOM: ~85 MB ✅

---

## 🚀 تحسينات إضافية

### Script التحميل (`download_checkpoints.sh`)

**تحسينات:**
- ✅ دعم تحميل تلقائي باستخدام `gdown`
- ✅ روابط Google Drive مباشرة
- ✅ تحقق من وجود `gdown` قبل التحميل

**الاستخدام الجديد:**
```bash
# تثبيت gdown
pip install gdown

# تشغيل script
./download_checkpoints.sh

# أو يدوياً:
gdown 'https://drive.google.com/uc?id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT' -O checkpoints/GMM/gmm_final.pth
gdown 'https://drive.google.com/uc?id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_' -O checkpoints/TOM/tom_final.pth
```

---

## 📋 Checklist للمستخدم

### قبل التحديث:
- [x] OneDrive links في الملفات
- [x] أحجام تقريبية غير دقيقة

### بعد التحديث:
- [x] Google Drive links محدثة
- [x] الأحجام الفعلية للملفات
- [x] دعم gdown للتحميل التلقائي
- [x] جميع ملفات Documentation محدثة

---

## 🎉 النتيجة

**جميع الروابط الآن تشير إلى Google Drive!**

### للتحميل:
1. **يدوياً:** افتح الروابط في المتصفح
2. **تلقائياً:** استخدم `./download_checkpoints.sh`
3. **مباشر:** استخدم `gdown` commands

### للرفع على RunPod:
راجع [AFTER_BUILD.md](AFTER_BUILD.md) للخطوات الكاملة.

---

## 📖 المراجع

- [CHECKPOINTS_LINKS.md](CHECKPOINTS_LINKS.md) - جميع الروابط
- [AFTER_BUILD.md](AFTER_BUILD.md) - خطوات الـ deployment
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل المشاكل

---

**✅ التحديث كامل! جاهز للاستخدام!**

*Updated: $(date)*


