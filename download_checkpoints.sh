#!/bin/bash
# script لتحميل checkpoints من Google Drive

echo "=========================================="
echo "تحميل CP-VTON+ Checkpoints"
echo "=========================================="

# إنشاء directories
mkdir -p checkpoints/GMM
mkdir -p checkpoints/TOM

echo ""
echo "⚠️  ملاحظة مهمة:"
echo "هذه الcheckpoints موجودة على Google Drive ويجب تحميلها يدوياً"
echo ""
echo "GMM Checkpoint:"
echo "https://drive.google.com/file/d/1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT/view?usp=sharing"
echo ""
echo "TOM Checkpoint:"
echo "https://drive.google.com/file/d/1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_/view?usp=sharing"
echo ""
echo "بعد التحميل، حط الملفات في:"
echo "  - checkpoints/GMM/gmm_final.pth"
echo "  - checkpoints/TOM/tom_final.pth"
echo ""
echo "=========================================="

# إذا كنت عايز تستخدم wget/gdown، ممكن تضيف الcommands هنا
# مثال باستخدام gdown (يحتاج: pip install gdown):
# gdown --id <FILE_ID> -O checkpoints/GMM/gmm_final.pth

# يمكن استخدام gdown لتحميل من Google Drive
echo ""
echo "للتحميل التلقائي باستخدام gdown:"
echo "pip install gdown"
echo "gdown 'https://drive.google.com/uc?id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT' -O checkpoints/GMM/gmm_final.pth"
echo "gdown 'https://drive.google.com/uc?id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_' -O checkpoints/TOM/tom_final.pth"
echo ""

echo "هل تريد تحميل checkpoints باستخدام gdown؟ (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    if command -v gdown &> /dev/null; then
        echo "📥 تحميل GMM checkpoint..."
        gdown 'https://drive.google.com/uc?id=1R34WLn5NXvxp_ZY2WmPZWcGo_H7jvKdT' -O checkpoints/GMM/gmm_final.pth
        echo "📥 تحميل TOM checkpoint..."
        gdown 'https://drive.google.com/uc?id=1LV6_lDOYkDluDsdTjDxu3PMhqgSbANP_' -O checkpoints/TOM/tom_final.pth
    else
        echo "❌ gdown غير مثبت. قم بتثبيته أولاً: pip install gdown"
    fi
fi

echo ""
echo "بعد التحميل، تحقق من الملفات:"
ls -lh checkpoints/GMM/ 2>/dev/null || echo "❌ GMM checkpoint غير موجود"
ls -lh checkpoints/TOM/ 2>/dev/null || echo "❌ TOM checkpoint غير موجود"


