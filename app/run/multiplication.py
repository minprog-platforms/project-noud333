'''
A program to test input with config files
'''
import argparse
import json


def main(input, output):
    file = open(input)
    data = json.load(file)

    item1 = data["mult"]
    item2 = data["mult2"]

    result= item1 + item2

    with open(output + ".txt", "w") as outfile:
            outfile.write(str(result))

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help="input file (conf)")
    parser.add_argument("output", help="location of output file")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)