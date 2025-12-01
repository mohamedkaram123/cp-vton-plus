# coding=utf-8
"""
RunPod Serverless Handler لـ CP-VTON+

هذا الـ handler يستقبل requests من RunPod ويعالجها باستخدام CP-VTON+
"""

import base64
import io
import os
import traceback

import runpod
from PIL import Image

from cpvton_infer import CPVTONPlusModel


# ==================== تحميل الموديل مرة واحدة ====================
# يتم تحميل الموديل عند بدء الكونتينر (cold start)
# وليس مع كل request (لتوفير الوقت والموارد)

print("=" * 80)
print("🚀 بدء تحميل CP-VTON+ Model...")
print("=" * 80)

# قراءة المسارات من environment variables (أو استخدام defaults)
GMM_CHECKPOINT = os.getenv("GMM_CHECKPOINT", "/app/checkpoints/GMM/gmm_final.pth")
TOM_CHECKPOINT = os.getenv("TOM_CHECKPOINT", "/app/checkpoints/TOM/tom_final.pth")
DEVICE = os.getenv("DEVICE", "cuda")

try:
    model = CPVTONPlusModel(
        gmm_checkpoint=GMM_CHECKPOINT,
        tom_checkpoint=TOM_CHECKPOINT,
        device=DEVICE
    )
    print("✅ تم تحميل الموديل بنجاح!")
except Exception as e:
    print(f"❌ فشل تحميل الموديل: {e}")
    traceback.print_exc()
    model = None

print("=" * 80)


# ==================== دوال مساعدة ====================

def decode_image(b64_str: str) -> Image.Image:
    """
    فك تشفير Base64 string إلى PIL Image
    
    Args:
        b64_str: Base64 encoded string
        
    Returns:
        PIL Image object
    """
    try:
        data = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(data)).convert("RGB")
        return img
    except Exception as e:
        raise ValueError(f"فشل فك تشفير الصورة: {str(e)}")


def encode_image(img: Image.Image, format="PNG") -> str:
    """
    تشفير PIL Image إلى Base64 string
    
    Args:
        img: PIL Image object
        format: صيغة الصورة (PNG, JPEG, etc.)
        
    Returns:
        Base64 encoded string
    """
    try:
        buf = io.BytesIO()
        img.save(buf, format=format)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"فشل تشفير الصورة: {str(e)}")


# ==================== RunPod Handler ====================

def handler(event):
    """
    RunPod Serverless Handler Function
    
    المدخل المتوقع (event):
    {
        "input": {
            "person_image": "<base64_encoded_image>",
            "cloth_image": "<base64_encoded_image>",
            "output_format": "PNG"  // اختياري (default: PNG)
        }
    }
    
    المخرج:
    {
        "result_image": "<base64_encoded_result>",
        "success": true,
        "message": "Virtual try-on completed successfully"
    }
    
    أو في حالة خطأ:
    {
        "error": "<error_message>",
        "success": false
    }
    """
    
    print("\n" + "="*80)
    print("📥 استلام request جديد...")
    
    # التحقق من تحميل الموديل
    if model is None:
        return {
            "error": "الموديل غير محمل بشكل صحيح. تحقق من logs.",
            "success": False
        }
    
    try:
        # استخراج البيانات من event
        inp = event.get("input", {})
        
        # التحقق من المدخلات المطلوبة
        person_b64 = inp.get("person_image")
        cloth_b64 = inp.get("cloth_image")
        
        if not person_b64:
            return {
                "error": "person_image مطلوب (Base64 encoded)",
                "success": False
            }
        
        if not cloth_b64:
            return {
                "error": "cloth_image مطلوب (Base64 encoded)",
                "success": False
            }
        
        # معلمات اختيارية
        output_format = inp.get("output_format", "PNG").upper()
        if output_format not in ["PNG", "JPEG", "JPG"]:
            output_format = "PNG"
        
        print(f"📊 معلومات Request:")
        print(f"  - Person image: {len(person_b64)} bytes (Base64)")
        print(f"  - Cloth image: {len(cloth_b64)} bytes (Base64)")
        print(f"  - Output format: {output_format}")
        
        # فك تشفير الصور
        print("🔄 فك تشفير الصور...")
        person_img = decode_image(person_b64)
        cloth_img = decode_image(cloth_b64)
        
        print(f"  - Person size: {person_img.size}")
        print(f"  - Cloth size: {cloth_img.size}")
        
        # تشغيل Virtual Try-On
        print("🎨 بدء Virtual Try-On...")
        result_img = model.try_on(person_img, cloth_img)
        
        print(f"  - Result size: {result_img.size}")
        
        # تشفير النتيجة
        print("📤 تشفير النتيجة...")
        result_b64 = encode_image(result_img, format=output_format)
        
        print(f"✅ نجح! حجم النتيجة: {len(result_b64)} bytes (Base64)")
        print("="*80 + "\n")
        
        # إرجاع النتيجة
        return {
            "result_image": result_b64,
            "success": True,
            "message": "Virtual try-on completed successfully",
            "output_size": result_img.size,
            "output_format": output_format
        }
    
    except ValueError as ve:
        # أخطاء validation (صور غير صحيحة، إلخ)
        error_msg = str(ve)
        print(f"❌ خطأ في البيانات: {error_msg}")
        print("="*80 + "\n")
        
        return {
            "error": error_msg,
            "success": False
        }
    
    except Exception as e:
        # أخطاء غير متوقعة
        error_msg = f"خطأ في معالجة الطلب: {str(e)}"
        print(f"❌ {error_msg}")
        traceback.print_exc()
        print("="*80 + "\n")
        
        return {
            "error": error_msg,
            "success": False,
            "traceback": traceback.format_exc()
        }


# ==================== RunPod Entrypoint ====================

if __name__ == "__main__":
    """
    نقطة دخول RunPod Serverless
    
    للتشغيل:
        python handler.py
    """
    
    print("\n" + "🚀" * 40)
    print("Starting RunPod Serverless Worker - CP-VTON+")
    print("🚀" * 40 + "\n")
    
    # بدء RunPod serverless worker
    runpod.serverless.start({
        "handler": handler
    })


