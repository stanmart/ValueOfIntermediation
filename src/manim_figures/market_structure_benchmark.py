from manim import *


NUM_FIRMS = 4


class MarketStructure(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        self.next_section("draw_objects")

        firms = []
        for i in range(NUM_FIRMS):
            firm_text = Tex(f"$A_{i + 1}$", color=BLACK, font_size=80)
            firm_text.bg = Rectangle(height=1.5, width=1.5, color=RED, fill_opacity=0.25)
            firm = VGroup(firm_text, firm_text.bg)
            firms.append(firm)

        platform_text = Tex("$P$", color=BLACK, font_size=80)
        platform_text.bg = Rectangle(height=2.5, width=2.5, color=BLUE_D, fill_opacity=0.25)
        platform = VGroup(platform_text, platform_text.bg)

        consumers = Tex("Consumers", color=BLACK, font_size=80)
        consumers.bg = Rectangle(height=1.5, width=5, color=GREEN, fill_opacity=0.25)
        consumers = VGroup(consumers, consumers.bg)

        firms_group = VGroup(*firms)

        all_players = VGroup(firms_group, platform, consumers)

        firms_group.arrange(RIGHT, buff=2)
        all_players.arrange(DOWN, buff=2)

        self.play(FadeIn(all_players))

        # Equations
        consumer_eq = MathTex(r"-\sum p_i", color=BLACK)
        consumer_eq.next_to(consumers, DOWN)

        platform_eq = MathTex(r"\sum F_j", r"+ \pi_P", color=BLACK)
        platform_eq.next_to(platform, LEFT)
        platform_brace = Brace(platform_eq, UP, color=BLACK)
        platform_brace_label = platform_brace.get_text(r"$\varphi_{P}$")
        platform_brace_label.set_color(BLACK)
        platform_brace_gr = VGroup(platform_brace, platform_brace_label)

        firm_eqs = []
        firm_shapleys = []
        for j, firm in enumerate(firms):
            firm_eq = MathTex(r"-c", f"-F_{j+1}", f"+ \\pi_{j+1}", color=BLACK)
            firm_eq.next_to(firm, UP)
            firm_eqs.append(firm_eq)
            brace = Brace(firm_eq[1:], UP, color=BLACK)
            brace_label = brace.get_text(f"$\\varphi_{j+1}$")
            brace_label.set_color(BLACK)
            brace_gr = VGroup(brace, brace_label)
            firm_shapleys.append(brace_gr)

        firm_connections = []
        for firm in firms:
            conn = Line(start = firm.get_bottom(), end = platform.get_top(), color=BLACK)
            firm_connections.append(conn)
        consumer_connection = Line(end = platform.get_bottom(), start = consumers.get_top(), color=BLACK)

        self.play(Create(consumer_connection))


        self.next_section("platform_entry")

        self.play(
            Create(firm_connections[0]),
            Create(firm_connections[1]),
            Create(firm_connections[2])
        )
        self.play(
            Write(firm_eqs[0][:2]),
            Write(firm_eqs[1][:2]),
            Write(firm_eqs[2][:2])
        )
        self.play(
            ReplacementTransform(firm_eqs[0][1].copy(), platform_eq[0]),
            ReplacementTransform(firm_eqs[1][1].copy(), platform_eq[0]),
            ReplacementTransform(firm_eqs[2][1].copy(), platform_eq[0])
        )

        self.next_section("pricing_game")

        self.play(
            Create(consumer_eq)
        )
        self.play(
            ReplacementTransform(consumer_eq.copy(), platform_eq[1]),
            ReplacementTransform(consumer_eq.copy(), firm_eqs[0][2]),
            ReplacementTransform(consumer_eq.copy(), firm_eqs[1][2]),
            ReplacementTransform(consumer_eq.copy(), firm_eqs[2][2])
        )
