## ====  Example usage: training a deep learning model on a VM ====
# in my case I want to clone a specific branch of a repo - I do not want to clone the whole repo
# And I wnat to run a script on the VM which is going to train a deep learning model.

# clone the branch from the github repo your are interested in
git clone -b jean/data_wrangling --single-branch git@github.com:exazyme/protein_engineering_data.git

# create a conda environment
conda create -n myenv python=3.10
conda activate myenv

# install requirements
pip install -r requirements.txt # or equivalent, depending on the requirements file

# if you need to login to huggingface - for example to download a model
huggingface-cli login
git config --global credential.helper store

# run trainer.py --> the thing you want to run on the WM
python trainer.py

