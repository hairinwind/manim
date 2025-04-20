from manim import *
import numpy as np

# Helper -------------------------------------------------------------

def first_circle_intersection(p0, p1, center, r):
    """Return the FIRST intersection (closest to p0) of the 
    infinite line p0->p1 with the circle (center,r). Assumes p0 is
    **outside** the circle and p1 is **on** the circle (or farther)."""
    d = p1 - p0  # direction
    f = p0 - center

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - r * r

    disc = b * b - 4 * a * c
    if disc < 0:
        raise ValueError("Line does not intersect circle.")

    sqrt_disc = np.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2 * a)  # smaller parameter (closer to p0)
    # t2 = (-b + sqrt_disc) / (2 * a)
    return p0 + t1 * d


class SecantAngleTheorem(Scene):
    """Demonstrates \angle BAC = (\alpha-\beta)/2 for two secants
    intersecting outside a circle, following the scripted steps the user
    provided. """

    def construct(self):
        # -----------------------------------------------------------
        # 1. Draw circle & basic points
        # -----------------------------------------------------------
        radius = 2.5
        circle = Circle(radius=radius)
        self.play(Create(circle))
        self.wait(0.5)

        # Coordinates for key points
        A = np.array([-4, 0, 0])              # external point
        theta_B = PI / 4                      # 45°
        theta_C = -PI / 4                     # -45°
        B = circle.point_at_angle(theta_B)    # point on circle
        C = circle.point_at_angle(theta_C)    # point on circle

        # D & E (first intersections of secants with the circle)
        D = first_circle_intersection(A, B, ORIGIN, radius)
        E = first_circle_intersection(A, C, ORIGIN, radius)

        # Dots & labels
        dotA = Dot(A, color=YELLOW)
        dotB = Dot(B)
        dotC = Dot(C)
        dotD = Dot(D)
        dotE = Dot(E)
        labelA = Tex("A").next_to(dotA, LEFT)
        labelB = Tex("B").next_to(dotB, UR)
        labelC = Tex("C").next_to(dotC, DR)
        labelD = Tex("D").next_to(dotD, UP, buff=0.2)
        labelE = Tex("E").next_to(dotE, DL)

        # Show A first (flash three times)
        self.play(FadeIn(dotA, labelA))

        # Show B & C
        self.play(*map(FadeIn, [dotB, labelB, dotC, labelC]))

        # -----------------------------------------------------------
        # 2. Emphasise small arc BC = alpha
        # -----------------------------------------------------------
        arc_BC = Arc(radius=radius, start_angle=theta_B, angle=theta_C - theta_B)
        arc_BC.set_color(ORANGE)
        alpha_label = MathTex(r"\alpha", color=ORANGE).move_to(arc_BC.point_from_proportion(0.5)+0.25*UP)
        self.play(Create(arc_BC), FadeIn(alpha_label))
        self.wait(0.5)

        # -----------------------------------------------------------
        # 3. Draw secants AB & AC (touch at D & E)
        # -----------------------------------------------------------
        secant_AB = Line(A, CIRCLE := B, color=WHITE)  # placeholder, will update below
        secant_AB.put_start_and_end_on(A, B)
        secant_AC = Line(A, C)
        self.play(Create(secant_AB), Create(secant_AC))
        self.play(FadeIn(dotD, labelD, dotE, labelE))
        self.wait(0.5)

        # -----------------------------------------------------------
        # 4. Emphasise small arc DE = beta
        # -----------------------------------------------------------
        # Draw the small arc directly between D and E
        arc_DE = ArcBetweenPoints(D, E, radius=radius)
        arc_DE.set_color(GREEN)
        beta_label = MathTex(r"\beta", color=GREEN).move_to(
            arc_DE.point_from_proportion(0.5) + 0.3 * IN
        )
        self.play(Create(arc_DE), FadeIn(beta_label))
        self.wait(0.5)

        # -----------------------------------------------------------
        # 5. Draw BE line
        # -----------------------------------------------------------
        BE_line = Line(B, E)
        self.play(Create(BE_line))
        self.wait(0.5)

        # -----------------------------------------------------------
        # 6. Flash triangle BAE three times
        # -----------------------------------------------------------
        triangle_BAE = Polygon(B, A, E, stroke_color=BLUE)
        self.add(triangle_BAE)  # keep outline for flashing
        for _ in range(3):
            self.play(Indicate(triangle_BAE, color=BLUE, scale_factor=1.05))
            self.wait(0.2)

        # -----------------------------------------------------------
        # 7. Flash angle BEC three times
        # -----------------------------------------------------------
        BE_vec = B - E
        CE_vec = C - E
        angle_BEC = Angle(Line(E, B), Line(E, C), radius=0.6, quadrant=(1, 1), color=RED)
        self.add(angle_BEC)
        for _ in range(3):
            self.play(Indicate(angle_BEC, color=RED))
            self.wait(0.2)

        # -----------------------------------------------------------
        # 8. Text area for formulas (right side)
        # -----------------------------------------------------------
        text_shift = RIGHT * 4
        formula1 = MathTex(r"\angle BEC = \angle A + \angle B").shift(text_shift)
        formula2 = MathTex(r"\angle BEC = \frac{\alpha}{2}").next_to(formula1, DOWN, aligned_edge=LEFT)
        formula3 = MathTex(r"\angle DBE = \frac{\beta}{2}").next_to(formula2, DOWN, aligned_edge=LEFT)
        formula4 = MathTex(r"\angle A = \angle BEC - \angle B = \frac{\alpha}{2} - \frac{\beta}{2} = \frac{\alpha - \beta}{2}").next_to(formula3, DOWN, aligned_edge=LEFT)

        for formula in [formula1, formula2, formula3, formula4]:
            self.play(Write(formula, run_time=3, lag_ratio=0.12))
            self.wait(0.8)

        self.wait(2)  # final pause for viewer
