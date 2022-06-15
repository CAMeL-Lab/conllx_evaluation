# Camel-depeval

Compare two CoNLL-X files or directories, to obtain the tokenization F-score and POS tag accuracy, as well as the LAS, UAS, and label scores.<br><br>
Since comparison usually occurs between gold and parsed files, the two files/directories will be differentiated using `gold` and `parsed` keywords. In other words, you do not need to have gold and parsed files to compare; any two will do.<br><br>

Note: the evaluator is also CoNLL-U compatible.

## Methodology
<ol>
<li>Two files or directories are passed to the evaluator. If two directories are passed, the directories must have matching file names.</li>
<li>The files are read, and the trees every two files are compared.</li>
<li>Align trees using ced_word_alignment
<ul><li>involves inserting null alignment tokens</li></ul>
</li>
<li>The evaluation scores are then calulated
<ul><li>tokenization f-score is calculated on all aligned tokens, while the remaining metrics are calulated after removing insertions (null alignment tokens added to the gold tree)</li></ul>
</li>
</ol>




## Assumptions
Since ced_word_alignment is used, the second and third assumptions are the same.
- No words are added to either the parsed or gold files.
- No changes to the word order.
- Text is in the same script and encoding.

---

## Contents

- `align_trees.py` aligns trees using the ced_word_alignment algorithm
- `class_conllx` used to read CoNLL-X files
- `classes` dataclasses used throughout the code
- `conllx_counts` gets different statistics after comparing 2 CoNLL-X files
- `conllx_scores` calculates scores given counts
- `evaluate_conllx_driver` main script
- `handle_args` simplifies use of the argparse library
- `requirements.txt` necessary dependencies needed to run the scripts.
- ced_word_alignment/ the ced alignment library
- `README.md` this document.

## Requirements

- Python 3.8 and above.

To use, you need to first install the necessary dependencies by running the following command:

```bash
pip install -r requirements.txt
```

---

## Usage

```text
usage: evaluate_conllx_driver.py [-h] [-g] [-p] [-gd] [-pd]

This script takes 2 CoNLL-X files or 2 directories of CoNLL-X files and evaluates the scores.

required arguments:
  -g , --gold          the gold CoNLL-X file
  -p , --parsed        the parsed CoNLL-X file

or:
  -gd , --gold_dir     the gold directory containing CoNLL-X files
  -pd , --parsed_dir   the parsed directory containing CoNLL-X files
```

---

## Examples

The sentences used are taken from CamelTB_1001_introduction_1.conllx and CamelTB_1001_night_1_1.conllx (data can be obtained from <a href="https://treebank.camel-lab.com/">The Camel Treebank</a>.

### Sample 1:
The toknization is the same, and so the F_score is 100%, and the insertion/deletion counts are both 0. <br>
```text
python evaluate_conllx_driver.py -g samples/sample_1_gold.conllx -p samples/sample_1_parsed.conllx
```
|||
|- |- |
| tokenization_f_score |      100.0 |
| tokenization_precision |    100.0 |
| tokenization_recall |       100.0 |
| pos |                        81.6 |
| uas |                        55.3 |
| label |                      65.8 |
| las |                        44.7 |
| insertion_count |    0 |
| deletion_count |     0 |


### Sample 2:

```text
python evaluate_conllx_driver.py -g samples/sample_2_gold.conllx -p samples/sample_2_parsed.conllx
```
|||
|- |- |
| tokenization_f_score |      90. |400000
| tokenization_precision |    90. |384615
| tokenization_recall |       90. |384615
| pos |                       86. |500000
| uas |                       65. |400000
| label |                     75. |000000
| las |                       57. |700000
| insertion_count |    2 |
| deletion_count |     2 |


---


## License

conllx_evaluator is available under the MIT license.
See the [LICENSE file](/LICENSE) for more info.