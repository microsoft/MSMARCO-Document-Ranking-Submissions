# MS MARCO Document Ranking Leaderboard Archive

This is a work-in-progress attempt to revamp the MS MARCO Document Ranking Leaderboard.
We will "switch over" to this repo at some future point, but until then, [the main MS MARCO site](https://microsoft.github.io/msmarco/) remains the "ground truth".

## Submission Instructions

To make a submission, please follow these instructions:

1. Decide on a submission id, which will be a permanent unique key. The submission id should be of the form `YYYYMMDD-foo`, where `foo` can be a suffix of your choice, e.g., your group's name.
Please keep the length reasonable.
See [here](https://github.com/microsoft/MSMARCO-Document-Ranking-Archive/tree/main/submissions) for examples.
`YYYYMMDD` should correspond to the submission date of your run.

2. Create the directory `submissions/YYYYMMDD-foo/`. This directory should contain three files:
   1. `submissions/YYYYMMDD-foo/dev.txt.bz2` - run file on the dev queries, bz2-compressed
   2. `submissions/YYYYMMDD-foo/eval.txt.bz2` - run file on the eval queries, bz2-compressed
   3. `submissions/YYYYMMDD-foo-metadata.json`, in the following format:

       ```
        {
          "team": "team name",
          "model_description": "model description",
          "date": "yyyyy/mm/dd",       // submission date
          "paper": "url",              // URL to paper
          "code": "url",               // URL to code
          "type": "full ranking"       // either 'full ranking' or 'reranking'
        }
       ```

3. Package (i.e., encrypt) the submission using the following script:
   ```bash
   $ eval/pack.sh YYYYMMDD-foo
   ```

4. Open a pull request against this repository.
The subject (title) of the pull request should be "Submission YYYYMMDD-foo", where `YYYYMMDD-foo` is the submission id you decided on.
This pull request should contain exactly two files:
   1. `submissions/YYYYMMDD-foo.key.bin.enc` - the encrypted key
   2. `submissions/YYYYMMDD-foo.tar.enc` - the encrypted tarball
   3. `submissions/YYYYMMDD-foo-metadata.json.enc` - the encrypted metadata

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
