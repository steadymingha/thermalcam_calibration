import os
from PIL import Image, ImageDraw, ImageFont

input_dir = "output"
output_gif = "time_annotated.gif"
duration_per_frame = 100  # 1초

# 모든 .jpg 파일 정렬
image_files = sorted([
    f for f in os.listdir(input_dir) if f.endswith(".jpg")
])

frames = []
# font = ImageFont.load_default()  # 기본 폰트
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 시스템 폰트 경로
font_size = 15  # 글씨 크기 키움
font = ImageFont.truetype(font_path, font_size)
# 기준 크기 (첫 이미지 기준)
first_image = Image.open(os.path.join(input_dir, image_files[0]))
base_size = first_image.size

for fname in image_files:
    base = os.path.splitext(fname)[0]
    if "_" not in base:
        continue

    try:
        _, time_str = base.split("_", 1)
    except ValueError:
        continue

    path = os.path.join(input_dir, fname)
    img = Image.open(path).convert("RGB")
    img = img.resize(base_size)

    draw = ImageDraw.Draw(img)
    text = time_str

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = base_size[0] - text_width - 10
    y = base_size[1] - text_height - 10
    draw.text((x, y), text, fill=(0, 0, 0), font=font)


    frames.append(img)

if frames:
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=duration_per_frame,
        loop=0
    )
