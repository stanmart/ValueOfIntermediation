rule paper:
    input:
        tex = "src/paper/paper.tex"
    output:
        pdf = "out/paper/paper.pdf"
    params:
        pdf_wo_ext = "out/paper/paper"
    shell:
        "latexmk -pdf -jobname={params.pdf_wo_ext} {input.tex}"
    
