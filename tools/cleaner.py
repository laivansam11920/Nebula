import os
import shutil

def clean_project():
    trash_folders = ['__pycache__', '.pytest_cache']
    ignore_folders = ['.venv', 'node_modules', '.git']
    
    count = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        for d in dirs:
            if d in trash_folders:
                path = os.path.join(root, d)
                logger.log(f"--- Đang dọn dẹp rác của bạn: {path} ---")
                shutil.rmtree(path)
                count += 1
    
    logger.log(f"Đã dọn xong {count} chỗ rác trong code của bạn. Project sạch bóng!")

if __name__ == "__main__":
    clean_project()