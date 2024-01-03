
# processing and csv file and uploading a dataset to a huggingface repository
python src/pedata/exazyme_datasets/upload.py --repo Exazyme/test_example_dataset_ha1 --filename local_datasets/datafiles/example_dataset_ha1.csv

# pulling a dataset from huggingface, updating it and upload to/replacing the same repo
python src/pedata/exazyme_datasets/upload.py --repo Exazyme/test_example_dataset_ha1
