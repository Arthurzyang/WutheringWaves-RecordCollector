import os

def generate_project_structure(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(dirpath)))
        subindent = ' ' * 4 * (level + 1)
        for filename in filenames:
            print('{}{}'.format(subindent, filename))

if __name__ == "__main__":
    root_directory = input("请输入项目根目录路径: ").strip()
    generate_project_structure(root_directory)
