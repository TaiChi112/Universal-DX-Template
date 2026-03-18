# 1. กำหนด Base Image: ใช้ Ubuntu เวอร์ชันที่ปรับแต่งมาเพื่อการเป็น DevContainer โดยเฉพาะ
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# 2. (ตัวเลือก) ติดตั้งเครื่องมือพื้นฐานระดับ OS ที่จำเป็นสำหรับโปรเจกต์ทั่วไป
# รันคำสั่งอัปเดตระบบและติดตั้ง curl, wget, git แบบอัตโนมัติ (-y)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    wget \
    git \
    build-essential

# 3. ล้างไฟล์ขยะเพื่อลดขนาดของ Container
RUN apt-get clean && rm -rf /var/lib/apt/lists/*