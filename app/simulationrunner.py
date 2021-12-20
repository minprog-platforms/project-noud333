from flask import Flask, render_template, request, send_from_directory
import json
import argparse
import numpy as np
import os


app = Flask(__name__)


def main(input, config):
    # loading in the data from the config file
    file = open("run/"+config)
    global data
    data = json.load(file)

    # checking if values are static or ranges
    global data_range
    data_range = {}
    for variable in data:
        data_range[variable] = False

    # use the name of the program to be run and configure it correctly
    assert input[-3:] == ".py", "Please input a python file"
    input = input[:-3]
    global program
    program = input

    # running the app itself
    app.run(debug=True, host="0.0.0.0")


# Load the main page initially
@app.route('/')
def index():
    return render_template("index.html", data=data, data_range=data_range)


# Create and load the site for the output
@app.route('/output')
def page2():
    output_list = os.listdir("output")
    return render_template("anothersite.html", files=output_list)


# Send requested output file to user
@app.route('/output/<path:file>')
def download_file(file):
    return send_from_directory(directory="output", path="/anothersite/{}".format(file), filename=file)


# Handle changes to the files that need to be ran.
@app.route('/', methods=["post"])
def get_values():
    for item in request.form:

        # check if request contains , or ___ which signify variables
        if item.strip(",") in data or "___" in item:
            item_name = item.strip(",").split("___")[0]

            # checks if value has been changed
            if request.form[item]:

                # handles changing values from the range
                if "___" in item:
                    name = item.split("___")[0]
                    pos = item.split("___")[1]
                    data[name][pos] = float(request.form[item])

                # handles changing single value
                else:
                    data[item.strip(",")] = request.form[item]

        # check for swap between range and single value
        elif "range" in item:

            # change range to single value
            if data_range[item_name]:
                data_range[item_name] = False
                data[item_name] = data[item_name]["begin"]

            # change single value to range
            else:
                data_range[item_name] = True
                data[item_name] = {"begin": data[item_name]}
                data[item_name]["end"] = data[item_name]["begin"]
                data[item_name]["stepsize"] = 1

        # filestart signifies the name the output files will start with
        elif item == "filestart":
            if request.form[item]:
                file_name = request.form[item]

        # when start button is pressed start running the code
        if item == "start":
            json_generator(file_name)

    # show the main page after requests have been handled
    return render_template("index.html", data=data, data_range=data_range)


def json_generator(file_name):
    """
    this function creates new json files based on the current data array
    """
    new_data = {}
    lists = {}

    # make a range for every datapoint that needs one otherwise add it to the final json
    for item in data_range:
        if data_range[item]:
            lists[item] = np.arange(start=data[item]["begin"], stop=data[item]["end"], step=data[item]["stepsize"])
        else:
            new_data[item] = data[item]

    # create new json files
    json_looper(new_data, lists, 0, file_name)

    # run the simulation for every json file
    code_runner()


def json_looper(data, lists, index, file_name):
    """recusively go by every instance and make a json file for every set of initial values"""
    # check if every combination from the lists have been added to the json files
    if len(lists) > index:
        key_list = list(lists.keys())
        key = key_list[index]

        for item in lists[key]:
            new_data = data
            new_data[key] = item
            json_looper(new_data, lists, index + 1, file_name)

    # make the json file
    else:
        for item in data_range:
            if data_range[item]:
                file_name += item + "_" + str(data[item])

        file_name.replace(".", ",")
        file_name += ".json"

        with open("json/"+file_name, "w") as outfile:
            json.dump(data, outfile)


def code_runner():
    """run the python program given in command line"""

    # import the python code into this program
    exec("import {} as function".format("run." + program), globals())

    # run every set of initial values
    for file in os.listdir("json"):
        # run the simulation for every json file
        function.main("json/" + str(file), "output/" + str(file[:-5]))


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help="python file of simulation")
    parser.add_argument("config", help="config file of simulation")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.config)
