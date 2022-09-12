import re
import os


def find_input_files(tex_file, add_tex_folder=False):
    """Find all of the files that are included, inputted or includegraphics'
    in a tex file.
    Args:
        tex_file: The path of the tex file.
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
