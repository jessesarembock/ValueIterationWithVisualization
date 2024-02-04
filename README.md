# Value Iteration Visualization Project

**Overview**

This project implements Value Iteration on a grid-based environment, using a Bellman Equation, to find the optimal policy for package delivery. The results of each iteration, as well as the optimal route, are visualized on an animated heatmap.
<br>
<br>

**Features**

> ● Value Iteration Algorithm Implementation: the program uses a Bellman Equation implementation of Value Iteration.
>
> ● Animated Heatmap Visualization: the animated map of the grid is helpful for understanding how Value Iteration works.
>
> ● Customizable Parameters: users can customize every aspect of the environment.
<br>

**Python Scripts**

> ● ValueIteration.py: responsible for Environment Setup, Value Iteration over the environment, and Policy Extraction.
>
> ● Animate.py: responsible for creating the visualization of the Value Iteration Process and the Optimal Route.
>
<br>

**Prerequisites**

> ● Python 3.x
>
> ● Required Python packages: 'numpy', 'matplotlib', 'animatplot'.


**Setup** **and** **Running** **the** **Application**

> 1\. Clone the repository or download the project to your local
> machine.
>
> 2\. Open the project in your terminal.
>
> 3\. Type 'make' to create a Python Virtual Environment, making sure you are in the root directory of the project. To then activate the virtual environment, type 'source venv/bin/activate'.
>
> 4\. To run the application, make sure
> you are still in the root directory of the project, then type \"make
> run\" to run the application with default environmental parameters. If you
> want to run the application with customized parameters, it is simpler to not use the run target of the Makefile and rather type 'python src/ValueIteration.py \<width\> \<height\> [-start \<x\> \<y\>] [-end \<x\> \<y\>] [-k \<number of landmines\>] [-gamma \<value of gamma\>]'. However, you may also run the program using the Makefile's run target by typing 'make run' followed by some customized parameters. For example: make run width=16 height=21 k='-k 36' gamma='-gamma 0.5' start='-start 5 7' end='-end 14 12'.
<br>

**Usage**

> Once you have run the application, allow some seconds for the animation to render, especially on the first run. Then watch how the values of the gridpoints change with each iteration. You can pause and play the animation, as well as toggle with the 'time' bar. The final frame shows the optimal route from the start point to the end point.

**Contributions**

Contributions are welcome. Please adhere to the project\'s coding
standards and submit pull requests for any proposed changes.
<br>
<br>

**License**

This project is licensed under the MIT License - see the
[LICENSE](https://chat.openai.com/c/LICENSE) ﬁle for details.
