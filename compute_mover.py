#!/usr/bin/env python
"""
created at: Thu 05 Nov 2020 09:58:04 AM EDT

Template for computing Moverscore for all labels.
"""


import os
import sys
import plac
import numpy as np
import torch
from moverscore import get_idf_dict, word_mover_score  # `moverscore_v2` is faster ...
from collections import defaultdict


def read_clean_lines(path):
    with open(path) as fp:
        data = [l.strip() for l in fp.readlines()]
    return data


@plac.pos('prefix_string', "Prefix string.", type=str)
@plac.pos('labels_file', "File containing label enums.", type=str)
@plac.pos('large_hypos', "Large collection train/test of model generated hypos.", type=str)
@plac.pos('large_refs', "Large collection train/test of gold hypos.", type=str)
@plac.pos('results_dir', "Dir with label-separated tgts+hypos.", type=str)
def main(prefix_string, labels_file, large_hypos, large_refs, results_dir):
    """
    1. Generate label enums set from labels_file.
    2. Using labels and prefix, generate file names to check in results_dir.
    3. Check for each file in results_dir.
    4. Read all samples from large_hypos and large_refs and compute idf_dict.
    5. For each pair of label files in results_dir, compute Moverscore 1, 2.
    6. Save as CSV in results_dir.
    7. Finally, compute score for all combined label files.
    """
    hypos = read_clean_lines(large_hypos)
    refs = read_clean_lines(large_refs)
    assert len(hypos) == len(refs)

    idf_dict_hyp = get_idf_dict(hypos)
    idf_dict_ref = get_idf_dict(refs)

    with open(labels_file) as fp:
        labels = sorted(set([l.strip() for l in fp.readlines()]))

    check_names = []
    for l in labels:
        check_names.append(prefix_string + l + '.tgt.txt')
        check_names.append(prefix_string + l + '.hypo.txt')

    file_names = set([f for f in os.listdir(results_dir) if f.endswith('.txt')])

    for c in check_names:
        if c not in file_names:
            raise AssertionError("%s is not in %s"%(c, results_dir))
        print("Found %s"%c)


    all_target, all_preds = [], []
    all_n1, all_n2 = [], []

    for i in range(0, len(check_names), 2):
        target = os.path.join(results_dir, check_names[i])
        preds = os.path.join(results_dir, check_names[i+1])
        output = os.path.join(results_dir, 'mvrs_%s.txt'%labels[i//2])

        lines_target = read_clean_lines(target)
        lines_preds = read_clean_lines(preds)
        assert len(lines_target) == len(lines_preds)

        scores_1 = word_mover_score(lines_target, lines_preds, idf_dict_ref, idf_dict_hyp, \
                                    stop_words=[], n_gram=1, remove_subwords=True, batch_size=16)
        scores_2 = word_mover_score(lines_target, lines_preds, idf_dict_ref, idf_dict_hyp, \
                                    stop_words=[], n_gram=2, remove_subwords=True, batch_size=16)

        avg_1 = np.mean(scores_1)
        avg_2 = np.mean(scores_2)

        all_n1.extend(scores_1)
        all_n2.extend(scores_2)

        with open(output, 'w') as fp:
            fp.write('n1,n2\n')
            fp.write(str(round(avg_1, 4)) + ',' + str(round(avg_2, 4)) + '\n')

        all_target.extend(lines_target)
        all_preds.extend(lines_preds)


    assert len(all_target) == len(all_preds)
    scores_1 = word_mover_score(all_target, all_preds, idf_dict_ref, idf_dict_hyp, \
                                stop_words=[], n_gram=1, remove_subwords=True, batch_size=16)
    scores_2 = word_mover_score(all_target, all_preds, idf_dict_ref, idf_dict_hyp, \
                                stop_words=[], n_gram=2, remove_subwords=True, batch_size=16)

    avg_1 = np.mean(scores_1)
    avg_2 = np.mean(scores_2)

    with open(os.path.join(results_dir, 'mvrs_all.txt'), 'w') as fp:
        fp.write('n1,n2\n')
        fp.write(str(round(avg_1, 4)) + ',' + str(round(avg_2, 4)) + '\n')


    print('Done', results_dir, labels)


if __name__ == '__main__':
    plac.call(main)
