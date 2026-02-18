import os

def collect_files(output_file='project_context.txt'):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, output_file)
    
    extensions = ('.sql', '.yml', '.yaml', '.py')
    
    exclude_dirs = {
        'target', 'dbt_packages', 'logs', 'venv_gen', 
        'venv', '.venv', '__pycache__', '.git', '.idea', '.vscode'
    }
    
    with open(output_path, 'w', encoding='utf-8') as f_out:
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file == output_file:
                    continue

                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_root)
                    
                    f_out.write(f"\n{'='*50}\n")
                    f_out.write(f"FILE: {rel_path}\n")
                    f_out.write(f"{'='*50}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f_in:
                            f_out.write(f_in.read())
                    except Exception:
                        pass
                    
                    f_out.write("\n")

if __name__ == "__main__":
    collect_files()
    print("done!")