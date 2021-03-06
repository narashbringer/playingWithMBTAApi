import requests
from requests.exceptions import HTTPError
from helper import get_route_long_names_and_ids, get_stops_and_counts, \
    find_route_from_a_to_b_ineficient
import argparse

if __name__ == "__main__":
    # add args parser to deal with different requests from cli
    parser = argparse.ArgumentParser()

    parser.add_argument('--list_subway', dest='subways',
                        action='store_true', help='list all subways',
                        default=False)
    parser.add_argument('--list_stops', dest='stops',
                        action='store_true', help='list stops with multiple lines and the line with the most data',
                        default=False)
    parser.add_argument('--find_route', dest='find_route',
                        action='store_true', help='list path from stop a to b',
                        default=False)
    parser.add_argument('--start', dest='start',
                        type=str, help='the stop you want to start at')
    parser.add_argument('--end', dest='end',
                        type=str, help='the stop you want to end at')

    args = parser.parse_args()  
    # get all the subway lines
    routes = get_route_long_names_and_ids()
    # use flag to tell us what api we need to call
    if args.subways:
        # print subway lines
        for route in routes:
            print(route['long_name'])
    if args.stops:
        # get the counts an the trains for each stop
        routes, stops_to_lines = get_stops_and_counts(routes)
        # print out the longest and shortest lines
        print(f"Line with the most stops:{routes[-1]['long_name']}, with number stops:{routes[-1]['count']}")
        print(f"Line with the least stops:{routes[0]['long_name']}, with number stops:{routes[0]['count']}")
        print("-----")
        # print out the stops with more then one line stoping there.
        print("stops with more then one subway")
        for stop in stops_to_lines.keys():
            if len(stops_to_lines[stop]) > 1:
                print(f"{stop} has: {stops_to_lines[stop]}, stop there")

    if args.find_route:
        # get the trains for each stop
        _, stops_to_lines = get_stops_and_counts(routes)
        # find route or error from point a to b
        trains, stop =find_route_from_a_to_b_ineficient(stops_to_lines, args.start, args.end)
        # check what we got back from are serch an print accoingly.
        if stop is not None and trains is not None:
            print(f"To get from {args.start} to {args.end} take {trains[0]} to {trains[1]} transfering at {stop}")
        elif trains is not None:
            print(f"To get from {args.start} to {args.end} take {trains[0]}")
