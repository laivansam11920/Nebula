import tempfile
from PIL import Image


def compress_image_for_ai(input_path: str, max_size: tuple = (640, 640)) -> str:
    try:
        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_path = temp_file.name
            temp_file.close()
            img.save(temp_path, format="JPEG", quality=85, optimize=True)
            return temp_path
    except Exception as e:
        print(f"Lỗi khi nén ảnh: {e}")
        return input_path
