# 🎨 CP-VTON+ على RunPod Serverless

> تحويل CP-VTON+ إلى Serverless API جاهز للإنتاج

[![RunPod](https://img.shields.io/badge/RunPod-Serverless-blue)](https://runpod.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-green)](Dockerfile)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](requirements_runpod.txt)

---

## 🚀 ما هذا؟

تم تحويل [CP-VTON+](https://github.com/minar09/cp-vton-plus) بنجاح إلى **RunPod Serverless Worker**! الآن يمكنك:

- ✅ استخدام Virtual Try-On من أي backend عبر REST API
- ✅ Auto-scaling حسب الطلب (تدفع فقط عند الاستخدام)
- ✅ GPU قوية بدون تكلفة ثابتة
- ✅ Deployment سهل بدون infrastructure management

---

## 📁 الملفات الرئيسية

```
cp-vton-plus/
├── cpvton_infer.py          # ⭐ كلاس wrapper للموديل
├── handler.py               # ⭐ RunPod handler
├── Dockerfile               # ⭐ Docker image
├── client_example.py        # ⭐ أمثلة استخدام
│
├── QUICK_DEPLOY.md          # 📖 خطوات سريعة (ابدأ هنا!)
├── DEPLOY_TO_RUNPOD.md      # 📖 دليل كامل
├── README_RUNPOD.md         # 📖 شرح شامل
└── DEPLOYMENT_SUMMARY.md    # 📖 ملخص التطبيق
```

---

## ⚡ Quick Start

### للـ Deploy مباشرة على RunPod (بدون Local):

```bash
# 1. Push على GitHub
git add . && git commit -m "ready" && git push

# 2. حمّل checkpoints على RunPod Network Storage
# (من Google Drive - راجع CHECKPOINTS_LINKS.md)

# 3. أنشئ Endpoint على RunPod Console
# استخدم image: ghcr.io/YOUR_USERNAME/cp-vton-plus:latest
```

**اقرأ:** [QUICK_DEPLOY.md](QUICK_DEPLOY.md) للخطوات التفصيلية

---

## 🎯 الاستخدام

### Python Client

```python
import requests
import base64

ENDPOINT_ID = "your-endpoint-id"
API_KEY = "your-api-key"

# تحويل صور لـ Base64
person_b64 = base64.b64encode(open("person.jpg", "rb").read()).decode()
cloth_b64 = base64.b64encode(open("cloth.jpg", "rb").read()).decode()

# Request
url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "input": {
        "person_image": person_b64,
        "cloth_image": cloth_b64
    }
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

# حفظ النتيجة
if result["status"] == "COMPLETED":
    output = result["output"]
    if output["success"]:
        img_data = base64.b64decode(output["result_image"])
        open("result.png", "wb").write(img_data)
        print("✅ نجح!")
```

**للمزيد:** [client_example.py](client_example.py)

---

## 💰 التكلفة

| Requests/Day | GPU Time | Cost/Month |
|-------------|----------|------------|
| 100         | ~0.14h   | **$1.80**  |
| 1,000       | ~1.4h    | **$17**    |
| 10,000      | ~14h     | **$170**   |

*مع RTX 3090 (~$0.40/hr) - تدفع فقط عند الاستخدام!*

---

## 📚 التوثيق الكامل

| ملف | الوصف |
|-----|-------|
| [QUICK_DEPLOY.md](QUICK_DEPLOY.md) | ⚡ خطوات سريعة (3 خطوات) |
| [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) | 📖 دليل deployment كامل |
| [README_RUNPOD.md](README_RUNPOD.md) | 📖 شرح تقني شامل |
| [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) | 📊 ملخص التطبيق |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 🏗️ بنية المشروع |

---

## 🎓 الموارد

- [CP-VTON+ Paper](https://minar09.github.io/cpvtonplus/)
- [RunPod Docs](https://docs.runpod.io/)
- [GitHub Container Registry](https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

---

## ⚠️ ملاحظة مهمة

الكود الحالي يستخدم **dummy parsing & pose** للتبسيط. للحصول على نتائج إنتاجية:

1. أضف CIHP_PGN / Graphonomy (human parsing)
2. أضف OpenPose COCO-18 (pose keypoints)

راجع [README.md](README.md) الأصلي للتفاصيل.

---

## 🤝 المساهمة

مرحب بالـ Pull Requests! راجع [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

نفس license CP-VTON+ الأصلي. راجع [LICENSE](LICENSE)

---

## 🆘 الدعم

- **GitHub Issues:** للمشاكل التقنية
- **RunPod Discord:** لمشاكل الـ deployment
- **Email:** your-email@example.com

---

**🎉 جاهز للاستخدام! ابدأ من [QUICK_DEPLOY.md](QUICK_DEPLOY.md)**

---

*Built with ❤️ by the CP-VTON+ Community*


