# ⚡ Quick Start - CP-VTON+ على RunPod

دليل سريع للبدء في أقل من 10 دقائق!

---

## 📦 المتطلبات

قبل البدء، تأكد من:

- ✅ حساب على [RunPod](https://runpod.io) (يفضل مع credit)
- ✅ حساب [Docker Hub](https://hub.docker.com)
- ✅ Docker مثبت محلياً
- ✅ Git مثبت

---

## 🚀 الخطوات

### 1️⃣ استنساخ الريبو

```bash
git clone https://github.com/YOUR_REPO/cp-vton-plus.git
cd cp-vton-plus
```

### 2️⃣ تحميل Checkpoints

**الخيار A: تحميل يدوي (مُفضّل)**

1. افتح الرابط: https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g
2. حمّل `gmm_final.pth` و `tom_final.pth`
3. ضعهم في:
   ```
   checkpoints/GMM/gmm_final.pth
   checkpoints/TOM/tom_final.pth
   ```

**الخيار B: استخدام script**

```bash
chmod +x download_checkpoints.sh
./download_checkpoints.sh
```

### 3️⃣ بناء Docker Image

```bash
# عدّل DOCKER_USER في build_and_push.sh أولاً
export DOCKER_USER="your-dockerhub-username"

# بناء ورفع
chmod +x build_and_push.sh
./build_and_push.sh
```

أو يدوياً:

```bash
docker build -t your-username/cpvton-runpod:latest .
docker push your-username/cpvton-runpod:latest
```

### 4️⃣ إنشاء Endpoint على RunPod

1. اذهب إلى https://www.runpod.io/console/serverless
2. اضغط **"New Endpoint"**
3. املأ:
   - **Name:** `cpvton-plus`
   - **Container Image:** `your-username/cpvton-runpod:latest`
   - **GPU:** RTX 3090 أو A4000
   - **Container Disk:** 15 GB
   - **Workers:** 0 → 3 (auto-scale)

4. اضغط **"Deploy"**

### 5️⃣ اختبار

انسخ **Endpoint ID** و **API Key** من RunPod، ثم:

```python
# اختبار سريع
from client_example import CPVTONClient

client = CPVTONClient(
    endpoint_id="YOUR_ENDPOINT_ID",
    api_key="YOUR_API_KEY"
)

result = client.try_on_sync(
    person_image="path/to/person.jpg",
    cloth_image="path/to/cloth.jpg",
    output_path="result.png"
)

print(result)
```

---

## 🎯 التالي؟

### للتطوير
- راجع [README_RUNPOD.md](README_RUNPOD.md) للتفاصيل الكاملة
- أضف human parsing & pose detection للنتائج الأفضل

### للإنتاج
- استخدم RunPod Network Storage للـ checkpoints
- فعّل monitoring & logging
- أضف caching & optimization

---

## 🐛 مشاكل شائعة

### "Model not loaded"
- تأكد من رفع checkpoints في `/app/checkpoints`
- استخدم RunPod Network Storage

### CUDA OOM
- استخدم GPU أكبر (A4000 بدلاً من RTX 4000)

### Slow inference
- فعّل Active Workers (بدلاً من auto-scale من 0)

---

## 📞 الدعم

- Issues: GitHub Issues
- Discord: RunPod Community

---

**الآن جاهز! 🎉**

راجع [README_RUNPOD.md](README_RUNPOD.md) للمزيد من التفاصيل.

