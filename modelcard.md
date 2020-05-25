This files summarizes the training data and preprocessing steps

### Training data

We used corpora from public benchmarks and OPUS, as well as medical datasets (such as [TAUS](https://md.taus.net/corona)).
Below the training size for each language:

#### Training size (in million line pairs)

|Language|Total|General|Back-translation|Biomedical|
|--------|-----|-------|----------------|----------|
|All|368.4|351.2|8.0|9.2|
|French|128.8|125.0||3.8|
|Spanish|92.9|90.8||2.1|
|German|87.3|84.8||2.5|
|Italian|45.6|44.9||0.7|
|Korean|13.8|5.7|8.0|0.1|

### Pre-processing

- Whitespace normalization, length-based filtering (min 1 token, max 200) and language ID filtering (with langid.py)
- Shared SentencePiece-BPE model trained on multilingual lower-cased data (6M random lines per language extracted from the parallel corpora. The 6M English lines are extracted from the French-English parallel data)
- 80,000 merge operations (vocabulary size of 96,837 with character coverage of 100%: we do the character filtering "manually" according to their absolute frequency)
- NFKC normalization
- Character frequency threshold of 20 (all characters with frequency < 20 are dropped from the dictionary, i.e., replaced with <unk>)
- SentencePiece segmentation is followed by [inline-casing](../master/Covid19/__init__.py): we lowercase the input, segment it into word-pieces, then put special tokens after each token that specify its original case (<U> for capitalized, <T> for title case, and no tag for lowercase). Word-pieces whose original case is undefined (e.g., "MacDonalds") are split again into wordpieces with defined case ("mac" and "donalds"). 
  

### Model settings

- Transformer Big with 3 decoder layers, and larger encoder (FFN dim = 8182)
- Label smoothing 0.1, dropout 0.1
- Adam with warmup and maximum LR of 0.001
- "Early stopping" based on average valid perplexity
