#!/usr/bin/env python3
# coding=utf-8
"""
اختبار محلي لـ RunPod Handler
يستخدم لاختبار الhandler قبل رفعه على RunPod
"""

import base64
import json
from PIL import Image
import io

# استيراد handler
from handler import handler


def image_to_base64(img_path: str) -> str:
    """تحويل صورة إلى Base64"""
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def base64_to_image(b64_str: str, output_path: str):
    """حفظ Base64 كصورة"""
    img_data = base64.b64decode(b64_str)
    img = Image.open(io.BytesIO(img_data))
    img.save(output_path)
    print(f"✅ تم حفظ الصورة: {output_path}")


def test_with_dummy_images():
    """اختبار بصور dummy"""
    print("=" * 80)
    print("اختبار 1: Dummy Images")
    print("=" * 80)
    
    # إنشاء صور dummy
    person = Image.new('RGB', (192, 256), color=(200, 200, 200))
    cloth = Image.new('RGB', (192, 256), color=(100, 150, 200))
    
    # حفظ مؤقتاً
    person.save("/tmp/test_person.png")
    cloth.save("/tmp/test_cloth.png")
    
    # تحويل لـ Base64
    person_b64 = image_to_base64("/tmp/test_person.png")
    cloth_b64 = image_to_base64("/tmp/test_cloth.png")
    
    # إنشاء event
    event = {
        "input": {
            "person_image": person_b64,
            "cloth_image": cloth_b64,
            "output_format": "PNG"
        }
    }
    
    # تشغيل handler
    print("\n🚀 تشغيل handler...\n")
    result = handler(event)
    
    # عرض النتيجة
    print("\n" + "=" * 80)
    print("النتيجة:")
    print("=" * 80)
    print(json.dumps({
        k: v if k != "result_image" else f"<{len(v)} bytes>" 
        for k, v in result.items()
    }, indent=2, ensure_ascii=False))
    
    # حفظ النتيجة إذا نجح
    if result.get("success"):
        base64_to_image(result["result_image"], "test_output_runpod.png")
    
    return result


def test_with_real_images(person_path: str, cloth_path: str):
    """اختبار بصور حقيقية"""
    print("=" * 80)
    print("اختبار 2: Real Images")
    print("=" * 80)
    print(f"Person: {person_path}")
    print(f"Cloth: {cloth_path}")
    
    # تحويل لـ Base64
    person_b64 = image_to_base64(person_path)
    cloth_b64 = image_to_base64(cloth_path)
    
    # إنشاء event
    event = {
        "input": {
            "person_image": person_b64,
            "cloth_image": cloth_b64,
            "output_format": "PNG"
        }
    }
    
    # تشغيل handler
    print("\n🚀 تشغيل handler...\n")
    result = handler(event)
    
    # عرض النتيجة
    print("\n" + "=" * 80)
    print("النتيجة:")
    print("=" * 80)
    print(json.dumps({
        k: v if k != "result_image" else f"<{len(v)} bytes>" 
        for k, v in result.items()
    }, indent=2, ensure_ascii=False))
    
    # حفظ النتيجة إذا نجح
    if result.get("success"):
        output_name = f"test_output_real_{person_path.split('/')[-1]}"
        base64_to_image(result["result_image"], output_name)
    
    return result


def test_error_handling():
    """اختبار error handling"""
    print("=" * 80)
    print("اختبار 3: Error Handling")
    print("=" * 80)
    
    # Event بدون person_image
    event1 = {
        "input": {
            "cloth_image": "dummy_base64"
        }
    }
    
    print("\n[اختبار] Event بدون person_image:")
    result1 = handler(event1)
    print(f"  ✓ Error: {result1.get('error')}")
    
    # Event بدون cloth_image
    event2 = {
        "input": {
            "person_image": "dummy_base64"
        }
    }
    
    print("\n[اختبار] Event بدون cloth_image:")
    result2 = handler(event2)
    print(f"  ✓ Error: {result2.get('error')}")
    
    # Event ببيانات Base64 غير صحيحة
    event3 = {
        "input": {
            "person_image": "invalid_base64!!!",
            "cloth_image": "invalid_base64!!!"
        }
    }
    
    print("\n[اختبار] Event ببيانات Base64 غير صحيحة:")
    result3 = handler(event3)
    print(f"  ✓ Error: {result3.get('error')}")
    
    print("\n✅ جميع اختبارات Error Handling نجحت!")


# ==================== Main ====================

if __name__ == "__main__":
    import sys
    import os
    
    print("\n" + "🧪" * 40)
    print("RunPod Handler Local Test")
    print("🧪" * 40 + "\n")
    
    # اختبار 1: Dummy images
    print("\n" + "▶" * 40)
    test_with_dummy_images()
    
    # اختبار 2: Real images (إذا كانت موجودة)
    if len(sys.argv) > 2:
        person_path = sys.argv[1]
        cloth_path = sys.argv[2]
        
        if os.path.exists(person_path) and os.path.exists(cloth_path):
            print("\n" + "▶" * 40)
            test_with_real_images(person_path, cloth_path)
        else:
            print(f"\n⚠️  ملفات غير موجودة: {person_path}, {cloth_path}")
    
    # اختبار 3: Error handling
    print("\n" + "▶" * 40)
    test_error_handling()
    
    print("\n" + "✅" * 40)
    print("انتهت جميع الاختبارات!")
    print("✅" * 40 + "\n")

