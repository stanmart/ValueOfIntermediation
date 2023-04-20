from manim import *
import pandas as pd


class Baseline(Scene):

    def construct(self):

        data = pd.read_csv("out/figures/equilibrium.csv")

        self.next_section("draw_graph")

        self.camera.background_color = WHITE
        Text.set_default(color=BLACK)
        Line.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Brace.set_default(color=BLACK)
        ParametricFunction.set_default(color=BLACK)

        # Create plane
        ax = Axes(
            x_range=[0, 1.5, 0.015],
            y_range=[0, 2.5, 0.02],
            x_length=11,
            y_length=7,
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},

        )
        x_ax_label, y_ax_label = ax.get_axis_labels(x_label=r"N_P", y_label=r"A^*(N_P)")

        # Destiniations
        A_noF =  (ax.plot_line_graph(
            x_values=data["N_P"], y_values=data["A_noF"],
            line_color=BLACK, add_vertex_dots=False
        ))
        A_bench = ax.plot_line_graph(
            data["N_P"], data["A_bench"],
            line_color=BLUE_D, add_vertex_dots=False
        )
        A_barg = ax.plot_line_graph(
            data["N_P"], data["A"],
            line_color=RED_D, add_vertex_dots=False
        )

        pi_P_noF = (ax.plot_line_graph(
            data["N_P"], data["pi_P_noF"],
            line_color=BLACK, add_vertex_dots=False
        ))
        pi_P_bench = ax.plot_line_graph(
            data["N_P"], data["pi_P_bench"],
            line_color=BLUE_D, add_vertex_dots=False
        )
        pi_P_barg = ax.plot_line_graph(
            data["N_P"], data["pi_P"],
            line_color=RED_D, add_vertex_dots=False
        )

        pi_P_noF_scaled = (ax.plot_line_graph(
            data["N_P"], data["pi_P_noF"] * 3,
            line_color=BLACK, add_vertex_dots=False
        ))
        pi_P_bench_scaled = ax.plot_line_graph(
            data["N_P"], data["pi_P_bench"] * 3,
            line_color=BLUE_D, add_vertex_dots=False
        )
        pi_P_barg_scaled = ax.plot_line_graph(
            data["N_P"], data["pi_P"] * 3,
            line_color=RED_D, add_vertex_dots=False
        )

        y_ax_label_pi = MathTex(r"\pi_P")
        y_ax_label_pi.move_to(y_ax_label.get_center())

        # Plotted objects
        f_noF = A_noF.copy()
        f_bench = A_bench.copy()
        f_barg = A_barg.copy()


        # First phase: draw axes
        self.play(Create(ax), Write(x_ax_label), Write(y_ax_label))

        # Second phase: no fringe
        self.next_section("a_nof")
        self.play(Create(f_noF))

        # Third phase: benchmark
        self.next_section("a_bench")
        self.play(Create(f_bench))

        # Fourth phase: bargaining
        self.next_section("a_barg")
        self.play(Create(f_barg))

        # Fifth : platform_profits
        self.next_section("pi_p_all")
        self.play(
            Transform(f_noF, pi_P_noF_scaled),
            Transform(f_bench, pi_P_bench_scaled),
            Transform(f_barg, pi_P_barg_scaled),
            Transform(y_ax_label, y_ax_label_pi)
        )

        self.wait(0.1)
