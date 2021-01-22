# MS MARCO Document Ranking Submissions

This repo holds the official MS MARCO document ranking leaderboard and describes the process for submitting runs.
All associated data for the task (corpus, training data, eval queries, etc.) are held in [this repo](https://github.com/microsoft/MSMARCO-Document-Ranking).

## Submission Instructions

To make a submission, please follow these instructions:

1. Decide on a submission id, which will be a permanent (public) unique key. The submission id should be of the form `yyyymmdd-foo`, where `foo` can be a suffix of your choice, e.g., your group's name.
Please keep the length reasonable.
See [here](https://github.com/microsoft/MSMARCO-Document-Ranking-Archive/tree/main/submissions) for examples.
`yyyymmdd` should correspond to the submission date of your run.

2. In the directory `submissions/`, create the following files:
   1. `submissions/yyyymmdd-foo/dev.txt.bz2` - run file on the dev queries (`msmarco-docdev-queries.tsv`), bz2-compressed
   2. `submissions/yyyymmdd-foo/eval.txt.bz2` - run file on the eval queries (`docleaderboard-queries.tsv`), bz2-compressed
   3. `submissions/yyyymmdd-foo-metadata.json`, in the following format:

       ```
        {
          "team": "team name",
          "model_description": "model description",
          "paper": "url",              // URL to paper
          "code": "url",               // URL to code
          "type": "full ranking"       // either 'full ranking' or 'reranking'
        }
       ```
       Leave the value of `paper` and `code` empty (i.e., the empty string) if not available.
       These fields correspond to what is shown on the leaderboard.

3. Run our evaluation script to make sure everything is in order (and fix any errors):
   ```bash
   $ python eval/run_eval.py --id yyyymmdd-foo
   ```

4. Package (i.e., encrypt) the submission using the following script:
   ```bash
   $ eval/pack.sh yyyymmdd-foo
   ```

5. Open a pull request against this repository.
The subject (title) of the pull request should be "Submission yyyymmdd-foo", where `yyyymmdd-foo` is the submission id you decided on.
This pull request should contain exactly three files:
   1. `submissions/yyyymmdd-foo.key.bin.enc` - the encrypted key
   2. `submissions/yyyymmdd-foo.tar.enc` - the encrypted tarball
   3. `submissions/yyyymmdd-foo-metadata.json.enc` - the encrypted metadata

**IMPORTANT NOTE:**
You might want to save the _unencrypted_ version of the key you've generated, i.e., `submissions/yyyymmdd-foo.key.bin`.
You'll need it if you want to, for example, change your metadata later on.
If you don't keep it, you'll lose it forever, because the `pack.sh` script generates a random key each time, see [here](https://github.com/microsoft/MSMARCO-Document-Ranking-Submissions/blob/main/eval/pack.sh#L6).

## Additional Submission Guidelines
The goal of the MS MARCO leaderboard is to encourage [coopetition](https://en.wikipedia.org/wiki/Coopetition) (cooperation + competition) among various groups working on deep learning and other methods for search that requires or benefits from large-scale training data.
So, while we encourage friendly competition between different participating groups for top positions on the leaderboard, our core motivation is to ensure that over time the leaderboard provides meaningful scientific insights about how different methods compare to each other and answer questions like whether we are making real progress as a research community.
All participants are requested to abide by this spirit of coopetition and strictly observe good scientific principles when participating.
We will follow an honour system and expect participants to ensure that they are acting in compliance with both the policies and the spirit of this leaderboard.
We will also periodically audit all submissions ourselves and may flag issues as appropriate. 

### Frequency of Submission
The eval set is meant to be a blind set.
We want to discourage modeling decisions based eval numbers to avoid overfitting to the set.
To ensure this, we request participants to submit:

1. No more than 2 runs in any given period of 30 days.
2. No more than 1 run with very small changes, such as different random seeds or different hyper-parameters (e.g., small changes in number of layers or number of training epochs).

Participants who may want to run ablation studies on their models are encouraged to do so on the dev set, but not on the eval set.

### Metadata Updates

The metadata you provide during run submission is meant to be permanent.
However, we do allow "reasonable" updates to the metadata as long as it abides by the spirit of the leaderboard (see above).
These reasons might include adding links to a paper or a code repository, fixing typos, clarifying the description of a run, etc.
However, we reserve the right to reject any changes.

To update the metadata of a particular run, you'll need to encrypt a new metadata JSON file _with the same key_ that you used in the original submission.
The command to encrypt the metadata is [here](https://github.com/microsoft/MSMARCO-Document-Ranking-Submissions/blob/main/eval/pack.sh#L11).
Hopefully, you've saved the key?
If you've lost it, get in touch with us and we'll send you the key back via another channel (e.g., email).
Once you've created a new metadata JSON file (i.e., `submissions/yyyymmdd-foo-metadata.json.enc`), send us a pull request with it.
Please make the subject of the pull request something obvious like "Metadata change for yyyymmdd-foo".
Also, please make it clear to us that _you_ have "permission" to change the metadata, e.g., the person making the change request is the same person who performed the original submission. 

### Anonymous Submissions

We allow anonymous submissions.
Note that the purpose of an anonymous submission is to support blind reviewing for corresponding publications, not as a probing mechanism to see how well you do, and then only make your identity known if you do well.

Anonymous submissions should still contain accurate team and model information in the metadata JSON file, but on the leaderboard we will anonymize your entry.
By default, we allow an embargo period of anonymous submissions for up to nine months.
That is, after nine months, your identity will be revealed and the leaderboard will be updated accordingly.
Additional extensions to the embargo period based on exceptional circumstances can be discussed on a case-by-case basis; please get in touch with the organizers.

For an anonymous submission, the metadata JSON file should have an additional field:

```
"embargo_until": "yyyy/mm/dd"
```

Where the date in `yyyy/mm/dd` format cannot be more than nine months past the submission date.
For example, if the submission date is 2020/11/01, the longest possible embargo period is 2021/07/31.
Of course, you are free to specify a shorter embargo period if you wish.

Note that even with an anonymous submission, the submission id is publicly known, as well as the person performing the submission.
You might consider using a random string as the submission id, and you might consider creating a separate GitHub account for the sole purpose of submitting an anonymous run.
Neither is necessary; we only provide this information for your reference.


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at http://go.microsoft.com/fwlink/?LinkID=254653.

Privacy information can be found at https://privacy.microsoft.com/en-us/

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel or otherwise.
