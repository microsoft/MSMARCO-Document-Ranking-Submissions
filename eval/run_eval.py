import argparse
import bz2
import gzip
import json
import re
import os
import shutil
import subprocess

from urllib.request import urlretrieve


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


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def main(args):
    id = args.id
    base_dir = os.path.join('.', 'submissions', id)

    print(f'# Processing submission {id}\n')

    output = subprocess.check_output(f'eval/unpack.sh {id}', shell=True).decode('utf-8')
    print(output)

    print(f'Submission directory {base_dir}')

    assert os.path.exists(base_dir), f'Error: {base_dir} does not exist!'

    print('Verified: submission directory exists!')

    dev_run = os.path.join(base_dir, 'dev.txt.bz2')
    test_run = os.path.join(base_dir, 'eval.txt.bz2')
    metadata_file = base_dir + '-metadata.json'

    for f in [dev_run, test_run, metadata_file]:
        assert os.path.exists(f), f'Error: {f} does not exist!'

    print('Verified: expected files appear in the submission directory!\n')

    # Uncompress the dev run and the test run
    for filepath in [dev_run, test_run]:
        newfilepath = filepath[:-4]
        print(f'Decompressing {filepath} to {newfilepath}')
        with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
            for data in iter(lambda: file.read(100 * 1024), b''):
                new_file.write(data)
        print(f'Number of lines in {newfilepath}: ' + str(file_len(newfilepath)))

    print('\nProceeding to evaluate: \n')

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

    dev_run_uncompressed = dev_run[:-4]  # Strip the .bz2 suffix
    dev_run_mrr = evaluate_run_with_qrels(dev_run_uncompressed, 'msmarco-docdev-qrels.tsv')

    print(f'Dev run MRR@100: {dev_run_mrr}')

    # Evaluate test run

    if os.path.exists('eval/docleaderboard-qrels.tsv'):
        test_run_uncompressed = test_run[:-4]  # Strip the .bz2 suffix
        test_run_mrr = evaluate_run_with_qrels(test_run_uncompressed, 'docleaderboard-qrels.tsv', exclude=True)
        print(f'Eval run MRR@100: {test_run_mrr}')
    else:
        print('Test qrels not available, skipping evaluation.')

    # Piece together entry in leaderboard.csv
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    if args.generate_csv:
        leaderboard_entry = [id,
                             metadata['date'],
                             '',  # this is where the emojis go
                             '"' + metadata['model_description'].replace('"', '\\"') + '"',
                             '"' + metadata['team'].replace('"', '\\"') + '"',
                             metadata['paper'],
                             metadata['code'],
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
