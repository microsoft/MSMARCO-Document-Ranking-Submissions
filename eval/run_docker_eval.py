import argparse
import gzip
import requests
import os
import shutil

from urllib.request import urlretrieve
from tqdm import tqdm

# Helper to download qrels, etc.
from download import download_dev_queries


def full_ranking(args):
    with open(args.output, 'w') as out:
        for entry in tqdm(queries):
            qid = entry[0]
            query = entry[1]
            response = requests.get(f'http://{args.host}:{args.port}/search/', params={'q': query, 'k': args.k})
            hits = response.json()

            rank = 1
            for h in hits['results']:
                out.write(f'{qid}\t{h["docid"]}\t{rank}\n')
                rank = rank + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a run.')
    parser.add_argument('--output', required=True, type=str, help='Output run file.')
    parser.add_argument('--k', required=True, type=int, help='Number of hits.')
    parser.add_argument('--queries', required=True, type=str, help='Query file.')

    parser.add_argument('--host', type=str, default='127.0.0.1', help='Query file.')
    parser.add_argument('--port', type=int, default=8000, help='Query file.')

    parser.add_argument('--full-ranking', action='store_true', help='Full ranking mode.')
    parser.add_argument('--reranking', action='store_true', help='Reranking mode.')

    args = parser.parse_args()

    # Download dev queries
    if not os.path.exists(os.path.join('eval', 'msmarco-docdev-queries.tsv')):
        download_dev_queries()

    print(f'queries: {args.queries}')
    print(f'output: {args.output}')
    print(f'k: {args.k}')
    print(f'host: {args.host}')
    print(f'host: {args.port}')

    queries = []
    with open(args.queries, 'r') as f:
        for line in f:
            qid, query = line.rstrip().split('\t')
            queries.append([qid, query])

    if args.full_ranking:
        print('\nMode: full ranking')
        full_ranking(args)
