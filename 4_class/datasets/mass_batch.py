import random
import torch
from torch.utils.data import DataLoader,TensorDataset
import numpy as np
import pandas as pd
import os
import glob
import random
from pytorch_lightning import seed_everything
import pytorch_lightning as pl

from torch.utils.data import Dataset, DataLoader
import torch
import pytorch_lightning as pl
import os

class MASSDataset(Dataset):
    def __init__(self, path_list):
        self.path_lists = path_list
        self.len_list = [0]
        self.iter = 0
        len_sum = 0
        self.file_path_list = []
        for i in range(len(self.path_lists)):
            file_path = sorted(os.listdir(self.path_lists[i]))
            len_sum+=len(file_path)
            self.len_list.append(len_sum)
            self.file_path_list.append(file_path)
        # self.path_lists is list of file paths (i.e., aasm path and rk path)
        # self.len_list is list of accumulated lengths of files in each file path, with first value as 0
        # self.file_path_list is list of list of files under each file path in self.path_lists
    
    def __len__(self):
        return self.len_list[-1]
    # returns total length of files = last value in list of accumulated length of files

    def __getitem__(self, idx):
        # import pdb; pdb.set_trace()
        file_path_iter = 0
        if torch.is_tensor(idx):
            idx = idx.tolist()
        if idx < self.len_list[self.iter + 1]:
            idx = idx
        elif idx >= self.len_list[self.iter + 1] and idx < self.len_list[self.iter + 2]:
            idx-=self.len_list[self.iter + 1]
            file_path_iter+=1
        elif idx > self.len_list[self.iter + 2]:
            idx-=self.len_list[self.iter + 2]
            file_path_iter+=1
        eeg_path = os.path.join(self.path_lists[file_path_iter], self.file_path_list[file_path_iter][idx])
        tens = torch.from_numpy(np.genfromtxt(eeg_path, delimiter=","))
        eeg_data = torch.as_tensor(tens)
        print(self.file_path_list[file_path_iter][idx])
        return eeg_data

