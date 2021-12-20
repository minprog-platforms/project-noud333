# Assessment file
This project has mostly went as planned. 

One of the things that initially did not work as expected was the input for multiple variables.
In the first version of the project only 1 variable could be changed at the same time. Making it so that any amount of requests can be handled at once was a necessary and good step.

A side effect of the debug mode of the flask app really works well for this project. Where it automatically restarts the page when an error is found (such as not giving the name input directly with the start button). This way the site will also remember all initial values that have been inputted by the user. And as this project is supposed to be something only for the person who hosts the site this should not be an issue.

I also really like the way in which I handled the generation of the json files in the function named "json_looper" as loops over a variable amount of lists. 

### modularity
A major focus of mine in this project is that it should be as modular as possible, as such I made the initial conditions for a simulation to work with my project very small. These are: the input should be a json file and there should be an argument which contains the name of the files. File type should be added within the program.\
The Dockerfile: In the docker file I think the creation of an empty run folder which will be coupled to a local folder is a great addition. The run folder is removed during the build before re-adding an empty one. Due to this the docker container will not have to be remade to run a new simulation (which could be done due to the dockerfile in the github).