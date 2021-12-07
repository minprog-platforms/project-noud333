from flask import Flask, render_template, request
import json
import argparse
import numpy as np


app = Flask(__name__)

def main(input, config):
    # loading in the data from the config file
    file = open(config)
    global data
    data = json.load(file)
    
    global data_range
    data_range = {}
    for variable in data:
        data_range[variable] = False

    # running the app itself
    app.run(debug=True)

@app.route('/')
def index():
    return render_template("index.html", data=data, data_range = data_range)

# makes changes to single data points possible
@app.route('/', methods=["post"])
def get_values():
    for item in request.form:
        
        # check if request contains
        if item.strip(",") in data or "_" in item:
            item_name = item.strip(",").split("_")[0]

            # checks if value has been changed
            if request.form[item]:
                
                # handles changing values form the range
                if "_" in item:
                    name = item.split("_")[0]
                    pos = item.split("_")[1]
                    data[name][pos] = float(request.form[item])
                
                # handles changing single value
                else:
                    data[item.strip(",")] = request.form[item]
        
        # check for swap between range and single value
        elif "range" in item:
            if data_range[item_name]:
                data_range[item_name] = False
                data[item_name] = data[item_name]["begin"]
            else:
                data_range[item_name] = True
                data[item_name] = {"begin": data[item_name]}
                data[item_name]["end"] = data[item_name]["begin"]
                data[item_name]["stepsize"] = 1
    
        elif item == "filestart":
            file_name = item

        if item == "start":
            json_generator(file_name)

    return render_template("index.html", data=data, data_range = data_range)
        



@app.route('/anothersite')
def page2():
    return render_template("anothersite.html")

def json_generator(file_name):
    new_data = {}
    lists = {}
    for item in data_range:
        if data_range[item]:
            lists[item] = np.arange(start= data[item]["begin"], stop= data[item]["end"], step=data[item]["stepsize"])
        else:
            new_data[item] = data[item]
    json_looper(new_data, lists, 0, file_name)

def json_looper(data, lists, index, file_name):
    if len(lists) > index:
        key_list = list(lists.keys())
        key = key_list[index]
        
        for item in lists[key]:
            new_data = data
            new_data[key] = item
            json_looper(new_data, lists, index + 1, file_name)
    
    else:
        print(data)
        for item in data_range:
            if data_range[item]:
                file_name += item + "_" + str(data[item])

        file_name += ".json"

        with open("json/"+file_name, "w") as outfile:
            json.dump(data, outfile)
        
        code_runner()

def code_runner():
    pass

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
    