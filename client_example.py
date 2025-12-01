#!/usr/bin/env python3
# coding=utf-8
"""
مثال Client للاستدعاء من Backend
يوضح كيفية استخدام CP-VTON+ RunPod API من أي تطبيق
"""

import requests
import base64
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any


class CPVTONClient:
    """
    كلاس client للتواصل مع CP-VTON+ RunPod Endpoint
    """
    
    def __init__(self, endpoint_id: str, api_key: str):
        """
        Initialize client
        
        Args:
            endpoint_id: RunPod endpoint ID
            api_key: RunPod API key
        """
        self.endpoint_id = endpoint_id
        self.api_key = api_key
        self.base_url = f"https://api.runpod.ai/v2/{endpoint_id}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _image_to_base64(self, image_path: str) -> str:
        """تحويل صورة إلى Base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    def _base64_to_image(self, b64_str: str, output_path: str):
        """حفظ Base64 كصورة"""
        img_data = base64.b64decode(b64_str)
        with open(output_path, "wb") as f:
            f.write(img_data)
    
    def try_on_sync(self, 
                    person_image: str, 
                    cloth_image: str,
                    output_path: Optional[str] = None,
                    output_format: str = "PNG") -> Dict[str, Any]:
        """
        Virtual try-on (synchronous)
        ينتظر حتى تنتهي المعالجة ويرجع النتيجة
        
        Args:
            person_image: مسار صورة الشخص
            cloth_image: مسار صورة الملابس
            output_path: (اختياري) مسار حفظ النتيجة
            output_format: صيغة الناتج (PNG أو JPEG)
            
        Returns:
            dict مع النتيجة أو الخطأ
        """
        print(f"🚀 بدء Virtual Try-On...")
        print(f"  - Person: {person_image}")
        print(f"  - Cloth: {cloth_image}")
        
        # تحويل الصور لـ Base64
        person_b64 = self._image_to_base64(person_image)
        cloth_b64 = self._image_to_base64(cloth_image)
        
        # إعداد payload
        payload = {
            "input": {
                "person_image": person_b64,
                "cloth_image": cloth_b64,
                "output_format": output_format
            }
        }
        
        # إرسال request
        url = f"{self.base_url}/runsync"
        
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, headers=self.headers, timeout=120)
            duration = time.time() - start_time
            
            response.raise_for_status()
            result = response.json()
            
            print(f"⏱️  المدة: {duration:.2f} ثانية")
            
            # معالجة النتيجة
            if result.get("status") == "COMPLETED":
                output = result.get("output", {})
                
                if output.get("success"):
                    print(f"✅ نجح!")
                    
                    # حفظ النتيجة إذا طلب
                    if output_path:
                        result_b64 = output["result_image"]
                        self._base64_to_image(result_b64, output_path)
                        print(f"💾 تم الحفظ في: {output_path}")
                    
                    return {
                        "success": True,
                        "result_image": output.get("result_image"),
                        "duration": duration,
                        "size": output.get("output_size")
                    }
                else:
                    error = output.get("error", "Unknown error")
                    print(f"❌ خطأ: {error}")
                    return {
                        "success": False,
                        "error": error
                    }
            else:
                error = result.get("error", result.get("status", "Unknown error"))
                print(f"❌ فشل: {error}")
                return {
                    "success": False,
                    "error": error
                }
        
        except requests.exceptions.Timeout:
            print("❌ انتهت مهلة الانتظار")
            return {
                "success": False,
                "error": "Request timeout"
            }
        
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def try_on_async(self, 
                     person_image: str, 
                     cloth_image: str,
                     output_format: str = "PNG") -> str:
        """
        Virtual try-on (asynchronous)
        يرجع job ID ويمكنك استعلام النتيجة لاحقاً
        
        Args:
            person_image: مسار صورة الشخص
            cloth_image: مسار صورة الملابس
            output_format: صيغة الناتج
            
        Returns:
            job_id: معرف الوظيفة للاستعلام لاحقاً
        """
        print(f"🚀 بدء Virtual Try-On (async)...")
        
        # تحويل الصور لـ Base64
        person_b64 = self._image_to_base64(person_image)
        cloth_b64 = self._image_to_base64(cloth_image)
        
        # إعداد payload
        payload = {
            "input": {
                "person_image": person_b64,
                "cloth_image": cloth_b64,
                "output_format": output_format
            }
        }
        
        # إرسال request
        url = f"{self.base_url}/run"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            job_id = result.get("id")
            print(f"📝 Job ID: {job_id}")
            print(f"🔄 استخدم get_status('{job_id}') للاستعلام")
            
            return job_id
        
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ: {e}")
            raise
    
    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        الاستعلام عن حالة job asynchronous
        
        Args:
            job_id: معرف الوظيفة
            
        Returns:
            dict مع الحالة والنتيجة
        """
        url = f"{self.base_url}/status/{job_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ: {e}")
            raise
    
    def wait_for_completion(self, 
                           job_id: str, 
                           timeout: int = 120,
                           poll_interval: int = 2) -> Dict[str, Any]:
        """
        انتظار اكتمال job async
        
        Args:
            job_id: معرف الوظيفة
            timeout: أقصى وقت انتظار (ثواني)
            poll_interval: فترة الاستعلام (ثواني)
            
        Returns:
            dict مع النتيجة النهائية
        """
        print(f"⏳ انتظار اكتمال job {job_id}...")
        
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                print(f"❌ انتهت المهلة بعد {timeout} ثانية")
                return {
                    "success": False,
                    "error": "Timeout waiting for job completion"
                }
            
            status = self.get_status(job_id)
            job_status = status.get("status")
            
            print(f"  Status: {job_status} ({elapsed:.1f}s)")
            
            if job_status == "COMPLETED":
                output = status.get("output", {})
                if output.get("success"):
                    print(f"✅ نجح!")
                    return output
                else:
                    print(f"❌ فشل: {output.get('error')}")
                    return output
            
            elif job_status in ["FAILED", "CANCELLED"]:
                error = status.get("error", f"Job {job_status.lower()}")
                print(f"❌ {error}")
                return {
                    "success": False,
                    "error": error
                }
            
            # انتظر قبل الاستعلام مرة أخرى
            time.sleep(poll_interval)


