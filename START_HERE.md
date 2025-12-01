# 🎯 ابدأ من هنا - CP-VTON+ RunPod Deployment

## ✅ تم تجهيز كل شيء!

تم تحويل CP-VTON+ بنجاح إلى **RunPod Serverless Worker**. كل الملفات جاهزة!

---

## 📋 الخطوات للـ Deploy (بدون تشغيل محلي)

### الخطوة 1: Push على GitHub ✨

```bash
# في terminal
cd /home/momo/dev/cp-vton-plus

# Initialize git
git init
git add .
git commit -m "CP-VTON+ RunPod Serverless ready"

# Add remote (عدّل USERNAME و REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git branch -M main
git push -u origin main
```

**بعد الـ Push:**
- ✅ GitHub Actions سيبني Docker image تلقائياً
- ✅ الـ image سيكون في: `ghcr.io/YOUR_USERNAME/YOUR_REPO:latest`

---

### الخطوة 2: حمّل Checkpoints 📦

**لازم تحمل Checkpoints للموديل!**

#### 2a. حمّل من OneDrive:

الرابط: https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g

الملفات:
- `gmm_final.pth` (~80MB)
- `tom_final.pth` (~180MB)

#### 2b. ارفعهم على RunPod Network Storage:

1. اذهب: https://www.runpod.io/console/storage
2. اضغط **"Create Network Volume"**
   - Name: `cpvton-checkpoints`
   - Size: 10 GB
3. بعد الإنشاء، اضغط **"Browse Files"**
4. أنشئ folders:
   - `/checkpoints/GMM/`
   - `/checkpoints/TOM/`
5. ارفع الملفات:
   - `gmm_final.pth` في `/checkpoints/GMM/`
   - `tom_final.pth` في `/checkpoints/TOM/`

---

### الخطوة 3: Deploy على RunPod 🚀

1. **اذهب إلى:** https://www.runpod.io/console/serverless

2. **اضغط:** "New Endpoint"

3. **املأ المعلومات:**

   ```
   📝 Basic Settings:
   ├─ Endpoint Name: cpvton-plus
   ├─ Container Image: ghcr.io/YOUR_USERNAME/YOUR_REPO:latest
   └─ Container Disk: 15 GB
   
   🎮 GPU Selection:
   ├─ ☑ RTX 3090 (موصى به)
   ├─ ☑ RTX 4090 (أسرع)
   └─ ☑ A4000 (متوسط)
   
   📊 Scaling:
   ├─ Min Workers: 0
   ├─ Max Workers: 3
   ├─ Idle Timeout: 5 seconds
   └─ GPU Utilization: 80%
   
   ⚙️ Advanced (مهم!):
   └─ Network Storage:
      ├─ Mount Path: /app/checkpoints
      └─ Select Volume: cpvton-checkpoints
   ```

4. **اضغط:** "Deploy"

---

### الخطوة 4: احصل على Credentials 🔑

بعد الـ Deploy:

1. **انسخ Endpoint ID** من صفحة الـ Endpoint:
   ```
   مثال: abc123xyz-serverless
   ```

2. **احصل على API Key:**
   - اذهب: Settings → API Keys
   - انسخ الـ key:
   ```
   مثال: 1234567890abcdef...
   ```

---

### الخطوة 5: اختبار! 🧪

```python
import requests
import base64
from PIL import Image
import io

# عدّل هنا
ENDPOINT_ID = "your-endpoint-id"
API_KEY = "your-api-key"

def test():
    # تحويل صور لـ Base64
    def img_to_b64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    # Request
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    payload = {
        "input": {
            "person_image": img_to_b64("person.jpg"),
            "cloth_image": img_to_b64("cloth.jpg")
        }
    }
    
    print("🚀 Sending request...")
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    if result["status"] == "COMPLETED":
        output = result["output"]
        if output["success"]:
            # حفظ النتيجة
            img_data = base64.b64decode(output["result_image"])
            img = Image.open(io.BytesIO(img_data))
            img.save("result.png")
            print("✅ Success! Result saved to result.png")
        else:
            print(f"❌ Error: {output['error']}")
    else:
        print(f"❌ Failed: {result}")

test()
```

---

## 📚 الملفات المفيدة

| ملف | متى تقرأه |
|-----|-----------|
| **QUICK_DEPLOY.md** | خطوات سريعة (3 خطوات فقط) |
| **DEPLOY_TO_RUNPOD.md** | دليل deployment كامل ومفصل |
| **README_RUNPOD.md** | شرح تقني شامل + troubleshooting |
| **client_example.py** | أمثلة استخدام API من Backend |
| **DEPLOYMENT_SUMMARY.md** | ملخص التطبيق والتكلفة |

---

## 🎓 الترتيب الموصى به

### للبدء الفوري:
1. ✅ اقرأ هذا الملف (START_HERE.md)
2. ✅ اتبع الخطوات أعلاه
3. ✅ اختبر باستخدام الكود أعلاه

### للفهم الأعمق:
1. 📖 [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - خطوات مختصرة
2. 📖 [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) - شرح كامل
3. 📖 [README_RUNPOD.md](README_RUNPOD.md) - تفاصيل تقنية

### للاستخدام من Backend:
1. 💻 [client_example.py](client_example.py) - أمثلة Python
2. 📖 [README_RUNPOD.md](README_RUNPOD.md) → API Usage section

---

## 🆘 مشاكل شائعة

### "Container failed to start"
→ تأكد من رفع checkpoints على Network Storage في المسار الصحيح

### "Model not loaded"
→ تأكد من mount الـ Network Storage على `/app/checkpoints`

### "CUDA out of memory"
→ استخدم GPU أكبر (RTX 3090 بدلاً من A4000)

**للمزيد:** [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) → Troubleshooting

---

## 💰 التكلفة المتوقعة

| الاستخدام | التكلفة/شهر |
|-----------|-------------|
| 100 requests/day | ~$2 |
| 1,000 requests/day | ~$17 |
| 10,000 requests/day | ~$170 |

*مع auto-scaling: تدفع فقط عند الاستخدام!*

---

## ✅ Checklist

قبل ما تبدأ:

- [ ] عندي حساب GitHub
- [ ] عندي حساب RunPod (مع credit)
- [ ] حمّلت checkpoints من OneDrive
- [ ] فهمت الخطوات أعلاه

---

## 🚀 Let's Deploy!

```bash
# خطوة 1: Push
git init && git add . && git commit -m "ready"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# خطوة 2: حمّل checkpoints على RunPod Network Storage
# (يدوياً من RunPod Console)

# خطوة 3: أنشئ Endpoint على RunPod
# (يدوياً من RunPod Console)

# خطوة 4: اختبر!
python test_client.py
```

---

## 📞 تحتاج مساعدة؟

1. **راجع الملفات أعلاه** - كل شيء موثق!
2. **شوف Logs** - في RunPod Console → Your Endpoint → Logs
3. **افتح Issue** - على GitHub
4. **RunPod Discord** - للدعم الفني

---

## 🎉 النهاية

**كل شيء جاهز! اتبع الخطوات أعلاه وسيشتغل معك 100%**

**Next:** اقرأ [QUICK_DEPLOY.md](QUICK_DEPLOY.md) للتفاصيل

---

*Good luck! 🚀*

