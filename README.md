# The value of intermediation

Contains the papers "The Value of Being Indispensable", "Hybrid platforms and bargaining power" and related materials. The main outputs are the following:

 * `out/paper/paper.pdf`: The latest version of "The Value of Being Indispensable"
 * `out/paper/application.pdf`: The latest version of "Hybrid platforms and bargaining power"
 * `out/presentation/*.html`: a number of revealjs presentations about the project

## How to compile

The project is set up so that `pixi` installs required dependencies into a local virtual environment. The exception is latex:

 * `manim` needs latex to render text. See [manim's documentation](texlive-latex-base) for details.
 * `pdflatex`, `biber` and `pdflatex` are needed to compile the papaers.

Other than these, simply [install `pixi`](https://pixi.sh/latest/#installation), and then you can use the following commands to compile the outputs:

 * `pixi run papers` to compile the papers
 * `pixi run presentations` to compile the presentations
 * `pixi run all` to compile everything
 * `pixi run publish` to compile everything and upload the results to Github pages

## Continuous integration

The project uses Github Actions to automatically compile the outputs and upload them to Github pages. First, the following checks must pass:

 * `ruff` for Python linting and formatting
 * `pyright` for Python type checking
 * `codespell` for spell checking

If they do, the `publish` job is triggered, which compiles the outputs and uploads them to `gh-pages` branch. The results can be seen at `stanmart.github.io/ValueOfIntermediation/{output}`.
