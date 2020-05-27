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
cat covid19-nmt/Covid19/checkpoint_best.pt.part* > covid19-nmt/Covid19/checkpoint_best.pt

python interactive.py covid19-nmt/Covid19 --user-dir covid19-nmt/Covid19 --path covid19-nmt/Covid19/checkpoint_best.pt \
-s src -t en --bpe covid19 --buffer-size 1000 --max-tokens 8000 --fp16 \
< INPUT | grep "^D" | cut -f3 > OUTPUT
```

Where _INPUT_ contains the sentences you want to translate (one sentence per line). The translation output will be stored in _OUTPUT_.

Depending on the type of GPU your machine has, you might need to adapt the `--buffer-size`, `--max-tokens` and `--fp16` options. `--fp16` speeds up decoding but needs a Volta GPU to be useful. If your GPU has less than 16 GB of memory, you could run into memory errors, in which case you can try halving the `--buffer-size` and `--max-tokens` values.

You can also decode the keyboard inputs interactively (no _INPUT_ and _OUTPUT_) by using the option `--buffer-size 1`.

## Domain-specific translation
In order to translate in the _medical_ domain, use the option `--medical`

## More information
For more information, checkout the [blog post](https://europe.naverlabs.com/blog/a-machine-translation-model-for-covid-19-research/)

### Data & Model
The model card, with data and architecture & hyperparameter information is [here](modelcard.md)

### Performance
BLEU scores on standard benchmarks (together with reference points) are [here](benchmarks.md)


## Contact
For remarks or questions, please contact covid19nmt@naverlabs.com .

## License
The NTM Model is distributed under the CC BY-NC-SA 4.0 License. See [LICENSE_NMT-Model](LICENSE_NMT-Model.txt) for more information.

The modified fairseq modules are distributed under the MIT License.
