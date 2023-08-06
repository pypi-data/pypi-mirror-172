import argparse
import json

import ofdskit.lib.geojson


def main():
    parser = argparse.ArgumentParser(description="OFDSKit")
    subparsers = parser.add_subparsers(dest="subparser_name")

    json_to_geojson_parser = subparsers.add_parser("jsontogeojson")
    json_to_geojson_parser.add_argument("inputfilename")
    json_to_geojson_parser.add_argument("outputnodesfilename")
    json_to_geojson_parser.add_argument("outputspansfilename")

    args = parser.parse_args()

    if args.subparser_name == "jsontogeojson":

        with open(args.inputfilename) as fp:
            input_data = json.load(fp)

        converter = ofdskit.lib.geojson.JSONToGeoJSONConverter()
        converter.process_package(input_data)

        with open(args.outputnodesfilename, "w") as fp:
            json.dump(converter.get_nodes_geojson(), fp, indent=4)

        with open(args.outputspansfilename, "w") as fp:
            json.dump(converter.get_spans_geojson(), fp, indent=4)


if __name__ == "__main__":
    main()
