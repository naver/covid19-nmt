"""
This file includes modifications to fairseq distributed through GitHub at https://github.com/pytorch/fairseq/blob/master/fairseq/data/encoders/sentencepiece_bpe.py under this license https://github.com/pytorch/fairseq/blob/master/LICENSE.

Copyright with respect to the modifications: Copyright 2020 Naver Corporation

ORIGINAL COPYRIGHT NOTICE AND PERMISSION NOTICE:

Copyright (c) Facebook, Inc. and its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from fairseq import file_utils, utils
from fairseq.data.encoders import register_bpe
import unicodedata
import regex
import os


lower, title, upper, other = range(4)
case_symbols = [None, '<T>', '<U>', None]


class Covid19BPE(object):

    @staticmethod
    def add_args(parser):
        # fmt: off
        # stays here for back-compatibility with older version of fairseq
        parser.add_argument('--sentencepiece-model', type=str,
                            help='path to sentencepiece model')
        parser.add_argument('--medical', action='store_true',
                            help='automatically add the <medical> tag to translate text in the biomedical domain')
        # fmt: on

    def __init__(self, args):
        vocab = file_utils.cached_path(args.sentencepiece_model)
        try:
            import sentencepiece as spm
            self.sp = spm.SentencePieceProcessor()
            self.sp.Load(vocab)
        except ImportError:
            raise ImportError('Please install sentencepiece with: pip install sentencepiece')

        self.mixed_case_regex = regex.compile('(▁?[[:upper:]]?[^[:upper:]\s▁]+|▁?[[:upper:]]+|▁)')
        self.tags = ['<medical>']  # protect these tags at the beginning of sentences
        self.medical = args.medical

    def is_beginning_of_word(self, x: str) -> bool:
        if x in ['<unk>', '<s>', '</s>', '<pad>']:
            # special elements are always considered beginnings
            # HACK: this logic is already present in fairseq/tasks/masked_lm.py
            # but these special tokens are also contained in the sentencepiece
            # vocabulary which causes duplicate special tokens. This hack makes
            # sure that they are all taken into account.
            return True
        return x.startswith('▁')

    @staticmethod
    def clean(line):
        return regex.sub(r'\s+', ' ', line).strip()

    def get_case(self, s):
        if s.istitle():
            return title
        if s.isupper():
            return upper
        elif s.islower() or s.lower() == s:
            return lower
        else:
            return other

    def _encode(self, x: str) -> str:
        pieces = []
        for piece in self.sp.EncodeAsPieces(x):
            if self.sp.IsUnknown(self.sp.PieceToId(piece)):
                pieces += list(piece)
            else:
                pieces.append(piece)
        return ' '.join(pieces)

    def encode(self, x: str, **kwargs) -> str:
        tag = None
        for tag_ in self.tags:
            if x.startswith(tag_):
                tag = tag_
                x = x.replace(tag, '', 1)
                break
        if tag is None and self.medical:
            tag = self.tags[0]

        orig = self.clean(unicodedata.normalize('NFKC', x))
        orig_lower = ' '.join(y if len(x) == len(y) else x for x, y in ((w, w.lower()) for w in orig.split()))
        # only lowercase words whose length is not modified by lowercasing
        line = self.clean(self._encode(orig_lower))

        output = []
        j = 0
        for wordpiece in line.split():
            if wordpiece == '▁':
                output.append(wordpiece)
                continue

            prefix = ''
            try:
                if wordpiece.startswith('▁'):
                    prefix = '▁'
                    wordpiece = wordpiece[1:]
                i = orig_lower.find(wordpiece, j)
            except:
                output.append(prefix + wordpiece)
                continue

            j = i + len(wordpiece)
            cased = orig[i:j]

            case = self.get_case(cased)
            if len(cased) == len(wordpiece) and case == other:
                cased_split = self.mixed_case_regex.findall(cased)
                k = 0
                for n, s in enumerate(cased_split):
                    case = self.get_case(s)
                    output += [(prefix if n == 0 else '') + wordpiece[k:k + len(s)], case_symbols[case]]
                    k += len(s)
            else:
                output += [prefix + wordpiece, case_symbols[case]]

        output.insert(0, tag)
        return ' '.join(w for w in output if w is not None)

    def decode(self, x: str, **kwargs) -> str:
        tokens = x.split()
        for i, w in enumerate(tokens):
            if w == case_symbols[title]:
                tokens[i - 1] = tokens[i - 1].title()
            elif w == case_symbols[upper]:
                tokens[i - 1] = tokens[i - 1].upper()

        x = ' '.join(w for w in tokens if w not in case_symbols)
        return x.replace(' ', '').replace('▁', ' ').strip()


try:
    from dataclasses import dataclass, field
    from fairseq.dataclass import FairseqDataclass

    @dataclass
    class Covid19BPEConfig(FairseqDataclass):
        sentencepiece_model: str = field(
            default="???", metadata={"help": "path to sentencepiece model"}
        )
        medical: bool = field(
            default=False, metadata={"help": "automatically add the <medical> tag to translate text in the biomedical domain"}
        )
    Covid19BPE = register_bpe('covid19', dataclass=Covid19BPEConfig)(Covid19BPE)
except:
    # support for older versions of fairseq
    Covid19BPE = register_bpe('covid19')(Covid19BPE)
