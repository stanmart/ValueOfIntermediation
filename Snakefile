from platform import system
from shutil import move, which
from os.path import normpath, splitext, basename, dirname
from src.utils.makeutils import find_input_files, find_manim_sections, find_videos


PAPERS, *_ = glob_wildcards("src/paper/{paper}.tex")
PRESENTATIONS, *_ = glob_wildcards("src/presentation/{pres}.qmd")


rule all:
    input:
        presentations = expand("out/presentation/{presentation}.html", presentation=PRESENTATIONS),
        paper = expand("out/paper/{paper}.pdf", paper=PAPERS)


rule papers:
    input:
        paper = expand("out/paper/{paper}.pdf", paper=PAPERS)


rule deploy_to_github:
    input:
        presentation = "out/presentation/presentation.html",
        script_ps1 = "src/deploy/deploy_to_github.ps1",
        script_sh = "src/deploy/deploy_to_github.sh"
    output:
        presentation = "gh-pages/index.html"
    params:
        sh = "pwsh" if which("pwsh") else ("git bash" if system() == "Windows" else "sh"),
        script = lambda wildcards, input: input.script_ps1 if which("pwsh") else input.script_sh
    shell:
        "{params.sh} {params.script} {input.presentation} {output.presentation}"


rule presentation:
    input:
        qmd = "src/presentation/{presentation}.qmd",
        bib = "src/presentation/references.bib",
        manim_videos = lambda wildcards: find_videos(f"src/presentation/{wildcards.presentation}.qmd", remove_prefix="../.."),
        util_script = "src/utils/makeutils.py"
    output:
        html = "out/presentation/{presentation}.html"
    params:
        output_in_out = lambda wildcards, output: normpath(output.html),
        output_in_src = lambda wildcards, input: normpath(input.qmd.rstrip(".qmd") + ".html"),
        mv = "move" if system() == "Windows" else "mv"
    shell:
         "quarto render {input.qmd} --self-contained && \
          {params.mv} {params.output_in_src} {params.output_in_out}"


rule manim_market_structure:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/market_structure.py"
    output:
        videos = expand(
            "out/manim_figures/videos/market_structure/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/market_structure.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: int(wildcards.height),
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/market_structure/{wildcards.height}p{wildcards.fps}/sections"


rule manim_market_structure_benchmark:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/market_structure_benchmark.py"
    output:
        videos = expand(
            "out/manim_figures/videos/market_structure_benchmark/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/market_structure_benchmark.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: int(wildcards.height),
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/market_structure_benchmark/{wildcards.height}p{wildcards.fps}/sections"


rule manim_equilibrium_entry:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/equilibrium_entry.py"
    output:
        videos = expand(
            "out/manim_figures/videos/equilibrium_entry/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/equilibrium_entry.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: int(16/9 * int(wildcards.height)),
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/equilibrium_entry/{wildcards.height}p{wildcards.fps}/sections"


rule manim_corollary_comparative:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/corollary_comparative.py"
    output:
        videos = expand(
            "out/manim_figures/videos/corollary_comparative/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/corollary_comparative.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: wildcards.height,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/corollary_comparative/{wildcards.height}p{wildcards.fps}/sections"


rule manim_proposition_main:
    conda: "envs/manim.yaml"
    input:
        script = "src/manim_figures/proposition_main.py"
    output:
        videos = expand(
            "out/manim_figures/videos/proposition_main/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/proposition_main.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: wildcards.height,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/proposition_main/{wildcards.height}p{wildcards.fps}/sections"


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
        tex = "src/paper/{paper}.tex",
        bib = "src/paper/references.bib",
        inputs = lambda wildcard: find_input_files(f"src/paper/{wildcard.paper}.tex"),
        util_script = "src/utils/makeutils.py"
    output:
        pdf = "out/paper/{paper}.pdf"
    params:
        pdf_wo_ext = lambda wildcards, output: splitext(basename(output.pdf))[0],
        outdir = lambda wildcards, output: dirname(output.pdf)
    shell:
        "latexmk -pdf -synctex=1 -file-line-error \
                 -outdir={params.outdir} \
                 -jobname={params.pdf_wo_ext} \
                 -interaction=nonstopmode {input.tex}"


rule figure_equilibrium:
    conda:
        "envs/python-analysis.yaml"
    input:
        script = "src/figures/equilibrium.py"
    output:
        csv = "out/figures/equilibrium.csv"
    shell:
        "python {input.script} {output.csv} \
         --mu 1 --v-p 1 --v-f 1 --i-f 0.2 --n-p-range 0 1 --num-obs 200"


rule figure_equilibrium_entry:
    conda:
        "envs/python-analysis.yaml"
    input:
        script = "src/figures/equilibrium_nf.py"
    output:
        fig = "out/figures/equilibrium_entry.pdf"
    shell:
        "python {input.script} {output.fig} \
         --mu 1 --v-p 1 --v-f 1 --i-f 0.2 --n-p 0 --n-p 0.2 --n-f-range 0 1 \
         --num-obs 500 --width 5 --height 3.8 --dpi 300"


rule filegraph:
    conda: "envs/graphviz.yaml"
    input:
        "Snakefile"
    output:
        "build_graphs/filegraph.pdf"
    shell:
        "snakemake --filegraph | dot -Tpdf > build_graphs/filegraph.pdf"

rule rulegraph:
    conda: "envs/graphviz.yaml"
    input:
        "Snakefile"
    output:
        "build_graphs/rulegraph.pdf"
    shell:
        "snakemake --rulegraph | dot -Tpdf > build_graphs/rulegraph.pdf"

rule dag:
    conda: "envs/graphviz.yaml"
    input:
        "Snakefile"
    output:
        "build_graphs/dag.pdf"
    shell:
        "snakemake --dag | dot -Tpdf > build_graphs/dag.pdf"
