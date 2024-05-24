from platform import system
from shutil import move, which
from os.path import normpath, splitext, basename, dirname
from src.utils.makeutils import find_input_files, find_manim_sections, find_videos


PAPERS, *_ = glob_wildcards("src/paper/{paper}.tex")
PRESENTATIONS, *_ = glob_wildcards("src/presentation/{presentation}.qmd")


rule all:
    input:
        presentations = expand("out/presentation/{presentation}.html", presentation=PRESENTATIONS),
        papers = expand("out/paper/{paper}.pdf", paper=PAPERS)


rule update_latex_deps:
    input:
        deps = expand("out/paper/{paper}.dep", paper=PAPERS)
    output:
        dep_file = "tl_packages.txt"
    shell:
        "python src/utils/makeutils.py collect-latex-packages \
            --add-biber --add-latexmk --add-manim-deps --check-against-tl \
            --output-file tl_packages.txt {input.deps}"


rule papers:
    input:
        papers = expand("out/paper/{paper}.pdf", paper=PAPERS)


rule presentations:
    input:
        expand("out/presentation/{presentation}.html", presentation=PRESENTATIONS)


rule deploy_to_github:
    input:
        # presentations = expand("gh-pages/{presentation}.html", presentation=PRESENTATIONS),
        papers = expand("gh-pages/{paper}.pdf", paper=PAPERS),
        index = "gh-pages/index.html",
        nojekyll = "gh-pages/.nojekyll"
    run:
        import os
        import stat
        from shutil import rmtree
        from subprocess import run
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)
        if os.path.exists("gh-pages/.git"):
            rmtree("gh-pages/.git", onerror=del_rw)
        os.chdir("gh-pages")
        run(["git", "init", "--initial-branch=main"])
        run(["git", "add", "-A"])
        run(["git", "commit", "-m", "Deploy to GitHub Pages"])
        run(["git", "push", "--force", "git@github.com:stanmart/ValueOfIntermediation.git", "main:gh-pages"])
        rmtree(".git", onerror=del_rw)


rule prepare_to_deploy:
    input:
        presentations = expand("out/presentation/{presentation}.html", presentation=PRESENTATIONS),
        papers = expand("out/paper/{paper}.pdf", paper=PAPERS)
    output:
        presentations = expand("gh-pages/{presentation}.html", presentation=PRESENTATIONS),
        papers = expand("gh-pages/{paper}.pdf", paper=PAPERS),
        index = "gh-pages/index.html",
        nojekyll = "gh-pages/.nojekyll"
    run:
        from shutil import copy2
        from pathlib import Path
        for file in input.presentations + input.papers:
            copy2(file, "gh-pages")
        Path("gh-pages/index.html").touch()
        Path("gh-pages/.nojekyll").touch()


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


rule manim_equilibrium_outcomes:
    input:
        script = "src/manim_figures/equilibrium_outcomes.py",
        data = "out/figures/equilibrium_profit_onesided_scale-1_lambda-1.csv"
    output:
        videos = expand(
            "out/manim_figures/videos/equilibrium_outcomes/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/equilibrium_outcomes.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: int(wildcards.height) * 16 // 10,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/equilibrium_outcomes/{wildcards.height}p{wildcards.fps}/sections"


rule manim_market_structure:
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


rule manim_comparative_equilibrium_entry:
    input:
        script = "src/manim_figures/comparative_equilibrium_entry.py"
    output:
        videos = expand(
            "out/manim_figures/videos/comparative_equilibrium_entry/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/comparative_equilibrium_entry.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: wildcards.height,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/comparative_equilibrium_entry/{wildcards.height}p{wildcards.fps}/sections"


rule manim_comparative_n_p_on_shares:
    input:
        script = "src/manim_figures/comparative_n_p_on_shares.py"
    output:
        videos = expand(
            "out/manim_figures/videos/comparative_n_p_on_shares/{height}p{fps}/sections/{section}.mp4",
            section = find_manim_sections("src/manim_figures/comparative_n_p_on_shares.py"),
            allow_missing=True
        )
    params:
        width = lambda wildcards: wildcards.height,
    shell:
        "manim render -qh {input.script} --save_sections --media_dir out/manim_figures \
                      -r {params.width},{wildcards.height} --fps {wildcards.fps} && \
         python src/utils/makeutils.py rename-manim-sections \
                out/manim_figures/videos/comparative_n_p_on_shares/{wildcards.height}p{wildcards.fps}/sections"


rule manim_corollary_comparative:
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
        pdf = "out/paper/{paper}.pdf",
        dep = "out/paper/{paper}.dep"
    params:
        pdf_wo_ext = lambda wildcards, output: splitext(basename(output.pdf))[0],
        outdir = lambda wildcards, output: dirname(output.pdf)
    shell:
        "latexmk -pdf -synctex=1 -file-line-error \
                 -outdir={params.outdir} \
                 -jobname={params.pdf_wo_ext} \
                 -interaction=nonstopmode {input.tex}"


rule figure_equilibrium:
    input:
        script = "src/figures/equilibrium_symbolic.py"
    output:
        csv = "out/figures/equilibrium_{value_function}_{bargaining}_scale-{n_c}_lambda-{lambda_P}.csv"
    shell:
        "python {input.script} {output.csv} \
         --mu 1 --v-p 1 --v-f 1 --i-f 0.05 --n-p-range 0 4.5 --num-obs 200 \
         --n-c {wildcards.n_c} --lambda-p {wildcards.lambda_P} \
         --value-function {wildcards.value_function} --bargaining {wildcards.bargaining}"


rule figure_equilibrium_entry:
    input:
        script = "src/figures/equilibrium_nf.py"
    output:
        fig = "out/figures/equilibrium_entry.pdf"
    shell:
        "python {input.script} {output.fig} \
         --mu 1 --v-p 1 --v-f 1 --i-f 0.2 --n-p 0 --n-p 0.2 --n-f-range 0 1 \
         --num-obs 500 --width 5 --height 3.8 --dpi 300"
