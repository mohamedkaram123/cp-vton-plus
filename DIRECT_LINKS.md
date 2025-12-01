# 🚀 روابط التحميل المباشرة - Direct Download Links

## ✅ روابط محدثة وشغالة!

---

## 📦 Checkpoints

### GMM Checkpoint (~76 MB)

**تحميل مباشر:**
```bash
wget -O gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"
```

**أو curl:**
```bash
curl -L -o gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"
```

**Link:** https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_

---

### TOM Checkpoint (~85 MB)

**تحميل مباشر:**
```bash
wget -O tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

**أو curl:**
```bash
curl -L -o tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

**Link:** https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT

---

## ⚡ تحميل سريع (Copy & Paste)

```bash
# إنشاء directories
mkdir -p checkpoints/GMM checkpoints/TOM

# تحميل GMM
wget -O checkpoints/GMM/gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"

# تحميل TOM
wget -O checkpoints/TOM/tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"

# تحقق
ls -lh checkpoints/GMM/gmm_final.pth
ls -lh checkpoints/TOM/tom_final.pth
```

**الناتج المتوقع:**
```
gmm_final.pth  ~76M
tom_final.pth  ~85M
```

---

## 🐳 للاستخدام في Dockerfile

إذا تريد دمج checkpoints في Docker image:

```dockerfile
# في Dockerfile قبل CMD:
RUN wget -O /app/checkpoints/GMM/gmm_final.pth \
    "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_" && \
    wget -O /app/checkpoints/TOM/tom_final.pth \
    "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

**⚠️ ملاحظة:** هيزود حجم الimage ~160MB

---

## 📝 للاستخدام في Scripts

```bash
#!/bin/bash
# download_checkpoints_direct.sh

GMM_URL="https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"
TOM_URL="https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"

mkdir -p checkpoints/GMM checkpoints/TOM

echo "📥 تحميل GMM..."
wget -O checkpoints/GMM/gmm_final.pth "$GMM_URL"

echo "📥 تحميل TOM..."
wget -O checkpoints/TOM/tom_final.pth "$TOM_URL"

echo "✅ تم!"
```

---

## 🎯 الاستخدام السريع

### للتحميل المحلي:
```bash
./download_checkpoints.sh
```

### للتحميل على RunPod Network Storage:
1. حمّل محلياً أولاً (باستخدام wget أعلاه)
2. ارفعهم على RunPod Storage
3. أو استخدم wget في RunPod Pod

---

## 💡 Tips

1. **wget** أسرع من المتصفح
2. **الروابط المباشرة** تعمل في أي مكان
3. **يمكن استخدامها** في CI/CD pipelines
4. **لا تحتاج** authentication

---

## ✅ التحقق

بعد التحميل:

```bash
# تحقق من الأحجام
ls -lh checkpoints/GMM/gmm_final.pth  # ~76M
ls -lh checkpoints/TOM/tom_final.pth  # ~85M

# تحقق من MD5 (اختياري)
md5sum checkpoints/GMM/gmm_final.pth
md5sum checkpoints/TOM/tom_final.pth
```

---

## 📚 المراجع

- [download_checkpoints.sh](download_checkpoints.sh) - Script محدث
- [Dockerfile](Dockerfile) - Docker build config
- [FIX_ERRORS.md](FIX_ERRORS.md) - حل مشكلة الcheckpoints

---

**🎉 روابط مباشرة جاهزة للاستخدام!**

*Updated with direct download links*

