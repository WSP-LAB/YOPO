import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

class CustomDataset(torch.utils.data.Dataset):
	def __init__(self, csv_path):
		df = pd.read_csv(csv_path)
		self.inp = df.iloc[:, :-1].values
		self.outp = df.iloc[:,-1].values.reshape(-1,1)
	
	def __len__(self):
		return len(self.inp)

	def __getitem__(self,idx):
		inp = torch.FloatTensor(self.inp[idx])
		outp = torch.FloatTensor(self.outp[idx])
		return inp, outp

