[![checks](https://github.com/stanmart/ValueOfIntermediation/actions/workflows/ci.yml/badge.svg)](https://github.com/stanmart/ValueOfIntermediation/actions/workflows/ci.yml)
[![publish](https://github.com/stanmart/ValueOfIntermediation/actions/workflows/publish.yml/badge.svg)](https://github.com/stanmart/ValueOfIntermediation/actions/workflows/publish.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/MIT)

# The value of intermediation

Contains the papers "The Value of Being Indispensable", "Hybrid platforms and bargaining power" and related materials. The main outputs are the following:

 * `out/paper/paper.pdf`: The latest version of "The Value of Being Indispensable"
 * `out/paper/application.pdf`: The latest version of "Hybrid platforms and bargaining power"
 * `out/presentation/*.html`: a number of revealjs presentations about the project:
   * `io_day.html`: A presentation for the Swiss IO day, 2023 (focus on application)
   * `topics_talk`: A talk at the Topics in Micro seminar at UZH (focus on application)
   * `micro_seminar_talk`: A talk at the Topics in Micro seminar at UZH (focus on theory)
   * `fourth_year_seminar_talk`: A presentation for the Fourth Year Seminar at UZH (focus on theory)

## How to compile

The project is set up so that `pixi` installs required dependencies into a local virtual environment. The exception is latex:

 * `manim` needs latex to render text. See [manim's documentation](texlive-latex-base) for details.
 * `pdflatex`, `biber` and `pdflatex` are needed to compile the papaers.

Other than these, simply [install `pixi`](https://pixi.sh/latest/#installation), and then you can use the following commands to compile the outputs:

 * `pixi run papers` to compile the papers
 * `pixi run presentations` to compile the presentations
 * `pixi run all` to compile everything
 * `pixi run publish` to compile everything and upload the results to Github pages

<details>
<summary>Other pixi tasks</summary>
The following commands are available to check the code:

 * `pixi run format` to format the Python code using `ruff`
 * `pixi run lint` to lint the Python code using `ruff`
 * `pixi run typecheck` to typecheck the Python code using `pyright`
 * `pixi run spell` to check the spelling using `codespell`
 * `pixi run check` to run all the checks

The following commands are available to create graphs of snakemake's execution plan:

 * `pixi run dag` to create a directed acyclic graph of the snakemake workflow
 * `pixi run filegraph` to create a file graph of the snakemake workflow
 * `pixi run rulegraph` to create a rule graph of the snakemake workflow

The following commands are used for the CI publish job:

 * `pixi run update-latex-deps` to collect the texlive packages needed for the project and write them to `tl_packages.txt`
 * `pixi run prepare-to-publish` to collect every output file and write them to the `gh-pages` folder

</details>

## Continuous integration

The project uses Github Actions to automatically compile the outputs and upload them to Github pages. First, the following checks must pass:

 * `ruff` for Python linting and formatting
 * `pyright` for Python type checking
 * `codespell` for spell checking

If they do, the `publish` job is triggered, which compiles the outputs and uploads them to `gh-pages` branch. The results can be seen at `stanmart.github.io/ValueOfIntermediation/{output}`.
