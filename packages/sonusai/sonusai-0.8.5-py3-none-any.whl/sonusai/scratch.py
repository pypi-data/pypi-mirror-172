from os.path import join

import h5py
import numpy as np


def main():
    path = '/opt/Aaware/sonusai/scratch/test_mapped_snr_f'
    names = ['000', '001', '002']

    features = []
    for name in names:
        filename = join(path, name + '.h5')
        with h5py.File(filename, 'r') as f:
            features.append(np.array(f['feature']))

    for idx, feature in enumerate(features):
        print(f'{idx} = {feature.shape}')

    feature = np.vstack([features[i] for i in range(len(features))])
    print(f'composite = {feature.shape}')


if __name__ == '__main__':
    main()
