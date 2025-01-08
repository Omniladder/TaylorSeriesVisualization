from manim import *
import math as m
import sympy as sp

class DefaultTemplate(Scene):
    def construct(self):
        
        self.camera.background_color = WHITE

        axes = Axes(
            x_range=[-2 * PI, 2 * PI, 1],  # x-axis range: (min, max, step)
            y_range=[-4, 4, 1],  # y-axis range: (min, max, step)
            tips=False,
            axis_config={"color": BLACK},
        )

        function = sp.exp

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        xInput, yInput = sp.symbols('x y')
        d_n = function(xInput) #Holds the nth Derivate

        taylorText = Text("Taylor Series Approximation").set_color(BLACK)
        taylorText.scale(.5)
        taylorText.shift(np.array([-3.5, 2.5, 0]))

        cosGraph = axes.plot(function, color=GOLD_E)  # Example: y = x^2
        taylorGraph = axes.plot(lambda x: 0, color=GREEN_E)  # Example: y = x^2
        graph_label = axes.get_graph_label(cosGraph, label='sin(x)')

        graph_label.shift([0,.25,0])

        taylorSeries = VGroup(axes, taylorText, cosGraph, taylorGraph, graph_label, y_label, x_label)

        taylorSeries.save_state()

        # Add the axes and labels to the scene
        self.play(Create(axes), Write(x_label), Write(y_label), Write(taylorText))
        self.play(Create(cosGraph), Create(taylorGraph), Write(graph_label), run_time = 2)

        f = 0 * xInput

        for i in range(10):
            f = f + d_n.subs(xInput, 0) / m.factorial(i) * xInput ** i
            d_n = sp.diff(d_n, xInput)



            self.play(Transform(taylorGraph, axes.plot(sp.Lambda(xInput,f), color=GREEN_E, x_range = [-5,5])))
            
        self.play(Restore(taylorSeries))
        self.play(taylorSeries.animate.scale(0.45).shift(UL * .45 - taylorSeries.get_center() * .45 + taylorSeries.get_critical_point(UL) * .45 + (DOWN * .5) * .45 + LEFT * 1.2))
        #self.play(taylorSeries.animate.shift(UL - taylorSeries.get_center() + taylorSeries.get_critical_point(UL) + DOWN * .5))
        

        errorAxes = Axes(
            x_range=[-4 * PI, 4 * PI, 1],  # x-axis range: (min, max, step)
            y_range=[-3, 3, 1],  # y-axis range: (min, max, step)
            tips=False,
            axis_config={"color": BLACK}  # Configuration for the axes
        )
        
        errorAxes.move_to(DR + UP * .2)

        eX_label = errorAxes.get_x_axis_label("x")
        eY_label = errorAxes.get_y_axis_label("y")

        errorFunc = errorAxes.plot(lambda x: 0, color=RED_D)

        
        errorSeries = Group(errorAxes, errorFunc)

        errorText = Text("Taylor Series Error Function").set_color(BLACK)
        errorText.scale(.5)
        errorText.shift(np.array([3.5, 2.5, 0]))


        self.play(GrowFromCenter(errorSeries), Write(errorText))

        d_n = function(xInput)

        f = 0 * xInput

        for i in range(10):
            f = f + d_n.subs(xInput, 0) / m.factorial(i) * xInput ** i
            d_n = sp.diff(d_n, xInput)

            d_n1 = sp.diff(d_n, xInput)
            solutions = sp.solve(sp.Eq(sp.diff(d_n1, xInput), 0), xInput)
            solutions = [float(sol.evalf()) for sol in solutions if sp.im(sol) == 0]

            solutions.extend([-2 * m.pi, 2 * m.pi])

            print([abs(sp.Lambda(xInput, d_n1)(i)) for i in solutions])

            maxErr = max([(sp.Lambda(xInput, d_n1))(i) for i in solutions])

            errf = maxErr / m.factorial(i+1) * xInput ** (i + 1)

            self.wait(1)

            self.play(Transform(taylorGraph, axes.plot(sp.Lambda(xInput,f), color=GREEN_E, x_range = [-2 * PI, 2 * PI, 1])), \
            Transform(errorFunc, errorAxes.plot(sp.Lambda(xInput,errf), color=RED_D, x_range = [-2 * PI, 2 * PI, 1])))

        #
