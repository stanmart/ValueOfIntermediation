import re
import os
import json
import glob
import typer


app = typer.Typer()


@app.command()
def find_input_files(tex_file: str, add_tex_folder: bool = False):
    """Find all of the files that are included, inputted or includegraphics'
    in a tex file.
    Args:
        tex_file: The path of the tex file.
        add_tex_folder: Whether to add the folder of the tex file to the
            paths of the included files.
    Returns:
        List[str]: the list of included files
    """

    with open(tex_file, 'r') as file:
        tex_contents = file.read()

    patterns = [
        re.compile(r"\\input\{(.*)\}"),
        re.compile(r"\\include\{(.*)\}"),
        re.compile(r"\\includegraphics(?:\[.*\])?\{(.*)\}")
    ]

    paths = sum((pattern.findall(tex_contents) for pattern in patterns), [])
    if add_tex_folder:
        prefix = os.path.dirname(tex_file)
        paths = [os.path.join(prefix, path) for path in paths]

    return paths


@app.command()
def find_manim_sections(manim_file: str):
    """Find all of the section names in a manim scirpt.
    Args:
        tex_file: The path of the tex file.
    Returns:
        List[str]: the list of included files
    """

    with open(manim_file, 'r') as file:
        manim_contents = file.read()

    patterns = [
        re.compile(r"self\.next_section\(\"(.*)\"\)"),
    ]

    sections = sum((pattern.findall(manim_contents) for pattern in patterns), [])
    return sections


@app.command()
def rename_manim_sections(section_dir: str):
    """Rename all of the section names in a manim sections folder.
    Args:
        section_dir: The path of the section directory.
    Returns:
        None
    """

    os.chdir(section_dir)
    section_json = glob.glob("*.json")[0]
    
    with open(section_json, 'r') as file:
        section_contents = json.load(file)

    for section in section_contents:
        os.rename(section["video"], section["name"] + ".mp4")


if __name__ == "__main__":
    app()
