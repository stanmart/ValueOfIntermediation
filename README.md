# The value of intermediation

Contains the paper "The Value of Intermediation" and related materials. The main outputs are the following:

 * `out/paper/paper.pdf`: The latest version of the paper
 * `out/presentation/presentation.html`: a revealjs presentation about the project

## How to compile

The project is set up so that snakemake handles the installation of the required dependencies into a local virtual environment. The following external dependencies have to be manually installed:

 * A TeX distribution with `pdflatex` and `latexmk` available on the path
 * The `snakemake` workflow management system

Software under the first bullet points can be installed using your preferred method. It is recommended to install snakemake in its own separate conda virtual environment (e.g. `conda create -c conda-forge -c bioconda -n snakemake snakemake`).

The steps to build the project are described in its snakemake file. If snakemake is installed it can be compiled from scratch by running the snakemake command in its root directory:

```bash
    cd /path/to/value-of-intermediation
    conda activate snakemake
    snakemake --cores all --use-conda
```
assuming that snakemake is available in the conda environment named snakemake. The number of jobs to be processed in paralell is set by the `--cores` argument (`e.g. snakemake --cores 4` runs four jobs in parallel).
