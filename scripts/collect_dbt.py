import os

def collect_files(target_dir='models', output_file='project_context.txt'):
    # Determine the project root (one level up from this script)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct absolute paths
    target_path = os.path.join(project_root, target_dir)
    output_path = os.path.join(project_root, output_file)
    
    extensions = ('.sql', '.yml', '.yaml')
    
    with open(output_path, 'w', encoding='utf-8') as f_out:
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    
                    f_out.write(f"\n{'='*50}\n")
                    f_out.write(f"FILE: {file_path}\n")
                    f_out.write(f"{'='*50}\n\n")
                    
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        f_out.write(f_in.read())
                    f_out.write("\n")

if __name__ == "__main__":
    collect_files()
    print("Done! Context collected in file project_context.txt")