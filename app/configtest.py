'''
A program to test input with config files
'''
import argparse
import json


def main(output, input):
    file = open(input)
    data = json.load(file)

    item1 = data["value"]
    item2 = data["value2"]

    print(item1 + item2)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help="input file (conf)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.input)