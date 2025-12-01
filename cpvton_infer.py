# coding=utf-8
"""
CP-VTON+ Inference Wrapper
تغليف CP-VTON+ في كلاس بسيط للاستخدام في RunPod أو أي API
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from PIL import Image, ImageDraw
import numpy as np
import json
import os
import io

from networks import GMM, UnetGenerator, load_checkpoint


class CPVTONPlusModel:
    """
    كلاس لتشغيل CP-VTON+ بشكل مبسط
    يتطلب:
    - checkpoints للـ GMM و TOM
    - صور مع preprocessing (parsing, pose, masks)
    """
    
    def __init__(self, 
                 gmm_checkpoint="/app/checkpoints/GMM/gmm_final.pth",
                 tom_checkpoint="/app/checkpoints/TOM/tom_final.pth",
                 device="cuda",
                 fine_width=192,
                 fine_height=256):
        """
        تحميل موديلات GMM و TOM
        
        Args:
            gmm_checkpoint: مسار checkpoint الـ GMM
            tom_checkpoint: مسار checkpoint الـ TOM  
            device: cuda أو cpu
            fine_width: عرض الصور (192)
            fine_height: طول الصور (256)
        """
        self.device = device
        self.fine_width = fine_width
        self.fine_height = fine_height
        
        # تحميل GMM (Geometric Matching Module)
        print(f"[CPVTONPlus] تحميل GMM من {gmm_checkpoint}")
        self.gmm = self._load_gmm(gmm_checkpoint)
        
        # تحميل TOM (Try-On Module)  
        print(f"[CPVTONPlus] تحميل TOM من {tom_checkpoint}")
        self.tom = self._load_tom(tom_checkpoint)
        
        # Image transforms
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # تحميل grid image (ثابت)
        self.grid_image = self._load_grid_image()
        
        print("[CPVTONPlus] تم تحميل الموديلات بنجاح!")
    
    def _load_gmm(self, checkpoint_path):
        """تحميل GMM model"""
        # إنشاء opt object مبسط
        class Opt:
            fine_width = self.fine_width
            fine_height = self.fine_height
            grid_size = 5
        
        opt = Opt()
        model = GMM(opt)
        
        if os.path.exists(checkpoint_path):
            load_checkpoint(model, checkpoint_path)
        else:
            print(f"[تحذير] checkpoint غير موجود: {checkpoint_path}")
            print("[تحذير] سيتم استخدام weights عشوائية!")
        
        model.to(self.device)
        model.eval()
        return model
    
    def _load_tom(self, checkpoint_path):
        """تحميل TOM model"""
        # CP-VTON+ uses 26 input channels (vs 25 in CP-VTON)
        model = UnetGenerator(26, 4, 6, ngf=64, norm_layer=nn.InstanceNorm2d)
        
        if os.path.exists(checkpoint_path):
            load_checkpoint(model, checkpoint_path)
        else:
            print(f"[تحذير] checkpoint غير موجود: {checkpoint_path}")
            print("[تحذير] سيتم استخدام weights عشوائية!")
        
        model.to(self.device)
        model.eval()
        return model
    
    def _load_grid_image(self):
        """تحميل grid image المستخدم في GMM"""
        grid_path = "grid.png"
        if os.path.exists(grid_path):
            im_g = Image.open(grid_path)
            im_g = self.transform(im_g)
            return im_g
        else:
            print("[تحذير] grid.png غير موجود، سيتم إنشاء grid فارغ")
            # إنشاء grid أبيض بسيط
            grid = Image.new('RGB', (self.fine_width, self.fine_height), (255, 255, 255))
            return self.transform(grid)
    
    def preprocess_images(self, person_img, cloth_img):
        """
        معالجة مبدئية للصور
        يجب أن تكون الصور بحجم 192x256
        
        Args:
            person_img: PIL Image للشخص
            cloth_img: PIL Image للملابس
            
        Returns:
            dict مع الصور المعالجة
        """
        # Resize إذا لزم الأمر
        if person_img.size != (self.fine_width, self.fine_height):
            person_img = person_img.resize((self.fine_width, self.fine_height), Image.BICUBIC)
        
        if cloth_img.size != (self.fine_width, self.fine_height):
            cloth_img = cloth_img.resize((self.fine_width, self.fine_height), Image.BICUBIC)
        
        # تحويل لـ tensors
        person_tensor = self.transform(person_img)  # [-1, 1]
        cloth_tensor = self.transform(cloth_img)    # [-1, 1]
        
        return {
            'person': person_tensor,
            'cloth': cloth_tensor,
            'person_pil': person_img,
            'cloth_pil': cloth_img
        }
    
    def create_simple_mask(self, cloth_img):
        """
        إنشاء mask بسيط للملابس (binary thresholding)
        للاستخدام المبسط بدون cloth-mask جاهز
        
        Args:
            cloth_img: PIL Image للملابس
            
        Returns:
            torch tensor mask [1, H, W]
        """
        # تحويل لـ grayscale
        gray = cloth_img.convert('L')
        mask_array = np.array(gray)
        
        # Simple threshold (اعتبار كل شيء فوق 240 هو background)
        mask_array = (mask_array < 240).astype(np.float32)
        
        mask = torch.from_numpy(mask_array).unsqueeze(0)
        return mask
    
    def create_dummy_parse(self, height, width):
        """
        إنشاء parsing map dummy للتجربة السريعة
        في الواقع يجب استخدام CIHP_PGN أو Graphonomy
        
        Returns:
            tensors: shape, head, pose_map
        """
        # Shape: كامل الجسم (dummy)
        shape = torch.ones(1, height, width) * 0.5  # gray
        
        # Head: المنطقة العلوية (dummy)
        head = torch.ones(1, height, width) * -1
        head_height = height // 4
        head[:, :head_height, :] = 0.5  # منطقة الرأس
        
        # Pose map: 18 keypoints (dummy - كلهم أصفار)
        pose_map = torch.zeros(18, height, width)
        
        return shape, head, pose_map
    
    def try_on(self, 
               person_img: Image.Image, 
               cloth_img: Image.Image,
               parse_img: Image.Image = None,
               pose_keypoints: dict = None,
               cloth_mask: Image.Image = None) -> Image.Image:
        """
        Virtual try-on رئيسي
        
        Args:
            person_img: صورة الشخص (PIL Image)
            cloth_img: صورة الملابس (PIL Image)
            parse_img: (اختياري) parsing map للشخص
            pose_keypoints: (اختياري) OpenPose keypoints
            cloth_mask: (اختياري) mask الملابس
            
        Returns:
            PIL Image: صورة الناتج
            
        ملاحظة:
            للحصول على نتائج جيدة، يجب توفير:
            - parse_img من CIHP_PGN أو Graphonomy
            - pose_keypoints من OpenPose COCO-18
            - cloth_mask binary mask
        """
        with torch.no_grad():
            # Preprocessing
            processed = self.preprocess_images(person_img, cloth_img)
            
            # إنشاء/تحميل المدخلات المطلوبة
            cloth_tensor = processed['cloth'].unsqueeze(0).to(self.device)
            
            # Cloth mask
            if cloth_mask is not None:
                cm_array = np.array(cloth_mask.convert('L'))
                cm_array = (cm_array >= 128).astype(np.float32)
                cm = torch.from_numpy(cm_array).unsqueeze(0).unsqueeze(0)
            else:
                # استخدام mask مبسط
                cm = self.create_simple_mask(processed['cloth_pil']).unsqueeze(0)
            
            cm = cm.to(self.device)
            
            # Agnostic representation (shape + head + pose)
            # في حالة عدم وجود parsing/pose حقيقي، نستخدم dummy
            if parse_img is None or pose_keypoints is None:
                print("[تحذير] لا يوجد parsing/pose، استخدام dummy data")
                print("[تحذير] النتيجة لن تكون دقيقة! استخدم CIHP_PGN + OpenPose للنتائج الأفضل")
                
                shape, head, pose_map = self.create_dummy_parse(
                    self.fine_height, self.fine_width
                )
            else:
                # TODO: معالجة parsing و pose الحقيقي
                # هنا يجب إضافة كود معالجة parse_img و pose_keypoints
                raise NotImplementedError("معالجة parsing/pose الحقيقي لم يتم تطبيقها بعد")
            
            # Concatenate agnostic representation
            agnostic = torch.cat([shape, head, pose_map], 0).unsqueeze(0).to(self.device)
            
            # ====== STAGE 1: GMM (Geometric Matching) ======
            grid, theta = self.gmm(agnostic, cm)
            
            # Warp cloth & mask
            warped_cloth = F.grid_sample(cloth_tensor, grid, padding_mode='border')
            warped_mask = F.grid_sample(cm, grid, padding_mode='zeros')
            
            # ====== STAGE 2: TOM (Try-On Module) ======
            # Parse cloth mask (dummy - في الواقع يجب أن يكون من parsing)
            pcm = (cm > 0.5).float()  # binary mask
            
            # TOM input: agnostic + warped_cloth + warped_mask
            tom_input = torch.cat([agnostic, warped_cloth, warped_mask], 1)
            
            # Generate output
            outputs = self.tom(tom_input)
            p_rendered, m_composite = torch.split(outputs, 3, 1)
            p_rendered = torch.tanh(p_rendered)
            m_composite = torch.sigmoid(m_composite)
            
            # Final composition
            p_tryon = warped_cloth * m_composite + p_rendered * (1 - m_composite)
            
            # Convert back to PIL Image
            result_tensor = p_tryon.squeeze(0).cpu()
            result_tensor = (result_tensor + 1) / 2.0  # [-1,1] -> [0,1]
            result_tensor = torch.clamp(result_tensor, 0, 1)
            
            # To PIL
            result_np = result_tensor.permute(1, 2, 0).numpy()
            result_np = (result_np * 255).astype(np.uint8)
            result_img = Image.fromarray(result_np)
            
            return result_img
    
    def try_on_batch(self, person_images, cloth_images):
        """
        معالجة batch من الصور
        
        Args:
            person_images: list of PIL Images
            cloth_images: list of PIL Images
            
        Returns:
            list of PIL Images
        """
        results = []
        for person, cloth in zip(person_images, cloth_images):
            result = self.try_on(person, cloth)
            results.append(result)
        return results


# ==================== وظائف مساعدة ====================

def load_image_from_base64(b64_str: str) -> Image.Image:
    """تحويل Base64 string إلى PIL Image"""
    import base64
    data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(data)).convert("RGB")


def image_to_base64(img: Image.Image, format="PNG") -> str:
    """تحويل PIL Image إلى Base64 string"""
    import base64
    buf = io.BytesIO()
    img.save(buf, format=format)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


# ==================== للتجربة المحلية ====================

if __name__ == "__main__":
    """
    تجربة محلية للموديل
    الاستخدام:
        python cpvton_infer.py
    """
    import sys
    
    print("=" * 60)
    print("CP-VTON+ Inference Test")
    print("=" * 60)
    
    # تحميل الموديل
    model = CPVTONPlusModel(
        gmm_checkpoint="checkpoints/GMM/gmm_final.pth",
        tom_checkpoint="checkpoints/TOM/tom_final.pth",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    
    # تجربة بسيطة
    print("\n[اختبار] إنشاء صور dummy...")
    person_img = Image.new('RGB', (192, 256), color=(200, 200, 200))
    cloth_img = Image.new('RGB', (192, 256), color=(100, 150, 200))
    
    print("[اختبار] تشغيل try_on...")
    result = model.try_on(person_img, cloth_img)
    
    print(f"[نجح] حجم الناتج: {result.size}")
    result.save("test_output.png")
    print("[نجح] تم حفظ النتيجة في test_output.png")
    
    print("\n" + "=" * 60)
    print("✓ الاختبار نجح!")
    print("=" * 60)