class MASSBatchDataModule(pl.LightningDataModule):
    def __init__(self, *args, **kwargs):
        self.n_workers = 32
        self.eeg_train = self.eeg_val = self.eeg_test = torch.Tensor([])
        self.ecg_train = self.ecg_val = self.ecg_test = torch.Tensor([])
        self.slp_stg_train = self.slp_stg_val = self.slp_stg_test = torch.Tensor([])

        # In AASM, there are train, val, and test files each for EEG, ECG and Sleep Stages. Similarly for RK
        # Train EEG-ECG-Sleep stages for AASM and RK combined and given as input to train dataloader. Similarly for val and test.
        # import pdb; pdb.set_trace()
        self.train_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/EEG/train','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/EEG/train/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/train','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/train/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Sleep_stages/train/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/Sleep_stages/train/'])
        self.val_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/EEG/val','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/EEG/val/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/val','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/val/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Sleep_stages/val/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/Sleep_stages/val/'])
        self.test_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/EEG/test','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/EEG/test/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/test','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/test/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/test','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/test/'])
        # self.ecg_train_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/train','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/train/'])
        # self.ecg_train_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/train','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/train/'])
        # self.slp_stg_train_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Sleep_stages/train/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/Sleep_stages/train/'])
        print("Train data accessed")
        # import pdb; pdb.set_trace()
        # for idx, tens in enumerate(self.eeg_train_dataset):
        #     self.eeg_train = torch.cat([self.eeg_train, tens], dim=0)
        # # import pdb; pdb.set_trace()
        
        # print("EEG Train put in eeg_train")

        # for idx, tens in enumerate(self.ecg_train_dataset):
        #     self.ecg_train = torch.cat([self.ecg_train, tens], dim=0)
        # print("ECG Train put in ecg_train")
        # # pdb.set_trace()
        # for idx, tens in enumerate(self.slp_stg_train_dataset):
        #     self.slp_stg_train = torch.cat([self.slp_stg_train, tens], dim=0)
        # # pdb.set_trace() 
        # self.train_data = torch.column_stack([self.eeg_train, self.ecg_train, self.slp_stg_train])
        # print("Sleep stage Train put in slp_stg_train and EEG,ECG,Sleep stage train put in train_data")
        
        # self.eeg_val_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/EEG/val','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/EEG/val/'])
        # self.ecg_val_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/val','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/val/'])
        # self.slp_stg_val_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Sleep_stages/val/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/Sleep_stages/val/'])
        # print("Val data accessed")

        # for idx, tens in enumerate(self.eeg_val_dataset):
        #     self.eeg_val = torch.cat([self.eeg_val, tens], dim=0)
        # # import pdb; pdb.set_trace()
        
        # print("EEG Val put in eeg_val")

        # for idx, tens in enumerate(self.ecg_val_dataset):
        #     self.ecg_val = torch.cat([self.ecg_val, tens], dim=0)
        # print("ECG Val put in ecg_val")
        # # pdb.set_trace()
        # for idx, tens in enumerate(self.slp_stg_val_dataset):
        #     self.slp_stg_val = torch.cat([self.slp_stg_val, tens], dim=0)
        # # pdb.set_trace() 
        # self.val_data = torch.column_stack([self.eeg_val, self.ecg_val, self.slp_stg_val])
        # print("Sleep stage Val put in slp_stg_val and EEG,ECG,Sleep stage val put in val_data")
        
        # self.eeg_test_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/EEG/test','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/EEG/test/'])
        # self.ecg_test_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/ECG/test','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/ECG/test/'])
        # self.slp_stg_test_dataset = MASSDataset(['/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Sleep_stages/test/','/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/RK/Sleep_stages/test/'])
        # print("Test data accessed")

        # for idx, tens in enumerate(self.eeg_test_dataset):
        #     self.eeg_test = torch.cat([self.eeg_test, tens], dim=0)
        # # import pdb; pdb.set_trace()
        
        # print("EEG Test put in eeg_test")

        # for idx, tens in enumerate(self.ecg_test_dataset):
        #     self.ecg_test = torch.cat([self.ecg_test, tens], dim=0)
        # print("ECG Test put in ecg_test")
        # # pdb.set_trace()
        # for idx, tens in enumerate(self.slp_stg_test_dataset):
        #     self.slp_stg_test = torch.cat([self.slp_stg_test, tens], dim=0)
        # # pdb.set_trace() 
        # self.test_data = torch.column_stack([self.eeg_test, self.ecg_test, self.slp_stg_test])
        # print("Sleep stage Test put in slp_stg_test and EEG,ECG,Sleep stage test put in test_data")

    def setup(self, stage = None):
        pass
    
    def train_dataloader(self):
        return DataLoader(self.train_dataset,num_workers=self.n_workers, pin_memory=True)
    def val_dataloader(self):
        return DataLoader(self.val_dataset,num_workers=self.n_workers, pin_memory=True)
    def test_dataloader(self):
        return DataLoader(self.test_dataset,num_workers=self.n_workers, pin_memory=True)


# mass_dataset = MASSDataset('/media/Sentinel_2/Dataset/Vaibhav/MASS/PT_FILES/Batchwise_Data/4_class/AASM/Biosig_files')
# train_loader = DataLoader(mass_dataset)

# for idx, tensor in enumerate(train_loader):
#     eeg_sample = tensor
#     print("mean is", eeg_sample.mean())
    @staticmethod
    def add_dataset_specific_args(parent_parser):
        from argparse import ArgumentParser

        # DATALOADER specific
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        # dataset_group = parser.add_argument_group("dataset")
        dataloader_group = parser.add_argument_group("dataloader")
        dataloader_group.add_argument("--batch_size", default=256, type=int)
        dataloader_group.add_argument("--n_workers", default=32, type=int)

        return parser

if __name__ == "__main__":
    seed_everything(0, workers=True)
    torch.manual_seed(0)
    np.random.seed(0)
    random.seed(0)
    mdm = MASSBatchDataModule()