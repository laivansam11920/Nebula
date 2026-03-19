import os
import json

def generate_project_structure(root_dir, output_file):
    project_structure = []
    # Các thư mục cần loại bỏ để bản đồ nhìn sạch sẽ
    ignored_dirs = {'venv', 'node_modules', '__pycache__', '.git', 'asset','backend'}
    ignored_files = {'desktop.ini', 'project_structure.json'}

    for root, dirs, files in os.walk(root_dir):
        # Loại bỏ các thư mục không cần thiết ngay tại bước duyệt
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file in files:
            if file in ignored_files:
                continue
                
            file_path = os.path.join(root, file)
            # Lấy vị trí tương đối tính từ gốc dự án
            relative_path = os.path.relpath(file_path, root_dir)
            
            # Thêm thông tin cơ bản: Tên file và Đường dẫn
            project_structure.append({
                "file_name": file,
                "path": relative_path
            })

    with open(output_file, 'w', encoding='utf-8') as json_file:
        # Lưu dưới dạng list các object để dễ tra cứu
        json.dump(project_structure, json_file, ensure_ascii=False, indent=2)
    
    logger(f"Xong rồi og ơi! Đã lập xong bản đồ vị trí file tại: {output_file} :)")

if __name__ == "__main__":
    # Lấy đường dẫn gốc của dự án (thư mục cha của folder tools)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) 
    
    output_path = os.path.join(project_root, "project_structure.json")
    generate_project_structure(project_root, output_path)