from manim import *
import numpy as np
# Double the scene’s coordinate frame height to create extra vertical space
config.frame_height = config.frame_height * 2
# Double the output video pixel height to match the increased frame height
config.pixel_height = config.pixel_height * 2

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
        # Double the camera frame's height for extra vertical space, keep width constant
        # -----------------------------------------------------------
        # 1. Draw circle & basic points
        # -----------------------------------------------------------
        radius = 2.5
        # Define the circle’s center and reposition dialog
        center = np.array([0, 2, 0])
        # Store radius for use in helper methods
        self.radius = radius
        circle = Circle(radius=radius).move_to(center)
        self.play(Create(circle))
        self.wait(0.5)

        # Coordinates for key points
        A = center + np.array([-4, 0, 0])              # external point
        theta_B = PI / 4                      # 45°
        theta_C = -PI / 4                     # -45°
        B = circle.point_at_angle(theta_B)    # point on circle
        C = circle.point_at_angle(theta_C)    # point on circle

        # D & E (first intersections of secants with the circle)
        D = first_circle_intersection(A, B, center, radius)
        E = first_circle_intersection(A, C, center, radius)

        # Dots & labels
        dotA = Dot(A, color=YELLOW)
        dotB = Dot(B)
        dotC = Dot(C)
        dotD = Dot(D)
        dotE = Dot(E)
        labelA = Tex("A").next_to(dotA, LEFT)
        labelB = Tex("B").next_to(dotB, UR)
        labelC = Tex("C").next_to(dotC, DR)
        labelD = Tex("D").next_to(dotD, UP, buff=0.5)
        labelE = Tex("E").next_to(dotE, DL)

        # Show A first (flash three times)
        self.play(FadeIn(dotA, labelA))

        # Show B & C
        self.play(*map(FadeIn, [dotB, labelB, dotC, labelC]))

        # -----------------------------------------------------------
        # 2. Emphasise small arc BC = alpha
        # -----------------------------------------------------------
        arc_BC = ArcBetweenPoints(C, B, radius=radius)
        arc_BC.set_color(GREEN)
        alpha_label = MathTex(r"\alpha", color=GREEN).move_to(arc_BC.point_from_proportion(0.5)+0.25*UP)
        self.play(Create(arc_BC), FadeIn(alpha_label))
        # Store the alpha arc for later highlighting
        self.arc_BC = arc_BC
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
        # Store the beta arc for later highlighting
        self.arc_DE = arc_DE
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
        # Draw the triangle outline and keep it on screen
        self.play(Create(triangle_BAE))
        for _ in range(3):
            self.play(Indicate(triangle_BAE, color=BLUE, scale_factor=1.1))
            self.wait(0.2)

        # -----------------------------------------------------------
        # 7. Flash angle BEC three times
        # -----------------------------------------------------------
        # ec_line = Line(E, C)
        # self.add(ec_line)
        # angle_BEC = Angle(Line(E, B), Line(E, C), radius=0.6, other_angle=True, color=RED)
        # self.add(angle_BEC)
        # for _ in range(3):
        #     self.play(
        #         Indicate(angle_BEC, scale_factor=1.1),
        #         Indicate(BE_line, scale_factor=1.1),
        #         Indicate(ec_line, scale_factor=1.1),
        #     )
        #     self.wait(0.2)

        # -----------------------------------------------------------
        # 8. Text area for formulas (right side)
        # -----------------------------------------------------------
        text_shift = DOWN * 2
        formula1 = MathTex(r"\angle BEC = \angle A + \angle B").shift(text_shift)
        self.play(Write(formula1, run_time=3, lag_ratio=0.12))
        #  flash angle
        self.flash_angle(B, E, C)
        self.flash_angle(B, A, E)
        self.flash_angle(E, B, A)
        

        formula2 = MathTex(r"\angle BEC = \frac{\alpha}{2}").next_to(formula1, DOWN, aligned_edge=LEFT)
        self.play(Write(formula2, run_time=3, lag_ratio=0.12))
        self.flash_angle(B, E, C)
        # Highlight the alpha arc
        self.refresh_arc(self.arc_BC)
        
        formula3 = MathTex(r"\angle DBE = \frac{\beta}{2}").next_to(formula2, DOWN, aligned_edge=LEFT)
        self.play(Write(formula3, run_time=3, lag_ratio=0.12))
        self.flash_angle(E, B, D)
        self.refresh_arc(self.arc_DE)

        
        formula4 = MathTex(r"\angle A = \angle BEC - \angle B = \frac{\alpha}{2} - \frac{\beta}{2} = \frac{\alpha - \beta}{2}").next_to(formula3, DOWN, aligned_edge=LEFT).shift(LEFT * 2)
        self.play(Write(formula4, run_time=3, lag_ratio=0.12))

        # for formula in [formula1, formula2, formula3, formula4]:
        #     self.play(Write(formula, run_time=3, lag_ratio=0.12))
        #     self.wait(0.8)

        self.wait(2) 

    def refresh_arc(self, arc):
        """
        Highlights an existing arc using its original color.
        """
        # Flash the given arc three times
        for _ in range(3):
            self.play(Indicate(arc, scale_factor=1.5))
            self.wait(0.2)
        return arc

    def flash_angle(self, point1, vertex, point2):
        line1 = Line(vertex, point2)
        self.add(line1)
        line2 = Line(vertex, point1)
        self.add(line2)
        angle = Angle(line1, line2, radius=0.6, color=RED)
        self.add(angle)
        for _ in range(3):
            self.play(
                Indicate(angle, scale_factor=1.5),
                Indicate(line2, scale_factor=1.5),
                Indicate(line1, scale_factor=1.5),
            )
            self.wait(0.2) # final pause for viewer
