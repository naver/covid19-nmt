# Covid19NMT

This is a multi-lingual translation model, with a domain specialization option for biomedical text.
To run translation with this you will need to install [fairseq](https://github.com/pytorch/fairseq), and add a provided script for the preprocessing of the input.

## Installation

```
git clone https://github.com/pytorch/fairseq
cd fairseq
python3 -m venv env
source env/bin/activate
python3 -m pip install --editable .
python3 -m pip install sentencepiece

git clone https://github.com/naver/covid19-nmt.git
cd covid19-nmt
cat model/checkpoint_best.pt.part* > model/checkpoint_best.pt

fairseq-interactive model --user-dir model --path model/checkpoint_best.pt --sentencepiece-model model/spm.model \
-s src -t en --bpe covid19 --buffer-size 1000 --max-tokens 8000 --fp16 \
< INPUT | grep "^D" | cut -f3 > OUTPUT
```

Where _INPUT_ contains the sentences you want to translate (one sentence per line). The translation output will be stored in _OUTPUT_.

Depending on the type of GPU your machine has, you might need to adapt the `--buffer-size`, `--max-tokens` and `--fp16` options. `--fp16` speeds up decoding but needs a Volta GPU to be useful. If your GPU has less than 16 GB of memory, you could run into memory errors, in which case you can try halving the `--buffer-size` and `--max-tokens` values.

You can also decode the keyboard inputs interactively (no _INPUT_ and _OUTPUT_) by using the option `--buffer-size 1`.

#### Notes:
- The source language `src` is not a placeholder, but a literal "src" (this is only to tell Fairseq it should use `dict.src.txt` as source dictionary).
- If you get a pickling error when running this command, this is probably because of a corrupted checkpoint file. In this case, try installing [git-lfs](https://git-lfs.github.com/) and pull again, or try downloading the files manually from [here](model/checkpoint_best.pt.part1?raw=true) and [here](model/checkpoint_best.pt.part2?raw=true) (and then concatenate them).
- The preprocessing steps are done in [`model/__init__.py`](model/__init__.py)

## Domain-specific translation
In order to translate in the _medical_ domain, use the option `--medical`

## More information
For more information, checkout the [blog post](https://europe.naverlabs.com/blog/a-machine-translation-model-for-covid-19-research/) or read the [paper](https://openreview.net/pdf?id=U5luH7UiQw6)

### Data & Model
The model card, with data and architecture & hyperparameter information is [here](modelcard.md)

### Performance
BLEU scores on standard benchmarks (together with reference points) are [here](benchmarks.md)


## Contact
For remarks or questions, please contact covid19nmt@naverlabs.com .
If you use this work, please cite

```
@inproceedings{berard-etal-2020-multilingual,
    title = "A Multilingual Neural Machine Translation Model for Biomedical Data",
    author = "B{\'e}rard, Alexandre  and
      Kim, Zae Myung  and
      Nikoulina, Vassilina  and
      Park, Eunjeong Lucy  and
      Gall{\'e}, Matthias",
    booktitle = "Proceedings of the 1st Workshop on {NLP} for {COVID}-19 (Part 2) at {EMNLP} 2020",
    month = dec,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.nlpcovid19-2.16",
    abstract = "We release a multilingual neural machine translation model, which can be used to translate text in the biomedical domain. The model can translate from 5 languages (French, German, Italian, Korean and Spanish) into English. It is trained with large amounts of generic and biomedical data, using domain tags. Our benchmarks show that it performs near state-of-the-art both on news (generic domain) and biomedical test sets, and that it outperforms the existing publicly released models. We believe that this release will help the large-scale multilingual analysis of the digital content of the COVID-19 crisis and of its effects on society, economy, and healthcare policies. We also release a test set of biomedical text for Korean-English. It consists of 758 sentences from official guidelines and recent papers, all about COVID-19.",
}
```

## License
The NTM Model is distributed under the CC BY-NC-SA 4.0 License. See [LICENSE_NMT-Model](LICENSE_NMT-Model.txt) for more information.

The modified fairseq modules are distributed under the MIT License.

The Korean-English data set is released under different licenses. Please refer to that [README file](test_sets/README.md) for more information.

