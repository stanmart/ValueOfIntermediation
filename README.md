# The value of intermediation

Contains the papers "The Value of Being Indispensable", "Hybrid platforms and bargaining power" and related materials. The main outputs are the following:

 * `out/paper/paper.pdf`: The latest version of "The Value of Being Indispensable"
 * `out/paper/application.pdf`: The latest version of "Hybrid platforms and bargaining power"
 * `out/presentation/*.html`: a number of revealjs presentations about the project

## How to compile

The project is set up so that `pixi` installs required dependencies into a local virtual environment. The exception is latex-related stuff:

 * `manim` needs latex to render text. See [manim's documentation](texlive-latex-base) for details.
 * Even though the project uses `tectonic` to render latex, it still needs `biber` to compile the bibliography. You need to install it separately.

Other than these, simply [install `pixi`](https://pixi.sh/latest/#installation), and then you can use the following commands to compile the outputs:

 * `pixi run papers` to compile the papers
 * `pixi run presentations` to compile the presentations
 * `pixi run all` to compile everything
 * `pixi run publish` to compile everything and upload the results to Github pages

