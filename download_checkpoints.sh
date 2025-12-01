#!/bin/bash
# script لتحميل checkpoints من OneDrive

echo "=========================================="
echo "تحميل CP-VTON+ Checkpoints"
echo "=========================================="

# إنشاء directories
mkdir -p checkpoints/GMM
mkdir -p checkpoints/TOM

echo ""
echo "⚠️  ملاحظة مهمة:"
echo "هذه الcheckpoints موجودة على OneDrive ويجب تحميلها يدوياً"
echo ""
echo "الرابط: https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g?e=7ZUxRA"
echo ""
echo "بعد التحميل، حط الملفات في:"
echo "  - checkpoints/GMM/gmm_final.pth"
echo "  - checkpoints/TOM/tom_final.pth"
echo ""
echo "=========================================="

# إذا كنت عايز تستخدم wget/gdown، ممكن تضيف الcommands هنا
# مثال باستخدام gdown (يحتاج: pip install gdown):
# gdown --id <FILE_ID> -O checkpoints/GMM/gmm_final.pth

# للأسف OneDrive links صعبة شوية مع wget مباشرة
# الأفضل تحملهم يدوي أو تستخدم OneDrive API

echo "هل تريد تحميل checkpoints يدوياً الآن؟ (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "افتح الرابط في المتصفح وحمل الملفات يدوياً"
    xdg-open "https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g?e=7ZUxRA" 2>/dev/null || \
    open "https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g?e=7ZUxRA" 2>/dev/null || \
    echo "افتح الرابط: https://1drv.ms/u/c/5435770760f02d2f/ES8t8GAHdzUggFSABAAAAAAB5ArDGoOr2-DU2pyW7NmH-g?e=7ZUxRA"
fi

echo ""
echo "بعد التحميل، تحقق من الملفات:"
ls -lh checkpoints/GMM/ 2>/dev/null || echo "❌ GMM checkpoint غير موجود"
ls -lh checkpoints/TOM/ 2>/dev/null || echo "❌ TOM checkpoint غير موجود"

