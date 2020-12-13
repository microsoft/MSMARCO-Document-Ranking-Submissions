import argparse
import gzip
import requests
import os
import shutil

from urllib.request import urlretrieve

from tqdm import tqdm

query_file = 'eval/msmarco-docdev-queries.tsv'

parser = argparse.ArgumentParser(description='Generates a run.')
parser.add_argument('--output', required=True, type=str, help='Output run file.')
parser.add_argument('--k', required=True, type=int, help='Number of hits.')

args = parser.parse_args()

# Evaluate dev run
if not os.path.exists(os.path.join('eval', 'msmarco-docdev-queries.tsv')):
    print('Dev queries not found, downloading...')
    dev_qrels_url = 'https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-queries.tsv.gz'
    dev_qrels_compressed = os.path.join('eval', 'msmarco-docdev-queries.tsv.gz')
    dev_qrels_uncompressed = os.path.join('eval', 'msmarco-docdev-queries.tsv')
    urlretrieve(dev_qrels_url, filename=dev_qrels_compressed)

    with gzip.open(dev_qrels_compressed, 'rb') as f_in:
        with open(dev_qrels_uncompressed, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

queries = []
with open(query_file, 'r') as f:
    for line in f:
        qid, query = line.rstrip().split('\t')
        queries.append([qid, query])

with open(args.output, 'w') as out:
    for entry in tqdm(queries):
        qid = entry[0]
        query = entry[1]
        response = requests.get('http://127.0.0.1:8000/search/', params={'q': query, 'k': args.k})
        hits = response.json()

        rank = 1
        for h in hits['results']:
            out.write(f'{qid}\t{h["docid"]}\t{rank}\n')
            rank = rank + 1
