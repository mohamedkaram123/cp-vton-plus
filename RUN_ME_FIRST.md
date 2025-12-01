# 🎯 ابدأ من هنا! CP-VTON+ على RunPod

## 🎉 تم تجهيز كل شيء!

تم تحويل CP-VTON+ بنجاح إلى **RunPod Serverless Worker**. الآن يمكنك استخدامه من أي backend عبر REST API!

---

## 🗂️ الملفات الجديدة

### 📦 الكود الرئيسي
- ✅ `cpvton_infer.py` - كلاس wrapper للموديل
- ✅ `handler.py` - RunPod serverless handler
- ✅ `Dockerfile` - تعريف Docker image
- ✅ `requirements_runpod.txt` - Dependencies

### 🛠️ Tools & Scripts
- ✅ `build_and_push.sh` - بناء ورفع Docker (تلقائي)
- ✅ `download_checkpoints.sh` - تحميل checkpoints
- ✅ `runpod_test.py` - اختبار محلي
- ✅ `client_example.py` - أمثلة استخدام API

### 📚 التوثيق
- ✅ `README_RUNPOD.md` - دليل شامل (اقرأه!)
- ✅ `QUICKSTART.md` - بداية سريعة
- ✅ `DEPLOYMENT_SUMMARY.md` - ملخص التطبيق
- ✅ `RUN_ME_FIRST.md` - هذا الملف

---

## ⚡ Quick Start (3 خطوات فقط!)

### 1️⃣ تحميل Checkpoints

**اختر واحدة:**

**Option A: Automatic (محاولة)**
```bash
chmod +x download_checkpoints.sh
./download_checkpoints.sh
```

**Option B: Manual (مُفضَّل)**
1. حمّل من Google Drive:
```bash
# تحميل تلقائي
wget "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_" -O gmm_final.pth
wget "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT" -O tom_final.pth
```
2. حمّل `gmm_final.pth` (~80MB) و `tom_final.pth` (~180MB)
3. ضعهم في:
   ```
   checkpoints/GMM/gmm_final.pth
   checkpoints/TOM/tom_final.pth
   ```

### 2️⃣ بناء ورفع Docker Image

```bash
# عدّل username بتاعك
export DOCKER_USER="your-dockerhub-username"

# بناء ورفع
chmod +x build_and_push.sh
./build_and_push.sh
```

البرنامج هيساعدك في:
- بناء Docker image
- اختبار (اختياري)
- رفع لـ Docker Hub

### 3️⃣ Deploy على RunPod

1. اذهب إلى: https://www.runpod.io/console/serverless
2. اضغط **"New Endpoint"**
3. املأ:
   ```
   Name: cpvton-plus
   Container Image: your-username/cpvton-runpod:latest
   GPU: RTX 3090 (أو A4000)
   Container Disk: 15 GB
   Workers: 0 → 3 (auto-scale)
   ```
4. اضغط **"Deploy"**

---

## 🧪 اختبار

### اختبار محلي (قبل Deploy)

```bash
# اختبار بسيط
python runpod_test.py

# اختبار بصور حقيقية
python runpod_test.py data/test/image/000001_0.jpg data/test/cloth/000001_1.jpg
```

### اختبار على RunPod (بعد Deploy)

```python
from client_example import CPVTONClient

# عدّل هنا بعد Deploy
client = CPVTONClient(
    endpoint_id="YOUR_ENDPOINT_ID",    # من RunPod Console
    api_key="YOUR_API_KEY"              # من RunPod Settings
)

result = client.try_on_sync(
    person_image="person.jpg",
    cloth_image="cloth.jpg",
    output_path="result.png"
)

if result["success"]:
    print(f"✅ نجح! النتيجة في: result.png")
else:
    print(f"❌ فشل: {result['error']}")
```

---

## 📖 أين تذهب بعد ذلك؟

### للاستخدام الفوري
→ اقرأ [QUICKSTART.md](QUICKSTART.md)

### للتفاصيل الكاملة
→ اقرأ [README_RUNPOD.md](README_RUNPOD.md)

### للفهم التقني
→ اقرأ [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

### لأمثلة الاستخدام
→ شوف [client_example.py](client_example.py)

---

## 💡 ملاحظات مهمة

### ⚠️ النتائج حالياً ليست مثالية

الكود الحالي يستخدم **dummy parsing & pose detection** للتبسيط.

**للحصول على نتائج إنتاجية:**
1. أضف CIHP_PGN أو Graphonomy (human parsing)
2. أضف OpenPose COCO-18 (pose keypoints)
3. راجع [README.md](README.md) الأصلي تحت "Testing with custom images"

### 💰 التكلفة المتوقعة

- **100 requests/day:** ~$2/month
- **1,000 requests/day:** ~$17/month  
- **10,000 requests/day:** ~$170/month

**مع auto-scaling:** تدفع فقط عند الاستخدام!

### 🎯 للإنتاج الحقيقي

بعد ما تجرب وتتأكد إنه شغال:
1. أضف human parsing & pose detection
2. استخدم RunPod Network Storage للـ checkpoints
3. فعّل monitoring & logging
4. أضف rate limiting & authentication

---

## 🆘 مشاكل شائعة

### "Model not loaded properly"
→ تأكد من وجود checkpoints في `checkpoints/GMM` و `checkpoints/TOM`

### "CUDA out of memory"
→ استخدم GPU أكبر (A4000 بدلاً من RTX 4000)

### "Slow inference"
→ استخدم Active Workers بدلاً من auto-scale من 0

### "Poor quality results"
→ أضف parsing & pose detection حقيقي (راجع README_RUNPOD.md)

---

## 🎓 الموارد

### Documentation
- [README_RUNPOD.md](README_RUNPOD.md) - دليل شامل
- [QUICKSTART.md](QUICKSTART.md) - بداية سريعة
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - ملخص التطبيق

### External
- [CP-VTON+ Paper](https://minar09.github.io/cpvtonplus/)
- [RunPod Docs](https://docs.runpod.io/)
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- [CIHP_PGN](https://github.com/Engineering-Course/CIHP_PGN)

---

## ✅ Checklist

قبل ما تبدأ، تأكد من:

- [ ] حمّلت checkpoints (`gmm_final.pth` + `tom_final.pth`)
- [ ] عندك حساب Docker Hub
- [ ] عندك حساب RunPod (مع credit)
- [ ] Docker مثبت محلياً
- [ ] قريت QUICKSTART.md

---

## 🚀 Let's Go!

```bash
# 1. تحميل checkpoints
./download_checkpoints.sh

# 2. بناء ورفع
export DOCKER_USER="your-username"
./build_and_push.sh

# 3. Deploy على RunPod
# (اتبع الخطوات أعلاه)

# 4. اختبار
python client_example.py
```

---

## 📞 الدعم

**عندك سؤال أو مشكلة؟**

1. راجع [README_RUNPOD.md](README_RUNPOD.md) أولاً
2. شوف "المشاكل الشائعة" أعلاه
3. افتح Issue على GitHub
4. تواصل على RunPod Discord

---

**🎉 مبروك! CP-VTON+ جاهز للاستخدام!**

**Need help?** → اقرأ [README_RUNPOD.md](README_RUNPOD.md)  
**Want details?** → اقرأ [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)  
**Quick start?** → اقرأ [QUICKSTART.md](QUICKSTART.md)

---

*Built with ❤️ for the CP-VTON+ Community*


