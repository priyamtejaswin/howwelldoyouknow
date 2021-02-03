#!/usr/bin/env python
"""
created at: Thu 08 Oct 2020 11:58:04 AM EDT

Template for computing rouge_score for all labels.
"""


import os
import sys
import plac
import subprocess


@plac.pos('prefix_string', "Prefix string.", type=str)
@plac.pos('labels_file', "File containing label enums.", type=str)
@plac.pos('results_dir', "Dir with tgts+hypos.", type=str)
def main(prefix_string, labels_file, results_dir):
    with open(labels_file) as fp:
        labels = sorted(set([l.strip() for l in fp.readlines()])) + ['all']

    check_names = []
    for l in labels:
        check_names.append(prefix_string + l + '.tgt.txt')
        check_names.append(prefix_string + l + '.hypo.txt')

    file_names = set([f for f in os.listdir(results_dir) if f.endswith('.txt')])

    for c in check_names:
        assert c in file_names, "%s is not in %s"%(c, results_dir)
        print("Found %s"%c)

    for i in range(0, len(check_names), 2):
        target = os.path.join(results_dir, check_names[i])
        preds = os.path.join(results_dir, check_names[i+1])
        output = os.path.join(results_dir, 'scores_%s.txt'%labels[i//2])

        cmd = 'python -m rouge_score.rouge \
                --target_filepattern=%s \
                --prediction_filepattern=%s \
                --output_filename=%s \
                --use_stemmer=true'%(target, preds, output)
        print("Running %s"%cmd)
        print(subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8'))

    print('Done', results_dir, labels)


if __name__ == '__main__':
    plac.call(main)
