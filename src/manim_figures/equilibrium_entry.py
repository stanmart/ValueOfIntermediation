from manim import *
from numpy import log
from scipy.optimize import root_scalar


B = 1
C = 0.2


def v(N_F, N_P):
    return (N_F * B + N_P * B) / (N_F * B + N_P * B + 1)


def phi_P(N_F, N_P):
    return 1 - (log(B * N_P + B * N_F + 1) - log(B * N_P + 1)) / (B * N_F)


def phi_F(N_F, N_P):
    return v(N_F, N_P) - phi_P(N_F, N_P)



class Equilibrium(Scene):

    def construct(self):

        self.next_section("draw_axes")

        self.camera.background_color = WHITE
        Text.set_default(color=BLACK)
        Line.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Brace.set_default(color=BLACK)
        ParametricFunction.set_default(color=BLACK)

        # Create plane
        ax = Axes(
            x_range=[0, 1.2, 0.05],
            y_range=[0, 0.7, 0.05],
            x_length=11,
            y_length=6
        )
        ax.shift(UP * 0.5)
        ax_label = MathTex("N_f", color=BLACK)
        ax_label.next_to(ax.get_corner(DOWN + RIGHT), DOWN)

        self.play(Create(ax), Write(ax_label))

        # Non-hybrid
        N_F_bar_val = 0.8
        N_P_val = 0

        self.next_section("char_func")
        v_fun = ax.plot(lambda N_f: v(N_f, N_P_val), color=BLUE_D)
        v_label = ax.get_graph_label(v_fun, "v(t)", direction=DOWN)
        self.play(Create(v_fun), Write(v_label))

        # Profit shares
        self.next_section("fix_players")

        pie_to_share = ax.c2p(N_F_bar_val, v(N_F_bar_val, N_P_val))
        N_F_bar = ax.get_vertical_line(ax.c2p(N_F_bar_val, 0.7), color=BLACK)
        N_F_bar_label = MathTex(r"\bar{N}_F")
        N_F_bar_label.next_to(N_F_bar, DOWN)

        self.play(Create(N_F_bar), Write(N_F_bar_label))

        self.next_section("P_profit_share")
        top_line = ax.get_horizontal_line(pie_to_share, color=BLACK)
        top_graph = ax.plot(lambda x: v(N_F_bar_val, N_P_val))
        area_f = ax.get_area(v_fun, (0, N_F_bar_val), bounded_graph=top_graph, opacity=0.5, color=YELLOW_D)
        area = ax.get_area(v_fun, (0, N_F_bar_val), opacity=0.5, color=BLUE_D)
        self.play(Create(top_line))
        self.play(FadeIn(area), FadeIn(area_f))

        self.next_section("profit_share_point")
        div_point = Dot(color=BLUE_D)
        div_point.move_to(ax.c2p(N_F_bar_val, phi_P(N_F_bar_val, N_P_val)))

        brace_P = BraceBetweenPoints(ax.c2p(N_F_bar_val, 0), div_point.get_bottom())
        label_P = Tex(r"$\varphi_P(v)$")
        label_P.next_to(brace_P, RIGHT)

        brace_F = BraceBetweenPoints(div_point.get_top(), pie_to_share)
        label_F = Tex(r"$\varphi_F(v)$")
        label_F.next_to(brace_F, RIGHT)

        self.play(
            ReplacementTransform(area, brace_P),
            ReplacementTransform(area_f, brace_F)
        )

        self.play(
            FadeIn(div_point),
            Write(label_P), Write(label_F)
        )
        self.play(FadeOut(top_line))

        # Hybrid
        self.next_section("hybrid_case")
        N_P_val_h = 0.2

        v_h_fun = ax.plot(lambda N_f: v(N_f, N_P_val_h), color=RED_D)
        v_h_label = ax.get_graph_label(v_h_fun, "v^h(t)", direction=UP)
        self.play(Create(v_h_fun), Write(v_h_label))

        pie_to_share_h = ax.c2p(N_F_bar_val, v(N_F_bar_val, N_P_val_h))
        top_line_h = ax.get_horizontal_line(pie_to_share_h, color=BLACK)
        top_graph_h = ax.plot(lambda x: v(N_F_bar_val, N_P_val_h))
        area_f_h = ax.get_area(v_h_fun, (0, N_F_bar_val), bounded_graph=top_graph_h, opacity=0.5, color=YELLOW_D)
        area_h = ax.get_area(v_h_fun, (0, N_F_bar_val), opacity=0.5, color=RED_D)
        
        self.play(Create(top_line_h))
        self.play(FadeIn(area_h), FadeIn(area_f_h))

        div_point_h = Dot(color=RED_D)
        div_point_h.move_to(ax.c2p(N_F_bar_val, phi_P(N_F_bar_val, N_P_val_h)))

        brace_P_h = BraceBetweenPoints(div_point_h.get_bottom(), ax.c2p(N_F_bar_val, 0))
        label_P_h = Tex(r"$\varphi_P^h(v)$")
        label_P_h.next_to(brace_P_h, LEFT)

        brace_F_h = BraceBetweenPoints(pie_to_share_h, div_point_h.get_top())
        label_F_h = Tex(r"$\varphi_F^h(v)$")
        label_F_h.next_to(brace_F_h, LEFT)

        self.play(
            ReplacementTransform(area_h, brace_P_h),
            ReplacementTransform(area_f_h, brace_F_h)
        )
        self.play(
            FadeIn(div_point_h), FadeOut(top_line_h),
            Write(label_P_h), Write(label_F_h)
        )

        # Switch to phi_F
        self.next_section("switch_to_phi_F")

        phi_F_point = Dot(color=BLUE_D)
        phi_F_point.move_to(ax.c2p(N_F_bar_val, phi_F(N_F_bar_val, N_P_val)))

        brace_phi_F = BraceBetweenPoints(ax.c2p(N_F_bar_val, 0), phi_F_point.get_bottom())
        label_phi_F = Tex(r"$\varphi_F(v)$")
        label_phi_F.next_to(brace_phi_F, RIGHT)

        phi_F_point_h = Dot(color=RED_D)
        phi_F_point_h.move_to(ax.c2p(N_F_bar_val, phi_F(N_F_bar_val, N_P_val_h)))

        brace_phi_F_h = BraceBetweenPoints(phi_F_point_h.get_bottom(), ax.c2p(N_F_bar_val, 0))
        label_phi_F_h = Tex(r"$\varphi_F^h(v)$")
        label_phi_F_h.next_to(brace_phi_F_h, LEFT)

        self.play(
            FadeOut(brace_P), FadeOut(brace_P_h), FadeOut(label_P), FadeOut(label_P_h)
        )
        self.play(
            ReplacementTransform(div_point, phi_F_point), ReplacementTransform(div_point_h, phi_F_point_h),
            ReplacementTransform(brace_F, brace_phi_F), ReplacementTransform(label_F, label_phi_F),
            ReplacementTransform(brace_F_h, brace_phi_F_h), ReplacementTransform(label_F_h, label_phi_F_h),
        )

        # phi_F functions
        self.next_section("phi_F_functions")

        phi_F_fun = ax.plot(lambda N_f: phi_F(N_f, N_P_val), color=BLUE_D, x_range=(0.02, 1.2))
        phi_F_fun_label = ax.get_graph_label(phi_F_fun, r"\varphi_F(v)", direction=UP)

        phi_F_h_fun = ax.plot(lambda N_f: phi_F(N_f, N_P_val_h), color=RED_D, x_range=(0.02, 1.2))
        phi_F_h_fun_label = ax.get_graph_label(phi_F_h_fun, r"\varphi_F^h(v)", direction=DOWN)

        self.play(
            FadeOut(brace_phi_F), FadeOut(brace_phi_F_h), FadeOut(N_F_bar)
        )
        self.play(
            ReplacementTransform(phi_F_point, phi_F_fun), ReplacementTransform(phi_F_point_h, phi_F_h_fun),
            ReplacementTransform(label_phi_F, phi_F_fun_label), ReplacementTransform(label_phi_F_h, phi_F_h_fun_label)
        )

        # Cost function
        self.next_section("cost_function")

        cost_fun = ax.plot(lambda N_F: C * N_F, color=BLACK)
        cost_fun_label = ax.get_graph_label(cost_fun, "C * N_F", direction=LEFT+UP)

        self.play(
            Create(cost_fun), Write(cost_fun_label)
        )

        # Equilibrium
        self.next_section("equilibrium")

        eq = root_scalar(lambda N_F: phi_F(N_F, N_P_val) - C * N_F, bracket=[0.4, 1.2], method='brentq')
        eq_point = Dot(color=BLUE_D)
        eq_point.move_to(ax.c2p(eq.root, phi_F(eq.root, N_P_val)))

        eq_line = ax.get_vertical_line(eq_point.get_bottom(), color=BLACK)
        eq_line_label = MathTex("N_F^*", color=BLUE_D)
        eq_line_label.next_to(eq_line, DOWN)

        eq_h = root_scalar(lambda N_F: phi_F(N_F, N_P_val_h) - C * N_F, bracket=[0.4, 1.2], method='brentq')
        eq_point_h = Dot(color=RED_D)
        eq_point_h.move_to(ax.c2p(eq_h.root, phi_F(eq_h.root, N_P_val_h)))

        eq_line_h = ax.get_vertical_line(eq_point_h.get_bottom(), color=BLACK)
        eq_line_h_label = MathTex("N_F^{h*}", color=RED_D)
        eq_line_h_label.next_to(eq_line_h, DOWN)

        self.play(
            FadeIn(eq_point), FadeIn(eq_point_h)
        )
        self.play(
            Create(eq_line), Write(eq_line_label),
            Create(eq_line_h), Write(eq_line_h_label)
        )

        self.next_section("N_F_loss")

        brace_loss = BraceBetweenPoints(ax.c2p(eq_h.root, 0), ax.c2p(eq.root, 0))
        loss_label = MathTex("N_F^*", "-", "N_F^{h*}", "> N_P^h", color=BLACK)
        loss_label[0].set_color(BLUE_D)
        loss_label[2].set_color(RED_D)
        loss_label.next_to(brace_loss, DOWN)

        self.play(
            ReplacementTransform(eq_line_label, loss_label[0]),
            ReplacementTransform(eq_line_h_label, loss_label[2]),
            FadeIn(brace_loss), FadeIn(loss_label[1]), FadeIn(loss_label[3])
        )

