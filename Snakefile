from platform import system
from shutil import move
from os.path import normpath
from src.utils.makeutils import find_input_files, find_manim_sections, find_videos


rule presentation:
    input:
        qmd = "src/presentation/presentation.qmd",
        bib = "src/presentation/references.bib",
        manim_videos = find_videos("src/presentation/presentation.qmd", remove_prefix="../..")
    output:
        html = "out/presentation/presentation.html"
    params:
        output_in_out = lambda wildcards, output: normpath(output.html),
        output_in_src = lambda wildcards, input: normpath(input.qmd.rstrip(".qmd") + ".html"),
        mv = "move" if system() == "Windows" else "mv"
    shell:
         "quarto render {input.qmd} --self-contained && \
          {params.mv} {params.output_in_src} {params.output_in_out}"


rule manim_shapley_value:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/shapley_value_demo.py"
    output:
        videos = expand(
            "out/manim_figures/videos/shapley_value_demo/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/shapley_value_demo.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: int(wildcards.height) * 4 // 3,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/shapley_value_demo/{wildcards.height}p{wildcards.fps}/sections"


rule paper:
    input:
        tex = "src/paper/paper.tex",
        bib = "src/paper/references.bib",
        inputs = find_input_files("src/paper/paper.tex"),
        util_script = "src/utils/makeutils.py"
    output:
        pdf = "out/paper/paper.pdf"
    params:
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
