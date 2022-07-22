rule paper:
    input:
        tex = "src/paper/paper.tex"
    output:
        pdf = "out/paper/paper.pdf"
    params:
        outdir = "out/paper/"
    shell:
        "latexmk -outdir={params.outdir} -pdf -shell-escape {input.tex}"
    
