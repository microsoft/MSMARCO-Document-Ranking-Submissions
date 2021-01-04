import gzip
import os
import shutil

from urllib.request import urlretrieve


def download_dev_qrels():
    print('Dev qrels not found, downloading...')
    dev_qrels_url = 'https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-qrels.tsv.gz'
    dev_qrels_compressed = os.path.join('eval', 'msmarco-docdev-qrels.tsv.gz')
    dev_qrels_uncompressed = os.path.join('eval', 'msmarco-docdev-qrels.tsv')
    urlretrieve(dev_qrels_url, filename=dev_qrels_compressed)

    with gzip.open(dev_qrels_compressed, 'rb') as f_in:
        with open(dev_qrels_uncompressed, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_dev_queries():
    print('Dev queries not found, downloading...')
    dev_qrels_url = 'https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-queries.tsv.gz'
    dev_qrels_compressed = os.path.join('eval', 'msmarco-docdev-queries.tsv.gz')
    dev_qrels_uncompressed = os.path.join('eval', 'msmarco-docdev-queries.tsv')
    urlretrieve(dev_qrels_url, filename=dev_qrels_compressed)

    with gzip.open(dev_qrels_compressed, 'rb') as f_in:
        with open(dev_qrels_uncompressed, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
