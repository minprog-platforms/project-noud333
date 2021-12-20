Review of the code of Noud Hover (12224693)
Reviewed by Tjibbe Valkenburg

# Use less code in the flask pages themselves.
The main part of my code was done within the flask pages themselves it is probably neater to get the logic tree and all the other parts that do not directly affect the look of the page in either seperate functions or seperate files. Currently the loading of the pages and handling off the requests is a bit messy due to that. This might also fix the issues of the site being stuck in loading when the start button is pressed. (though this might have another solution)

# The use of globals
In this project I used multiple globals to keep track of data points and setup for the json generator. This however might collide with code in the inputted files. Although I do know that it is bad practise in general to use globals I could not find an easy way to get to those values in the flask page without loading it in another file. This might be a good option but I have to look into that further.

# HTML
As this project was mostly made to be a tool for me to use I did not pay much attention the looks of the site, and thus only the functionality. In the future it wouldnt be a bad idea to improve the looks. And I do not yet know how intuitive it is for someone who hasnt been working with it for hours.

# Output page
Currently the output page just throws the output straight onto the output page. While this works fine for a small amount of simulations the site will quickly become cluttered when the code is ran a large amount of times. In the future it would be a good idea to further split them up into smaller subfolders.

# Saving of output
After the simulation has ran its course the output can be found in the output page of the flask app. This on its own is great but if the container is closed the results are lost. To use the data in more than 1 way I would like to add in a feature where the output is also saved somewhere locally.
