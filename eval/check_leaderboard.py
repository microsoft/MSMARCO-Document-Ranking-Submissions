import argparse
import csv
import json


def main(args):
    id = args.id

    leaderboard = {}

    with open('leaderboard/leaderboard.csv') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            leaderboard[row['id']] = row

    metadata_file = f'submissions/{id}-metadata.json'

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    assert id == leaderboard[id]['id'], 'ids do not match!'
    assert leaderboard[id]['date'] == metadata['date'], 'date does not match!'

    team = metadata['team'].replace('"', '\\"')
    assert leaderboard[id]['team'] == team, 'team does not match!'

    model_description = metadata['model_description'].replace('"', '\\"')
    assert leaderboard[id]['description'] == model_description, 'model_description does not match!'

    assert leaderboard[id]['paper'] == metadata['paper'], 'paper does not match!'
    assert leaderboard[id]['code'] == metadata['code'], 'code does not match!'
    assert leaderboard[id]['type'] == metadata['type'], 'type does not match!'

    print(f'Metadata data of {id} matches information in leaderboard/leaderboard.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks metadata of run against leaderboard.csv')
    parser.add_argument('--id', type=str, metavar='str', required=True, help='submission id')

    main(parser.parse_args())
