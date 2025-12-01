#!/bin/bash
# Script لبناء Docker image ورفعه

set -e  # إيقاف عند أي خطأ

# ==================== Configuration ====================

DOCKER_USER="${DOCKER_USER:-your-username}"  # عدّل هنا أو export DOCKER_USER
IMAGE_NAME="cpvton-runpod"
VERSION="${VERSION:-latest}"

FULL_IMAGE="${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"

# ==================== Colors ====================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== Functions ====================

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ==================== Pre-flight Checks ====================

print_header "Pre-flight Checks"

# التحقق من Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker غير مثبت!"
    exit 1
fi
print_success "Docker installed"

# التحقق من تسجيل الدخول
if ! docker info | grep -q "Username"; then
    print_warning "لم تسجل دخول Docker!"
    echo "تشغيل: docker login"
    docker login
fi
print_success "Docker logged in"

# التحقق من الملفات المطلوبة
REQUIRED_FILES=(
    "cpvton_infer.py"
    "handler.py"
    "Dockerfile"
    "requirements_runpod.txt"
    "networks.py"
    "grid.png"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "الملف مطلوب: $file"
        exit 1
    fi
done
print_success "All required files present"

# التحقق من checkpoints (تحذير فقط)
if [ ! -f "checkpoints/GMM/gmm_final.pth" ]; then
    print_warning "GMM checkpoint غير موجود"
    print_info "يمكنك تحميله لاحقاً أو استخدام RunPod Network Storage"
fi

if [ ! -f "checkpoints/TOM/tom_final.pth" ]; then
    print_warning "TOM checkpoint غير موجود"
    print_info "يمكنك تحميله لاحقاً أو استخدام RunPod Network Storage"
fi

# ==================== Build ====================

print_header "Building Docker Image"

print_info "Image: ${FULL_IMAGE}"

# Build with progress
docker build \
    --tag "${FULL_IMAGE}" \
    --tag "${DOCKER_USER}/${IMAGE_NAME}:latest" \
    --progress=plain \
    .

print_success "Build completed!"

# ==================== Test (optional) ====================

print_header "Testing Image"

echo "هل تريد اختبار الimage محلياً؟ (y/n)"
read -r test_response

if [[ "$test_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_info "تشغيل container للاختبار..."
    
    # تشغيل مع timeout
    docker run --rm \
        -e DEVICE=cpu \
        -v "$(pwd)/checkpoints:/app/checkpoints" \
        "${FULL_IMAGE}" \
        timeout 10s python cpvton_infer.py || true
    
    print_success "Test completed"
else
    print_warning "تخطي الاختبار"
fi

# ==================== Push ====================

print_header "Pushing to Docker Registry"

echo "هل تريد رفع الimage إلى Docker Hub؟ (y/n)"
read -r push_response

if [[ "$push_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_info "رفع ${FULL_IMAGE}..."
    docker push "${FULL_IMAGE}"
    
    if [ "$VERSION" != "latest" ]; then
        print_info "رفع ${DOCKER_USER}/${IMAGE_NAME}:latest..."
        docker push "${DOCKER_USER}/${IMAGE_NAME}:latest"
    fi
    
    print_success "Push completed!"
else
    print_warning "تخطي الرفع"
fi

# ==================== Summary ====================

print_header "Summary"

echo -e "${GREEN}✓ Image built successfully${NC}"
echo ""
echo "Image name: ${FULL_IMAGE}"
echo "Size: $(docker images ${FULL_IMAGE} --format "{{.Size}}")"
echo ""
print_info "الخطوات التالية:"
echo "  1. اذهب إلى RunPod Console: https://www.runpod.io/console/serverless"
echo "  2. أنشئ Serverless Endpoint جديد"
echo "  3. استخدم الimage: ${FULL_IMAGE}"
echo "  4. إذا لم تضف checkpoints، استخدم Network Storage"
echo ""
print_info "للاختبار المحلي:"
echo "  docker run --gpus all -v \$(pwd)/checkpoints:/app/checkpoints ${FULL_IMAGE}"
echo ""

print_success "Done!"


