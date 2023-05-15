from os import getenv
from dataiku import Dataset
original_ds_name = getenv("ORIGINAL_DATASET")
original_ds = Dataset(original_ds_name)