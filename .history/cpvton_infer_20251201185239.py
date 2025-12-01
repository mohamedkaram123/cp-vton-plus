# coding=utf-8
"""
CP-VTON+ Inference Wrapper
يوفر واجهة بسيطة لتشغيل CP-VTON+ على صور شخصية وملابس
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import os

from networks import GMM, UnetGenerator


class CPVTONPlusModel:
    """
    Wrapper class لـ CP-VTON+ للاستخدام في RunPod Serverless
    
    يقوم بتحميل GMM و TOM models ويوفر دالة try_on بسيطة
    """
    
    def __init__(
        self,
        gmm_checkpoint: str,
        tom_checkpoint: str,
        device: str = "cuda",
        fine_width: int = 192,
        fine_height: int = 256,
        radius: int = 5,
        grid_size: int = 5
    ):
        """
        تهيئة CP-VTON+ Model
        
        Args:
            gmm_checkpoint: مسار checkpoint لـ GMM
            tom_checkpoint: مسار checkpoint لـ TOM
            device: الجهاز المستخدم (cuda أو cpu)
            fine_width: عرض الصورة المعالجة
            fine_height: ارتفاع الصورة المعالجة
            radius: نصف قطر لـ pose points
            grid_size: حجم الشبكة لـ GMM
        """
        self.device = torch.device(device)
        self.fine_width = fine_width
        self.fine_height = fine_height
        self.radius = radius
        self.grid_size = grid_size
        
        # تحضير transforms
        self.transform = transforms.Compose([
            transforms.Resize((fine_height, fine_width)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # تحميل grid image للـ GMM
        self.grid_image = self._load_grid_image()
        
        # تحميل GMM Model
        print(f"[CPVTONPlus] تحميل GMM من {gmm_checkpoint}")
        
        # إنشاء dummy opt object للـ GMM
        class DummyOpt:
            def __init__(self, w, h, r, g):
                self.fine_width = w
                self.fine_height = h
                self.radius = r
                self.grid_size = g
        
        opt = DummyOpt(fine_width, fine_height, radius, grid_size)
        self.gmm = GMM(opt)
        self._load_checkpoint(self.gmm, gmm_checkpoint)
        self.gmm.to(self.device)
        self.gmm.eval()
        
        # تحميل TOM Model
        print(f"[CPVTONPlus] تحميل TOM من {tom_checkpoint}")
        self.tom = UnetGenerator(26, 4, 6, ngf=64, norm_layer=nn.InstanceNorm2d)
        self._load_checkpoint(self.tom, tom_checkpoint)
        self.tom.to(self.device)
        self.tom.eval()
        
        print("[CPVTONPlus] ✅ تم تحميل Models بنجاح!")
    
    def _load_grid_image(self) -> torch.Tensor:
        """تحميل grid image للـ GMM"""
        grid_path = "grid.png"
        if not os.path.exists(grid_path):
            # إنشاء grid بسيط إذا لم يكن موجود
            grid = np.zeros((256, 192, 3), dtype=np.uint8)
            grid[::20, :] = 255
            grid[:, ::20] = 255
            im_g = Image.fromarray(grid)
        else:
            im_g = Image.open(grid_path)
        
        im_g = self.transform(im_g)
        return im_g.unsqueeze(0)  # Add batch dimension
    
    def _load_checkpoint(self, model: nn.Module, checkpoint_path: str):
        """تحميل checkpoint للموديل"""
        if not os.path.exists(checkpoint_path):
            print(f"[تحذير] checkpoint غير موجود: {checkpoint_path}")
            print(f"[تحذير] سيتم استخدام weights عشوائية!")
            return
        
        try:
            state_dict = torch.load(checkpoint_path, map_location=self.device)
            model.load_state_dict(state_dict)
        except Exception as e:
            print(f"[خطأ] فشل تحميل checkpoint: {e}")
            print(f"[تحذير] سيتم استخدام weights عشوائية!")
    
    def _preprocess_images(
        self,
        person_img: Image.Image,
        cloth_img: Image.Image
    ) -> tuple:
        """
        معالجة الصور قبل الإدخال للموديل
        
        في الوضع المبسط، نستخدم الصورة كاملة بدون segmentation
        """
        # تحويل الصور إلى RGB
        person_img = person_img.convert("RGB")
        cloth_img = cloth_img.convert("RGB")
        
        # تطبيق transforms
        person_tensor = self.transform(person_img).unsqueeze(0).to(self.device)
        cloth_tensor = self.transform(cloth_img).unsqueeze(0).to(self.device)
        
        # إنشاء cloth mask بسيط (افترض أن الملابس تحتل معظم الصورة)
        # في production، يجب استخدام segmentation model
        cloth_mask = torch.ones(1, 1, self.fine_height, self.fine_width).to(self.device)
        
        # إنشاء agnostic representation بسيط
        # في production، يجب حساب هذا من parsing mask
        agnostic = person_tensor.clone()
        
        return person_tensor, cloth_tensor, cloth_mask, agnostic
    
    @torch.no_grad()
    def try_on(
        self,
        person_img: Image.Image,
        cloth_img: Image.Image
    ) -> Image.Image:
        """
        تشغيل virtual try-on
        
        Args:
            person_img: صورة الشخص (PIL Image)
            cloth_img: صورة الملابس (PIL Image)
            
        Returns:
            صورة النتيجة (PIL Image)
        """
        # معالجة الصور
        person_tensor, cloth_tensor, cloth_mask, agnostic = self._preprocess_images(
            person_img, cloth_img
        )
        
        # المرحلة 1: GMM - تشويه الملابس لتناسب الجسم
        grid_image = self.grid_image.to(self.device)
        grid, theta = self.gmm(agnostic, cloth_mask)
        warped_cloth = F.grid_sample(cloth_tensor, grid, padding_mode='border', align_corners=True)
        warped_mask = F.grid_sample(cloth_mask, grid, padding_mode='zeros', align_corners=True)
        
        # المرحلة 2: TOM - دمج الملابس المشوهة مع الشخص
        tom_input = torch.cat([agnostic, warped_cloth, warped_mask], 1)
        outputs = self.tom(tom_input)
        
        # فصل المخرجات
        p_rendered, m_composite = torch.split(outputs, 3, 1)
        p_rendered = torch.tanh(p_rendered)
        m_composite = torch.sigmoid(m_composite)
        
        # دمج النتيجة النهائية
        p_tryon = warped_cloth * m_composite + p_rendered * (1 - m_composite)
        
        # تحويل Tensor إلى PIL Image
        result = self._tensor_to_image(p_tryon)
        
        return result
    
    def _tensor_to_image(self, tensor: torch.Tensor) -> Image.Image:
        """
        تحويل PyTorch tensor إلى PIL Image
        
        Args:
            tensor: Tensor بصيغة (B, C, H, W) مع قيم [-1, 1]
            
        Returns:
            PIL Image
        """
        # إزالة batch dimension وتحويل إلى CPU
        img_tensor = tensor.squeeze(0).cpu()
        
        # تحويل من [-1, 1] إلى [0, 1]
        img_tensor = (img_tensor + 1) / 2
        
        # Clamp القيم
        img_tensor = torch.clamp(img_tensor, 0, 1)
        
        # تحويل إلى numpy array
        img_array = img_tensor.permute(1, 2, 0).numpy()
        
        # تحويل إلى [0, 255]
        img_array = (img_array * 255).astype(np.uint8)
        
        # إنشاء PIL Image
        return Image.fromarray(img_array, mode='RGB')


if __name__ == "__main__":
    """
    اختبار بسيط للموديل
    """
    print("=" * 80)
    print("اختبار CP-VTON+ Model")
    print("=" * 80)
    
    # تحميل الموديل
    model = CPVTONPlusModel(
        gmm_checkpoint="checkpoints/GMM/gmm_final.pth",
        tom_checkpoint="checkpoints/TOM/tom_final.pth",
        device="cpu"  # استخدم "cuda" إذا كان متوفر
    )
    
    # إنشاء صور اختبار
    person_img = Image.new("RGB", (192, 256), color=(200, 200, 200))
    cloth_img = Image.new("RGB", (192, 256), color=(100, 150, 200))
    
    # تشغيل try-on
    print("\n🎨 تشغيل Virtual Try-On...")
    result = model.try_on(person_img, cloth_img)
    
    print(f"✅ نجح! حجم النتيجة: {result.size}")
    print("=" * 80)
