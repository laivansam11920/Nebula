import os

def collect_code(target_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(target_dir):
            # Loại bỏ các folder rác/ẩn để AI đỡ rối
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'): # Chỉ lấy file Python
                    file_path = os.path.join(root, file)
                    f.write(f"## File: {file_path}\n")
                    f.write("```python\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as code_f:
                            f.write(code_f.read())
                    except Exception as e:
                        f.write(f"# Error reading file: {e}")
                    f.write("\n```\n\n")

if __name__ == "__main__":
    collect_code('.', 'project_for_ai.md')
    logger("Xong rồi og! File 'project_for_ai.md' đã sẵn sàng.")