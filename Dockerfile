# Dockerfile لـ CP-VTON+ RunPod Serverless Worker
# يبني Docker image مع كل المتطلبات

# استخدام base image من NVIDIA مع CUDA
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# تعيين working directory
WORKDIR /app

# منع Python من كتابة .pyc files وتفعيل unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# تثبيت system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# إنشاء symlink لـ python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# نسخ requirements أولاً (للاستفادة من Docker cache)
COPY requirements_runpod.txt /app/requirements_runpod.txt

# تثبيت Python dependencies
RUN pip3 install --no-cache-dir -r requirements_runpod.txt

# نسخ الكود الأصلي للـ CP-VTON+
COPY networks.py /app/networks.py
COPY visualization.py /app/visualization.py
COPY grid.png /app/grid.png

# نسخ الكود الجديد (wrapper + handler)
COPY cpvton_infer.py /app/cpvton_infer.py
COPY handler.py /app/handler.py

# إنشاء directory للـ checkpoints
# ⚠️ يجب تحميل checkpoints يدوياً أو mounting volume
RUN mkdir -p /app/checkpoints/GMM /app/checkpoints/TOM

# ==================== تحميل Checkpoints ====================
# الطريقة 1: تحميلهم أثناء build (يزيد حجم الimage ~160MB)
# Uncomment للتحميل أثناء build:
# RUN wget -O /app/checkpoints/GMM/gmm_final.pth \
#     "https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_"
# RUN wget -O /app/checkpoints/TOM/tom_final.pth \
#     "https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT"

# الطريقة 2 (مفضلة): استخدام RunPod Network Storage
# اترك الcheckpoints folder فارغ وحملهم من خلال RunPod Network Storage

# روابط Google Drive المباشرة:
# GMM: https://drive.google.com/uc?export=download&id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_
# TOM: https://drive.google.com/uc?export=download&id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT

# Healthcheck (اختياري)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import torch; print('OK')" || exit 1

# تشغيل handler
CMD ["python", "handler.py"]


