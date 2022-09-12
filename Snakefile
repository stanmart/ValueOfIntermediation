from os.path import dirname, basename, splitext
from src.utils.makeutils import find_input_files


rule paper:
    input:
        tex = "src/paper/paper.tex",
        bib = "src/paper/references.bib",
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
    

rule figure_equilibrium_entry:
    conda:
        "envs/python-analysis.yaml"
    input:
        script = "src/figures/equilibrium_nf.py"
    output:
        fig = "out/figures/equilibrium_entry.pdf"
    shell:
        "python {input.script} {output.fig} \
         --b 1 --c 0.2 --n-p 0 --n-p 0.2 --n-f-range 0 1 \
         --num-obs 500 --width 5 --height 3.8 --dpi 300"
