from manim import *

class InscribedAngle(Scene):
    """
    演示：圆周角 = 所对弧的一半
    """
    def construct(self):
        # 1️⃣ 画圆 & 标圆心
        circle = Circle(radius=2.5, color=BLUE)
        O = ORIGIN  # 圆心
        self.play(Create(circle))
        O_dot = Dot(O)
        O_lab = MathTex("O").next_to(O_dot, DOWN)
        self.play(FadeIn(VGroup(O_dot, O_lab)))

        # 2️⃣ 取圆上一点 A、B、C（∠ABC 为圆周角）
        A = circle.point_at_angle(35 * DEGREES)
        B = circle.point_at_angle(-150 * DEGREES)
        C = circle.point_at_angle(-45 * DEGREES)

        dots = VGroup(Dot(A), Dot(B), Dot(C))
        labels = VGroup(
            MathTex("A").next_to(A, RIGHT),
            MathTex("B").next_to(B, LEFT),
            MathTex("C").next_to(C, RIGHT)
        )
        self.play(FadeIn(dots), FadeIn(labels))

        # 3️⃣ 画弦 BA、BC 以及半径 OA、OC
        BA, BC = Line(B, A), Line(B, C)
        OA, OC = Line(O, A, color=YELLOW), Line(O, C, color=YELLOW)
        self.play(Create(VGroup(BA, BC)))
        self.play(Create(VGroup(OA, OC)))

        # 4️⃣ 高亮所对弧与中央角
        arc_AC = ArcBetweenPoints(A, C, radius=2.5, color=GREEN)
        central_angle = Angle(OA, OC, radius=0.8, color=GREEN)
        self.play(Create(arc_AC), Create(central_angle))
        theta_lab = MathTex("\\widehat{AC}=\\theta", color=GREEN)\
                    .next_to(central_angle, UP)
        self.play(Write(theta_lab))

        # 5️⃣ 高亮圆周角
        inscribed_angle = Angle(BA, BC, radius=0.8, color=RED)
        self.play(Create(inscribed_angle))
        inscribed_lab = MathTex("\\angle ABC=\\tfrac{\\theta}{2}", color=RED)\
                        .next_to(B, DOWN)
        self.play(Write(inscribed_lab))

        # 6️⃣ 总结公式
        conclusion = MathTex(
            "\\boxed{\\;\\angle ABC\\;=\\;\\tfrac12\\,\\widehat{AC}\\;}"
        ).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)