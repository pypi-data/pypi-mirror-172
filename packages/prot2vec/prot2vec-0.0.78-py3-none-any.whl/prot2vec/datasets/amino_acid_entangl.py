import numpy as np
import tensorflow as tf

AA_DICT = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4,
           'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9,
           'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14,
           'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19,
           '?': 20}
AA_COUNT = len(AA_DICT)
AA_DICT_REV = {AA_DICT[key]: key for key in AA_DICT}


def tokenize(seq):
    digit_seq = np.array(list(map(lambda x: AA_DICT[x], seq)))

    return digit_seq[None, :]


def vect_batch(batch):
    x = np.concatenate(batch, axis=0)
    y = x.copy()

    mask = np.ones(y.shape, dtype='float32') - (y == AA_DICT['?']).astype('float32')

    n_values = x.shape[0] * x.shape[1]

    x = tf.one_hot(x, len(AA_DICT)).numpy()
    x[:, :, AA_DICT['?']] = np.random.rand(n_values).reshape(x.shape[:2])

    dim_1_list = np.tile(np.arange(x.shape[0]), x.shape[1])
    dim_2_list = np.tile(np.arange(x.shape[1])[:, None], x.shape[0]).flatten()
    random_confusers = np.random.randint(0, len(AA_DICT), n_values)
    x[dim_1_list, dim_2_list, random_confusers] = 1.

    return x, y, mask


def line_to_seqtok(seq, seq_len):
    prot_len = len(seq[:-1])

    if prot_len >= seq_len:
        offset = np.random.randint(0, prot_len - seq_len + 1)
        seq = seq[offset:offset + seq_len]
    else:
        gap_size = seq_len - prot_len
        empty_start = np.random.randint(0, gap_size)
        seq = ''.join(['?' * empty_start, seq, '?' * (gap_size - empty_start - 1)])

    seq_in = tokenize(seq)

    return seq_in


def entangl_iter(src_file, seq_len, batch_size):
    batch = []
    while True:
        with open(src_file, "r", encoding="utf-8") as fr:
            fr.readline()
            for line in fr:
                _, _, seq = line[:-1].split('\t')
                seq_in = line_to_seqtok(seq, seq_len)
                if seq_in is None:
                    continue

                batch.append(seq_in)

                if len(batch) >= batch_size:
                    v_batch = vect_batch(batch)
                    yield v_batch
                    del batch[:]


if __name__ == '__main__':
    from pathlib import Path

    ROOT = Path(r'C:\DATA\ML-Data\BioML\datasets\Prot2Vec_dataset_2022-06')

    # ds_it = ds_iter(ROOT / 'uniref90_tax-free_shuffled.tsv', 64, 0.15, 1024)
    # ds_it = entangl_iter(ROOT / 'random' / 'completely_random.tsv', 128, 32)
    ds_it = entangl_iter(ROOT / 'uniref90_tax-free_shuffled.tsv', 128, 1024)

    for i in range(1000000):
        a = next(ds_it)
        print()
