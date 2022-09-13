import re
import os
import json
import glob
import typer


app = typer.Typer()


@app.command()
def find_input_files(tex_file: str, remove_prefix: str = "", print_console: bool = False):
    """Find all of the files that are included, inputted or includegraphics'
    in a tex file.
    Args:
        tex_file: The path of the tex file.
        add_tex_folder: Whether to add the folder of the tex file to the
            paths of the included files.
        print_console: Whether to print the paths of the included files
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

    if remove_prefix:
        paths = [path.lstrip(remove_prefix) for path in paths]

    if print_console:
        for path in paths:
            print(path)

    return paths


@app.command()
def find_manim_sections(manim_file: str, print_console: bool = False):
    """Find all of the section names in a manim scirpt.
    Args:
        tex_file: The path of the tex file.
        print_console: Whether to print the paths of the manim sections
    Returns:
        List[str]: the list of manim sections
    """

    with open(manim_file, 'r') as file:
        manim_contents = file.read()

    patterns = [
        re.compile(r"self\.next_section\(\"(.*)\"\)"),
    ]

    sections = sum((pattern.findall(manim_contents) for pattern in patterns), [])

    if print_console:
        for section in sections:
            print(section)

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


@app.command()
def find_videos(qmd_file: str, remove_prefix: str = "", print_console: bool = False):
    """Find the video paths in a qmd file.
    Args:
        qmd_file: The path of the qmd file.
        print_console: Whether to print the video path
    Returns:
        List[str]: the list of video paths
    """

    with open(qmd_file, 'r') as file:
        qmd_contents = file.read()

    patterns = [
        re.compile(r"<video.*src=\"(.*)\".*\/>"),
    ]

    paths = sum((pattern.findall(qmd_contents) for pattern in patterns), [])

    if remove_prefix:
        paths = [path.lstrip(remove_prefix) for path in paths]

    if print_console:
        for path in paths:
            print(path)

    return paths


if __name__ == "__main__":
    app()
