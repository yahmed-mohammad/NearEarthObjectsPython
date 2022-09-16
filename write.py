"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            content = {**result.serialize(), **result.neo.serialize()}
            content['name'] = content['name'] if content['name'] is not None else ''
            content['potentially_hazardous'] = True if content['potentially_hazardous'] else False
            writer.writerow(content)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    json_list = []
    for result in results:
        content = {**result.serialize(), **result.neo.serialize()}
        content['name'] = content['name'] if content['name'] is not None else ''
        content['potentially_hazardous'] = True if content['potentially_hazardous'] else False
        json_list.append(
            {
                'datetime_utc': content['datetime_utc'],
                'distance_au': content['distance_au'],
                'velocity_km_s': content['velocity_km_s'],
                'neo': {
                    'designation': content['designation'],
                    'name': content['name'],
                    'diameter_km': content['diameter_km'],
                    'potentially_hazardous': content['potentially_hazardous'],
                },
            }
        )

    with open(filename, 'w') as output_file:
        json.dump(json_list, output_file, indent="\t")
