'''
Concrete IO class for a specific dataset
'''

# Copyright (c) 2017-Current Jiawei Zhang <jiawei@ifmlab.org>
# License: TBD

import pickle

import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader

from code.base_class.dataset import dataset


# https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
# This is much more efficient to use for CNN
class CustomDataset(Dataset):
    def __init__(self, image, labels, data):
        self.labels = labels
        self.images = image
        self.data = data
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        return self.images[idx], self.labels[idx]

class Dataset_Loader(dataset):
    data = None
    dataset_source_folder_path = None
    dataset_source_file_name = None

    def __init__(self, dName=None, dDescription=None):
        super().__init__(dName, dDescription)

    def load(self):
        print('loading data...')
        f = open(self.dataset_source_folder_path + self.dataset_source_file_name, "rb")
        self.data = pickle.load(f)

        train_X = []
        train_y = []
        test_X = []
        test_y = []

        if self.dataset_source_file_name == 'MNIST':
            self.mean = [0.4914]
            self.std = [0.2470]
        elif self.dataset_source_file_name == 'ORL':
            self.mean = [0.4914, 0.4822, 0.4465]
            self.std = [0.2470, 0.2435, 0.2616]
        elif self.dataset_source_file_name == 'CIFAR':
            self.mean = [0.4914, 0.4822, 0.4465]
            self.std = [0.2470, 0.2435, 0.2616]

        # Normalize images
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(self.mean, self.std)])
        for line in self.data['test']:
            test_X.append(transform(line['image']))
            test_y.append(line['label'])

        for line in self.data['train']:
            train_X.append(transform(line['image']))
            train_y.append(line['label'])

        traindata = CustomDataset(train_X, train_y, self.data)
        testdata = CustomDataset(test_X, test_y, self.data)

        traindata = DataLoader(traindata, batch_size=10, shuffle=True, num_workers=0)
        testdata = DataLoader(testdata, batch_size=len(train_y), shuffle=False, num_workers=0)

        f.close()
        return {'test': testdata, 'train': traindata}