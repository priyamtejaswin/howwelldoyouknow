Code and data for "How well do you know your summarization datasets?", submitted to ACL 2021.
---

This repository contains the code and data used in the paper titled "How well do you know your summarization datsets?" submitted to [ACL 2021](https://2021.aclweb.org/calls/papers/). From the abstract:
> ... In this study, we manually analyse 600 samples from three popular summarization datasets. Our study is driven by a six-class typology which captures different noise types (missing facts, entities) and degrees of summarization difficulty (extractive, abstractive). We follow with a thorough analysis of 27 state-of-the-art summarization models and 5 popular metrics, and report our key insights ...

We include the following classes in the typology:
1. Incomplete/Ireelevant: `_incomplete`
2. Entity Missing: `_entity`
3. Evidence Missing: `_evidence`
4. Extractive: `_extractive`
5. Paraphrase: `_paraphrase`
6. Inference: `_inference`

# Notes on general organization.
For each dataset, the *raw* input data is stored in 2 forms:
1. **Indices**: Each line in this file corresponds to the line/sample number of the test dataset.
2. **Labels**: Each line in this file is the annotated typology label assigned to the test sample.

With these files, and the test source/reference data, we can extract the samples and perform any custom analysis. Model outputs can be found in the respective dirs of the datasets:
* **Gigaword**: `./giga-org-test-shuf-1to300`
* **CNN/DM**: `./cnndm-300`
* **XSum**: `./xsum-200`

Every directory in the dataset directory is a different model, that contains the source, target and model outputs. Consider the files in [BiSET](https://www.aclweb.org/anthology/P19-1207/) dir for Gigaword:
```bash
giga-org-test-shuf-1to300/biset$ find ./
./
./_all.src.txt
./_all.tgt.txt
./_all.hypo.txt
./_entity.src.txt
./_entity.tgt.txt
./_entity.hypo.txt
./_evidence.src.txt
./_evidence.tgt.txt
./_evidence.hypo.txt
...
```
* `_all` contains all test samples in order of the Indices file.
* `_<label>.src.txt` contains the source text.
* `_<label>.tgt.txt` contains the target text.
* `_<label>.hypo.txt` contains the model output text.
* `<label>` values can be `[all, incomplete, entity, evidence, extractive, paraphrase, inference]`


# Raw data
### Gigaword
* **Indices**: `./giga-org-test-shuf-1to300/test_indices_top200.txt`
* **Labels**: `./giga-org-test-shuf-1to300/labels_final.txt`
* **Source/Targets/Hypos:** `./giga-org-test-shuf-1to300/<model_dir>/`
* **Models:** `[pegasus, coverage, pgcov, prophet, unilm-v2, biset, control-copying]`

### CNN/DM
* **Indices**: `./cnndm-300/cnndm_indices.txt`
* **Labels**: `./cnndm-300/labels_final.txt`
* **Source/Targets/Hypos:** `./cnndm-300/<model_dir>/`
* **Models:** `[pnbert, bart-ext, bart-abs, unilm, ext_heter_graph, ext_matchsumm, ext_refresh, abs_two_stage_rl, abs_neusumm, abs_bottom_up, abs_semsim, abs_unilm, ext_bart, ext_banditsumm, abs_bart]`

### XSum
* **Indices**: `./xsum-200/xsum_indices.txt`
* **Labels**: `./xsum-200/labels.txt`
* **Source/Targets/Hypos:** `./xsum-200/aligned/<model_dir>/`
* **Models:** `[tconvs2s, presumm_ext_abs, presumm_abs, pgnv, presumm_trans, lead, ext_oracle, bart, convs2s]`

# Metrics
