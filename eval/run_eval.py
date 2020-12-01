import argparse
import bz2
import gzip
import json
import re
import os
import shutil
import subprocess

from urllib.request import urlretrieve


def autoopen(filename, mode="rt"):
    """
    A drop-in for open() that applies automatic compression for .gz and .bz2 file extensions
    """
    if not 't' in mode and not 'b' in mode:
       mode=mode+'t'
    if filename.endswith(".gz"):
        import gzip
        return gzip.open(filename, mode)
    elif filename.endswith(".bz2"):
        import bz2
        return bz2.open(filename, mode)
    return open(filename, mode)


def evaluate_run_with_qrels(run, qrels, exclude=False):
    if exclude:
        output = subprocess.check_output(
            f'python eval/ms_marco_eval.py {run} eval/{qrels} exclude/', shell=True).decode('utf-8')
    else:
        output = subprocess.check_output(
            f'python eval/ms_marco_eval.py {run} eval/{qrels}', shell=True).decode('utf-8')

    # print(f'\n\n{output}\n\n')
    m = re.compile('MRR @100: ([0-9.]+)').search(output)
    return m.group(1)


def sanity_check_run(file):
    print(f'Sanity checking run {file}')
    qids = set()
    with bz2.open(file, 'rt') as f:
        for i, l in enumerate(f):
            qids.add(l.split('\t')[0])
    line_cnt = i + 1
    num_queries = len(qids)
    print(f'Run has {line_cnt} lines, {num_queries} unique queries.')
    if line_cnt != num_queries * 100:
        print(f'Warning, {num_queries * 100} lines expected (100 hits per query), instead {line_cnt} lines found!')
    print('')


def main(args):
    id = args.id
    base_dir = os.path.join('.', 'submissions', id)

    print(f'# Processing submission {id}\n')

    if os.path.exists('msmarco_doc_private_key.pem'):
        print('Private key found!')
        output = subprocess.check_output(f'eval/unpack.sh {id}', shell=True).decode('utf-8')
        print(output)
    else:
        print('Private key not found, assuming unencrypted files exists...\n')

    print(f'Submission directory {base_dir}')

    assert os.path.exists(base_dir), f'Error: {base_dir} does not exist!'

    print('Verified: submission directory exists!')

    dev_run = os.path.join(base_dir, 'dev.txt.bz2')
    test_run = os.path.join(base_dir, 'eval.txt.bz2')
    metadata_file = base_dir + '-metadata.json'

    for f in [dev_run, test_run, metadata_file]:
        assert os.path.exists(f), f'Error: {f} does not exist!'

    print('Verified: expected files appear in the submission directory!\n')

    sanity_check_run(dev_run)
    sanity_check_run(test_run)

    print('Proceeding to evaluate:\n')

    # Evaluate dev run
    if not os.path.exists(os.path.join('eval', 'msmarco-docdev-qrels.tsv')):
        print('Dev qrels not found, downloading...')
        dev_qrels_url = 'https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-qrels.tsv.gz'
        dev_qrels_compressed = os.path.join('eval', 'msmarco-docdev-qrels.tsv.gz')
        dev_qrels_uncompressed = os.path.join('eval', 'msmarco-docdev-qrels.tsv')
        urlretrieve(dev_qrels_url, filename=dev_qrels_compressed)

        with gzip.open(dev_qrels_compressed, 'rb') as f_in:
            with open(dev_qrels_uncompressed, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    dev_run_mrr = evaluate_run_with_qrels(dev_run, 'msmarco-docdev-qrels.tsv')

    print(f'Dev run MRR@100: {dev_run_mrr}')

    # Evaluate test run

    if os.path.exists('eval/docleaderboard-qrels.tsv'):
        test_run_mrr = evaluate_run_with_qrels(test_run, 'docleaderboard-qrels.tsv', exclude=True)
        print(f'Eval run MRR@100: {test_run_mrr}')
    else:
        print('Test qrels not available, skipping evaluation.')

    # Piece together entry in leaderboard.csv
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    if args.generate_csv:
        match = re.search(r'(\d\d\d\d)(\d\d)(\d\d)-', id)
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)

        if 'embargo_until' in metadata.keys():
            model_description = '"Anonymous"'
            team = '"Anonymous"'
            paper = ''
            code = ''
        else:
            model_description = '"' + metadata['model_description'].replace('"', '\\"') + '"'
            team = '"' + metadata['team'].replace('"', '\\"') + '"'
            paper = metadata['paper']
            code = metadata['code']

        leaderboard_entry = [id,
                             f'{year}/{month}/{day}',
                             '',  # this is where the emojis go
                             model_description,
                             team,
                             paper,
                             code,
                             metadata['type'],
                             str(round(float(dev_run_mrr), 3)),
                             str(round(float(test_run_mrr), 3)),
                             ''            # This is the tweetid field, leaving empty for now
                             ]

        print('\n\n############')
        print(','.join(leaderboard_entry))
        print('############')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automated run script for leaderboard')
    parser.add_argument('--id', type=str, metavar='str', required=True, help='submission id.')
    parser.add_argument('--generate-csv', action='store_true', help='Generate the leaderboard csv entry.')

    main(parser.parse_args())
