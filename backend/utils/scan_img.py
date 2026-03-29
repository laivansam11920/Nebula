import os
from nudenet import NudeDetector
from utils.image_compressor import compress_image_for_ai
from logs import logger
from configs.duong_dan_thu_muc import duong_dan_hien_tai

detector = NudeDetector()


def check_image_sensitivity(image_path: str) -> dict:
    compressed_path = compress_image_for_ai(image_path)

    try:
        detections = detector.detect(compressed_path)

        EXPLICIT_LABELS = {
            "FEMALE_GENITALIA_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "FEMALE_BREAST_EXPOSED",
            "ANUS_EXPOSED",
            "BUTTOCKS_EXPOSED",
        }
        MILD_LABELS = {
            "FEMALE_BREAST_COVERED",
            "BUTTOCKS_COVERED",
            "BELLY_EXPOSED",
            "ARMPITS_EXPOSED",
        }

        explicit_score = 0.0
        mild_score = 0.0
        explicit_found = []
        mild_found = []

        for det in detections:
            label = det.get("class") or det.get("label")
            conf = det["score"]

            if label in EXPLICIT_LABELS:
                explicit_found.append(label)
                explicit_score = max(explicit_score, conf)
            elif label in MILD_LABELS:
                mild_found.append(label)
                mild_score = max(mild_score, conf)

        if explicit_score > 0:
            score = max(min(round(explicit_score * 10), 10), 5)
            level = (
                "explicit" if score >= 9 else "sensitive" if score >= 7 else "moderate"
            )
            safe_for_work = False
        elif mild_score > 0:
            score = max(min(round(mild_score * 6), 6), 1)
            level = "mild" if score <= 4 else "moderate"
            safe_for_work = score < 4
        else:
            score = 0
            level = "safe"
            safe_for_work = True

        return {
            "score": score,
            "level": level,
            "categories": list(set(explicit_found + mild_found)),
            "reason": f"Phát hiện: {', '.join(set(explicit_found + mild_found)) or 'Không có nội dung nhạy cảm'}",
            "safe_for_work": safe_for_work,
            "raw_detections": detections,
        }

    finally:
        if compressed_path != image_path and os.path.exists(compressed_path):
            try:
                os.remove(compressed_path)
            except Exception as e:
                logger.error(f"{e}", duong_dan_hien_tai())
