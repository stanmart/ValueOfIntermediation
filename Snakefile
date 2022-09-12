from os.path import dirname, basename, splitext
from src.utils.makeutils import find_input_files


rule paper:
    input:
        tex = "src/paper/paper.tex",
        inputs = find_input_files("src/paper/paper.tex"),
        util_script = "src/utils/makeutils.py"
    output:
        pdf = "out/paper/paper.pdf"
    params:
        outdir = lambda wildcards, output:  dirname(output.pdf),
        pdf_wo_ext = lambda wildcards, output: splitext(basename(output.pdf))[0]
    shell:
        "latexmk -pdf -synctex=1 -file-line-error \
                 -outdir={params.outdir} \
                 -jobname={params.pdf_wo_ext} \
                 -interaction=nonstopmode {input.tex}"
