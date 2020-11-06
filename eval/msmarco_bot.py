import argparse
import re
import subprocess
from github import Github


def evaluate_submission(id):
    # 'exit 0' is a trick so that we get the errors also
    # see https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    output = subprocess.check_output(
        f'python eval/run_eval.py --id {id}; exit 0', shell=True, stderr=subprocess.STDOUT).decode('utf-8')

    msg = f'''
Hi there, thanks for your submission!

I've gone ahead and run the evaluation... here are your results:

```
{output}
```
'''
    return msg


def current_branch():
    # https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git
    return subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True, encoding='UTF-8')


def clone_pr(id):
    # https://stackoverflow.com/questions/14947789/github-clone-from-pull-request
    print(f'Attempting to clone PR {id} into branch submission{id}...')
    subprocess.check_output(f'git fetch origin pull/{id}/head', shell=True)
    subprocess.check_output(f'git checkout -b submission{id} FETCH_HEAD', shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MS MARCO bot')
    parser.add_argument('--list-submissions', action='store_true', help='List submissions.')
    parser.add_argument('--evaluate-submission', type=int, metavar='int', help='Evaluate submission id.')
    parser.add_argument('--no-clone', action='store_true', help='Don\'t clone submission (e.g., if already cloned).')
    parser.add_argument('--post-results', action='store_true', help='Post evaluation results on GitHub.')
    parser.add_argument('--secret-token', type=str, metavar='str', help='secret GitHub token.')

    args = parser.parse_args()

    if args.secret_token:
        print('Initializing with secret token...')
        g = Github(args.secret_token)
    else:
        print('Initializing without secret token...')
        g = Github()

    repo = g.get_repo('microsoft/MSMARCO-Document-Ranking-Archive')
    branch = current_branch()
    print(f'Current branch: {branch}')

    if args.list_submissions:
        print('Listing submissions:')
        pulls = repo.get_pulls(state='open', sort='created', base='main')
        for pr in pulls:
            print(f'[{pr.number}] {pr.title}')
    elif args.evaluate_submission:
        print(f'Attempting to evaluation submission {args.evaluate_submission}')
        pr = repo.get_pull(args.evaluate_submission)
        m = re.search('\d\d\d\d\d\d\d\d-[^ ]+', pr.title)
        submission_id = m.group(0)
        print(f'Inferring that submission id is {submission_id}')

        if not args.no_clone:
            clone_pr(args.evaluate_submission)
        msg = evaluate_submission(submission_id)

        print('\n\n')
        print('Here\'s the evaluation message:')
        print('##################')
        print(msg)
        print('##################')

        if args.post_results:
            print('\n\nPosting evaluation results on GitHub...')
            pr = repo.get_pull(args.evaluate_submission)
            pr.create_issue_comment(msg)
            print('Done!')
    else:
        print('You haven\'t asked me to do anything!')
