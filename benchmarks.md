#### Performance


|Language|newstest<sup>1</sup>|medline-test2018<sup>2,4</sup>|medline-test2019<sup>2,4</sup>|IWSLT-test<sup>3</sup>|
|--------|--------|----------------|----------------|----------|
|French|41.00|34.32|34.13|41.09|
|German|41.28|25.97|28.10|31.55|
|Spanish|36.63|45.18|43.94|48.79|
|Italian||||42.18
|Korean||||21.33

1: `newstest2019.de-en`, `newstest2014.fr-en`, `newstest2013.es-en` <br>
2: test sets (to English) from the [WMT18](http://www.statmt.org/wmt18/biomedical-translation-task.html) and [WMT19 biomedical translation tasks](http://www.statmt.org/wmt19/biomedical-translation-task.html) <br>
3: [`IWSLT17-test`](https://wit3.fbk.eu/) (for all but Spanish) and [`IWSLT16-test`](https://wit3.fbk.eu/mt.php?release=2016-01-more) (for Spanish) <br>
4: results obtained by using the `<medical>` tag <br>

#### State of the art

|Language|newstest<sup>1</sup>|[medline-test2018<sup>2</sup>](http://www.statmt.org/wmt18/wmt-2018-biomedical-results.pdf)|[medline-test2019<sup>2</sup>](http://www.statmt.org/wmt19/wmt-2019-biomedical-results.pdf)|IWSLT-test<sup>3</sup>|
|--------|--------|----------------|----------------|----------|
|French|40.03 ([NLE UGC](https://arxiv.org/abs/1910.14589))|25.78|35.56|41.70 (NLE UGC)|
|German|40.98 ([FAIR @WMT19, single model](https://github.com/pytorch/fairseq/blob/master/examples/wmt19/README.md))|23.93|28.82|32.01 ([FAIR @WMT19, single model](https://github.com/pytorch/fairseq/blob/master/examples/wmt19/README.md))|
|Spanish||43.41|43.03|

**Disclaimer:** our "medline" BLEU scores are computed against untokenized references with SacreBLEU’s default settings. The Biomedical Task settings might differ. The test sets are also very small (~300 lines), which can cause a large variance in results.

We do not report comparison for Sp-En for newstest, as the models reported are outdated (the best entry achieved 30.4). 
Spanish, Italian and Korean were added later to the IWSLT challenge, and were not part of the competition at that time
