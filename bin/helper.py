import typing
import requests


def get_route_long_names_and_ids() -> typing.List[typing.Dict]:
    """gets the all of the routes and there ids"""
    # use filter and type 0,1 so we only get back that
    # data that is needed and reduce processing on the client side.
    route_dict = []
    url = 'https://api-v3.mbta.com/routes?type=0,1'
    try:
        response = requests.get(url)
        routes = response.json()
        for route in routes['data']:
            route_dict.append({
                "id":route['id'], 
                "long_name":route['attributes']['long_name']
            })
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return route_dict

def get_stops_and_counts(routes: typing.List[typing.Dict]):
    """
    gets the list of the stops and what trains stop there along with number of stops per line.
    """
    routes_clone = routes.copy()
    stops_to_lines = {}
    for i, route_id in enumerate(routes):
        url = f"https://api-v3.mbta.com/stops?include=route&filter%5Broute%5D={route_id['id']}"
        count = 0
        try:
            response = requests.get(url)
            stops = response.json()
            for x in stops['data']:
                count += 1
                stop_name = x['attributes']['name']
                if stop_name in stops_to_lines.keys():
                    stops_to_lines[stop_name] = stops_to_lines[stop_name]+[route_id['long_name']]
                else:
                    stops_to_lines[stop_name] = [route_id['long_name']]

                routes_clone[i] = {**route_id , "count": count}
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    routes = sorted(routes_clone, key = lambda i: i["count"])
    return routes, stops_to_lines

def find_route_from_a_to_b_ineficient(stops_to_lines, start, end):
    """lazy serch for path from stop a to stop b O(n^3)."""
    trains_to_take = []
    if start and end:
        start_tains = stops_to_lines[start]
        end_trains = stops_to_lines[end]
        trains_to_take = list(set(start_tains) & set(end_trains))
        if len(trains_to_take) == 0:
            for traina in start_tains:
                for trainb in end_trains:
                    for stops in stops_to_lines.keys():
                        lines = stops_to_lines[stops]
                        if traina in lines and trainb in lines:
                            trains_to_take.append(traina)
                            trains_to_take.append(trainb)
                            return trains_to_take, stops
            print(f"Error no with one train transfer or less from {stat} to {stop}.")
            return None, None
        return trains_to_take , None
    elif start:
        print("please add a end stop")
    elif end:
        print("please add a start stop")
