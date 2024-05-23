from manim import (
    BLACK,
    BLUE,
    RED,
    UP,
    WHITE,
    Axes,
    Brace,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    ParametricFunction,
    Scene,
    Tex,
    Text,
    Transform,
    Write,
)
from numpy import exp, log1p


class Baseline(Scene):
    def construct(self):
        self.next_section("draw_graph")

        self.camera.background_color = WHITE  # type: ignore
        Text.set_default(color=BLACK)
        Line.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Brace.set_default(color=BLACK)
        ParametricFunction.set_default(color=BLACK)

        # Create plane
        ax = Axes(
            x_range=[0, 1, 0.05], y_range=[0, 1.1, 0.05], x_length=10, y_length=10
        )
        ax_label = ax.get_x_axis_label(r"s")

        # Destinations
        f_orig = ax.plot(lambda x: log1p(x))
        f_positive = ax.plot(lambda x: x)
        f_negative = ax.plot(lambda x: log1p(exp(1) - 2 + x))

        f_orig_label = ax.get_graph_label(f_orig, "f(N_P, sN_F)", direction=UP)  # type: ignore
        f_positive_label = ax.get_graph_label(f_positive, "f(N_P', sN_F)", direction=UP)  # type: ignore
        f_negative_label = ax.get_graph_label(f_negative, "f(N_P', sN_F)", direction=UP)  # type: ignore

        top_orig = ax.plot(lambda x: log1p(1))
        top_alt = ax.plot(lambda x: 1)

        area_orig = ax.get_area(f_orig, (0, 1), opacity=0.5, color=BLUE)  # type: ignore
        area_fringe_orig = ax.get_area(
            f_orig,
            (0, 1),
            bounded_graph=top_orig,
            opacity=0.5,
            color=RED,  # type: ignore
        )
        area_positive = ax.get_area(f_positive, (0, 1), opacity=0.5, color=BLUE)  # type: ignore
        area_fringe_positive = ax.get_area(
            f_positive,
            (0, 1),
            bounded_graph=top_alt,
            opacity=0.5,
            color=RED,  # type: ignore
        )
        area_negative = ax.get_area(f_negative, (0, 1), opacity=0.5, color=BLUE)  # type: ignore
        area_fringe_negative = ax.get_area(
            f_negative,
            (0, 1),
            bounded_graph=top_alt,
            opacity=0.5,
            color=RED,  # type: ignore
        )

        # Dashed placeholders
        def get_dashed_version(obj):
            dashed = obj.copy()
            dashed.set_stroke(width=1, color=BLACK)
            return DashedVMobject(dashed)

        f_orig_dashed = get_dashed_version(f_orig)
        f_positive_dashed = get_dashed_version(f_positive)
        top_orig_dashed = get_dashed_version(top_orig)
        top_alt_dashed = get_dashed_version(top_alt)

        # Moving objects
        f = f_orig.copy()
        top = top_orig.copy()
        area = area_orig.copy()
        area_fringe = area_fringe_orig.copy()
        f_label = f_orig_label.copy()

        # First phase: create label and original functions
        self.play(Create(ax), Write(ax_label))
        self.play(Create(f), Create(f_label))
        self.wait(0.5)
        self.play(Create(top))
        self.play(FadeIn(area), FadeIn(area_fringe))
        self.add(f_orig_label)  # Have this always displayed

        # Second phase: positive cross derivative
        self.next_section("cross_derivative_positive")
        self.play(
            Transform(f, f_positive),
            Transform(top, top_alt),
            Transform(f_label, f_positive_label),
            Transform(area, area_positive),
            Transform(area_fringe, area_fringe_positive),
            FadeIn(f_orig_dashed),
            FadeIn(top_orig_dashed),
        )

        # Third phase: back to original
        self.next_section("back_to_original")
        self.play(
            Transform(f, f_orig),
            Transform(top, top_orig),
            Transform(f_label, f_orig_label),
            Transform(area, area_orig),
            Transform(area_fringe, area_fringe_orig),
            FadeOut(f_orig_dashed),
            FadeOut(top_orig_dashed),
            FadeIn(f_positive_dashed),
            FadeIn(top_alt_dashed),
        )

        # Fourth phase: negative cross derivative
        self.next_section("cross_derivative_negative")

        self.play(
            Transform(f, f_negative),
            Transform(top, top_alt),
            Transform(f_label, f_negative_label),
            Transform(area, area_negative),
            Transform(area_fringe, area_fringe_negative),
            FadeIn(f_orig_dashed),
            FadeIn(top_orig_dashed),
            FadeOut(top_alt_dashed),
        )
        self.wait(0.1)