# ==================== أمثلة الاستخدام ====================

def example_sync():
    """مثال: استخدام sync API"""
    print("\n" + "="*80)
    print("مثال 1: Synchronous Try-On")
    print("="*80 + "\n")
    
    # إنشاء client
    client = CPVTONClient(
        endpoint_id="YOUR_ENDPOINT_ID",  # ⚠️ عدّل هنا
        api_key="YOUR_API_KEY"            # ⚠️ عدّل هنا
    )
    
    # تشغيل try-on
    result = client.try_on_sync(
        person_image="data/test/image/000001_0.jpg",
        cloth_image="data/test/cloth/000001_1.jpg",
        output_path="result_sync.png"
    )
    
    if result["success"]:
        print(f"\n🎉 نجح!")
        print(f"  - حجم الناتج: {result.get('size')}")
        print(f"  - المدة: {result.get('duration'):.2f}s")
    else:
        print(f"\n❌ فشل: {result['error']}")


def example_async():
    """مثال: استخدام async API"""
    print("\n" + "="*80)
    print("مثال 2: Asynchronous Try-On")
    print("="*80 + "\n")
    
    # إنشاء client
    client = CPVTONClient(
        endpoint_id="YOUR_ENDPOINT_ID",  # ⚠️ عدّل هنا
        api_key="YOUR_API_KEY"            # ⚠️ عدّل هنا
    )
    
    # بدء job async
    job_id = client.try_on_async(
        person_image="data/test/image/000001_0.jpg",
        cloth_image="data/test/cloth/000001_1.jpg"
    )
    
    # انتظار النتيجة
    result = client.wait_for_completion(job_id)
    
    if result.get("success"):
        print(f"\n🎉 نجح!")
        
        # حفظ النتيجة
        result_b64 = result["result_image"]
        with open("result_async.png", "wb") as f:
            f.write(base64.b64decode(result_b64))
        print("💾 تم الحفظ في: result_async.png")
    else:
        print(f"\n❌ فشل: {result.get('error')}")


def example_batch():
    """مثال: معالجة batch من الصور"""
    print("\n" + "="*80)
    print("مثال 3: Batch Processing")
    print("="*80 + "\n")
    
    client = CPVTONClient(
        endpoint_id="YOUR_ENDPOINT_ID",  # ⚠️ عدّل هنا
        api_key="YOUR_API_KEY"            # ⚠️ عدّل هنا
    )
    
    # قائمة بأزواج (person, cloth)
    pairs = [
        ("data/test/image/000001_0.jpg", "data/test/cloth/000001_1.jpg"),
        ("data/test/image/000002_0.jpg", "data/test/cloth/000002_1.jpg"),
        ("data/test/image/000003_0.jpg", "data/test/cloth/000003_1.jpg"),
    ]
    
    results = []
    
    for i, (person, cloth) in enumerate(pairs, 1):
        print(f"\n[{i}/{len(pairs)}] معالجة {person}...")
        
        result = client.try_on_sync(
            person_image=person,
            cloth_image=cloth,
            output_path=f"result_batch_{i}.png"
        )
        
        results.append(result)
    
    # إحصائيات
    success_count = sum(1 for r in results if r["success"])
    print(f"\n📊 النتائج:")
    print(f"  - نجح: {success_count}/{len(results)}")
    print(f"  - فشل: {len(results) - success_count}/{len(results)}")


# ==================== Main ====================

if __name__ == "__main__":
    import sys
    
    print("\n" + "🎨" * 40)
    print("CP-VTON+ Client Examples")
    print("🎨" * 40)
    
    print("\n⚠️  تنبيه: يجب تعديل ENDPOINT_ID و API_KEY في الكود أولاً!")
    print("\nاختر مثال:")
    print("  1. Synchronous Try-On")
    print("  2. Asynchronous Try-On")
    print("  3. Batch Processing")
    print("  (أو اضغط Enter لتشغيل مثال 1)")
    
    choice = input("\n> ").strip() or "1"
    
    if choice == "1":
        example_sync()
    elif choice == "2":
        example_async()
    elif choice == "3":
        example_batch()
    else:
        print("❌ خيار غير صحيح")
    
    print("\n" + "✅" * 40)
    print("انتهى!")
    print("✅" * 40 + "\n")


