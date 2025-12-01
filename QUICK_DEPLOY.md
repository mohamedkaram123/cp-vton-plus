# ⚡ Quick Deploy - خطوات سريعة

## 🎯 للـ Deploy على RunPod مباشرة (3 خطوات فقط!)

---

## 1️⃣ Push على GitHub

```bash
cd /home/momo/dev/cp-vton-plus

git init
git add .
git commit -m "CP-VTON+ RunPod ready"

# عدّل USERNAME و REPO_NAME
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

✅ GitHub Actions سيبني Docker image تلقائياً!

---

## 2️⃣ حمّل Checkpoints

**تحميل مباشر (wget):**

```bash
# GMM (~76MB)
wget -O gmm_final.pth \
  "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"

# TOM (~85MB)  
wget -O tom_final.pth \
  "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"
```

الملفات المطلوبة:
- `gmm_final.pth` (~76MB)
- `tom_final.pth` (~85MB)

**ارفعهم على RunPod:**

1. اذهب: https://www.runpod.io/console/storage
2. أنشئ Network Volume: `cpvton-checkpoints` (10GB)
3. ارفع الملفات في:
   ```
   /checkpoints/GMM/gmm_final.pth
   /checkpoints/TOM/tom_final.pth
   ```

---

## 3️⃣ Deploy Endpoint

1. اذهب: https://www.runpod.io/console/serverless
2. اضغط **"New Endpoint"**
3. املأ:
   ```
   Name: cpvton-plus
   Image: ghcr.io/USERNAME/REPO_NAME:latest
   GPU: RTX 3090
   Disk: 15 GB
   Workers: 0 → 3
   ```
4. في Advanced → Network Storage:
   - Mount: `/app/checkpoints`
   - Select: `cpvton-checkpoints`
5. **Deploy!**

---

## ✅ جاهز!

انسخ **Endpoint ID** و **API Key** من RunPod

**اختبار:**

```python
import requests, base64

ENDPOINT_ID = "your-id"
API_KEY = "your-key"

url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync"
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "input": {
        "person_image": base64.b64encode(open("person.jpg","rb").read()).decode(),
        "cloth_image": base64.b64encode(open("cloth.jpg","rb").read()).decode()
    }
}

result = requests.post(url, json=payload, headers=headers).json()
print(result)
```

---

## 📚 للمزيد من التفاصيل

- [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) - دليل كامل
- [README_RUNPOD.md](README_RUNPOD.md) - شرح شامل
- [client_example.py](client_example.py) - أمثلة استخدام

---

**🎉 خلصنا! CP-VTON+ شغال على RunPod!**


