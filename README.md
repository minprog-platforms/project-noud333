# Simulation runner

### The problem
When a simulation is used to study a problem it is generally not sufficient to only look at a single case.
There are usually multiple variables that can be changed to study their effects on the end result.
This usually results in a few hours of changing the code or variables slightly to see the effect on the simulation, 
even longer if the code takes a while to run.
So it would be great to be able to give a program all the initial conditions and let it run in the background.
The output of the different runs will be saved in csv files or other specified in the simulation itself this is 
what this project seeks to accomplish.

###  Draft
![Sketch](doc/proposal_sketch.jfif)

Newly added simulations will have to be done via terminal. The program will have to automate setting up the site for all
added simulations.

#### The main page of the user interface.
The top of the page will have a pulldown menu with the different simulations.
Then for every variable in the code a box is added with a few options, its value, whether or not you want this value to be
a single one or a list and in the case a list is used how the file names are changed with it.

Under the variables 2 buttons will be available. A button to start the simulations and a button bringing you to the output pages.
At the bottom of the page a progress bar will be visible.

#### Output page
The output page will be accessed form the output button on the main page.
The page itself will contain maps for every simulation.

The insides of these maps will depend on the type of output the program gives.
If the simulation returns only data the output will be csv files with the data along with a txt file with the initial conditions.
The names of these files will be changed to show what part they are of a larger set. Details will be ironed out later.

If there is another type of file outputted such as a graph in a png all the files will be outputted into a seperate map for each simulation.

### Prerequisites
#### Data sources
The first thing that is needed is a simulation that works. I already have a basic simulation of a virus. But this will need to be modified to fit the project. The current ideas for necessary changes are things like adding a few stock functions that tell the program
what the changeble variables are. And possibly turning the whole thing into a class.

#### External components
Either bootstrap or Javascript is probably necessary to save input and send it off to the program which will run the simulation.
A python package that looks useful is Flask. It is a package that helps with web frameworks. Which overlaps with the python, web connection I want to make. It is also an easy way to get input from html into python which is what I will use it for.

#### Similar projects
By searching around I have found apps that seem like they do the same thing I want. The problem they all seem to share is that the simulation also needs to be made inside their system. Which is something I want to avoid as I would like to write my own version of the simulations.

The product that I was able to find that closely resembles what I want is this one:
https://www.mathworks.com/help/simulink/ug/configure-and-run-simulations-with-multiple-simulations-ui.html
It however seems to work for only 1 variable at a time instead of as many as I want. It also seems to be stuck in their own framework instead of being able to use Python for it.

20sim also seems to accomplish what I want. It also has the option to change things on the fly. It however has the same problem as mathworks as it is its own simulation platform where you have to build your model instead of loading in a python model.
https://www.20sim.com/webhelp/welcome.php

#### Hardest part
I feel like the hardest part will be the automatic loading of a new simulation. I want this project to be modular 
and not need to much modification to the original code. Another part that will probably be hard will be the communication between the site and the code that runs the simulation.
