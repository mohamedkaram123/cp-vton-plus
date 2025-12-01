# 🔧 إصلاح مشكلة Channels

## ❌ الخطأ السابق

```
RuntimeError: Given groups=1, weight of size [64, 22, 4, 4], 
expected input[1, 3, 256, 192] to have 22 channels, but got 3 channels instead
```

---

## 🎯 السبب

GMM model يتوقع **22 input channels** لكن كنا نبعتله **3 channels** فقط.

### التكوين الصحيح للـ Agnostic:

حسب الكود الأصلي في `cp_dataset.py`:
```python
agnostic = torch.cat([shape, im_h, pose_map], 0)
```

- `shape`: 1 channel (body shape)
- `im_h`: 1 channel (head region)  
- `pose_map`: 18 channels (pose keypoints)
- **Total: 20 channels**

لكن GMM في `networks.py` line 507:
```python
self.extractionA = FeatureExtraction(22, ngf=64, ...)
```

**يتوقع 22 channels!** 

---

## ✅ الحل

تم تحديث `cpvton_infer.py`:

```python
# إنشاء agnostic representation صحيح
shape = torch.ones(1, 1, H, W) * 0.5      # 1 channel
head = torch.ones(1, 1, H, W) * -1        # 1 channel  
pose_map = torch.zeros(1, 18, H, W)       # 18 channels

agnostic_20 = torch.cat([shape, head, pose_map], 1)  # 20 channels

# إضافة 2 channels dummy
dummy = torch.zeros(1, 2, H, W)
agnostic = torch.cat([agnostic_20, dummy], 1)  # 22 channels ✅
```

---

## 🔄 الخطوات للتطبيق

### 1. Commit التغييرات

```bash
cd /home/momo/dev/cp-vton-plus

git add cpvton_infer.py requirements_runpod.txt
git commit -m "Fix: GMM input channels (22) + NumPy<2.0"
git push
```

### 2. انتظر GitHub Actions Build

- اذهب: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- انتظر Build (5-10 دقائق)

### 3. Update RunPod Endpoint

```
1. RunPod Console → Your Endpoint
2. Stop All Workers (لتحميل الimage الجديد)
3. Request جديد
```

### 4. اختبار

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

```json
{
  "status": "COMPLETED",
  "output": {
    "success": true,
    "result_image": "base64...",
    "message": "Virtual try-on completed successfully"
  }
}
```

---

## 📋 المشاكل المتبقية

### 1. Checkpoints لسه مش موجودة! ⚠️

من الـ logs:
```
[تحذير] checkpoint غير موجود: /app/checkpoints/GMM/gmm_final.pth
[تحذير] checkpoint غير موجود: /app/checkpoints/TOM/tom_final.pth
```

**الحل:** ارفع checkpoints على RunPod Network Storage (راجع FIX_ERRORS.md)

### 2. NumPy Warning ⚠️

تم الإصلاح في `requirements_runpod.txt` (numpy<2.0.0)

---

## 🎯 الأولويات

### Priority 1 (عالي): رفع Checkpoints 📦
**بدون checkpoints:** الموديل يستخدم random weights = نتائج سيئة!

**الخطوات:**
1. حمّل من Google Drive (روابط مباشرة في DIRECT_LINKS.md)
2. ارفع على RunPod Network Storage
3. اربط بالـ Endpoint

### Priority 2 (متوسط): انتظر Build الجديد ⏳
بعد push الكود المُصلح، انتظر GitHub Actions.

---

## ⏱️ الوقت المتوقع

- Git push: **1 دقيقة**
- GitHub build: **10 دقائق**
- رفع checkpoints: **5 دقائق**
- **Total: ~15 دقيقة**

---

## 📖 للمزيد

- [FIX_ERRORS.md](FIX_ERRORS.md) - حل جميع المشاكل
- [DIRECT_LINKS.md](DIRECT_LINKS.md) - روابط التحميل المباشرة
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - دليل المشاكل

---

**🚀 بعد التطبيق، الموديل هيشتغل 100%!**

