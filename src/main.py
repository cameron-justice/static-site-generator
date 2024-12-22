from pathlib import Path
import os
import shutil

from converters.html_converters import markdown_to_html_node
from markdown_blocks import extract_title

def copy_directory_contents(src: str, dest: str) -> None:
    """
        Utility to copy a directory to another location, clearing the destination directory
    """
    # Clear destination
    contents = os.listdir(dest)
    for item in contents:
        file = Path(Path.joinpath(dest, item))
        if file.is_dir():
            shutil.rmtree(file)
        else:
            Path.unlink(file)


    contents = os.listdir(src)
    for item in contents:
        file = Path(Path.joinpath(src, item))
        if file.is_dir():
            os.mkdir(Path.joinpath(dest, item))
            copy_directory_contents(Path.joinpath(src, item), Path.joinpath(dest, item))
        else:
            shutil.copy(file, Path.joinpath(dest, item))

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generate page from `{from_path}` using `{template_path}` to `{dest_path}`")

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template = f.read()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content.to_html())

    output_file = Path(dest_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(dest_path, mode = "w") as f:
        f.write(template)    

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for item in os.listdir(dir_path_content):
        file = Path(Path.joinpath(dir_path_content, item))
        if file.is_dir():
            generate_pages_recursive(Path.joinpath(dir_path_content, item), template_path, Path.joinpath(dest_dir_path, item))
        else:
            generate_page(file, template_path, Path.joinpath(dest_dir_path, f"{file.stem}.html"))

def main():
    project_path = Path(__file__).parent.parent
    copy_directory_contents(Path.joinpath(project_path, 'static/'), Path.joinpath(project_path, 'public/'))
    generate_pages_recursive(Path.joinpath(project_path, 'content/'), Path.joinpath(project_path, 'template.html'), Path.joinpath(project_path, 'public/'))

if __name__ == "__main__":
    main()
