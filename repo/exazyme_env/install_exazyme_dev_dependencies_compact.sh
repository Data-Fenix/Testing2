# Run this script to install the dependencies for the exazyme project
# make sure to run this script from a directory (e.g. home) and make sure that there is no $env_name directory (here set to "exazyme") in the current directory
cd ~
conda deactivate
env_name="exazyme"
rm -rf $env_name
mkdir $env_name
cd $env_name
conda deactivate
conda remove --name $env_name --all -y
conda create -n $env_name python=3.11 -y
conda activate "$env_name"
pip install --upgrade pip
git clone -b main https://github.com/exazyme/JaxRK.git && cd JaxRK && pip install -e ".[ci]" && cd .. 
git clone -b dev git@github.com:exazyme/protein_engineering_data.git && cd protein_engineering_data && pip install -e ".[ci, doc]" && cd .. 
git clone -b dev git@github.com:exazyme/enzyme_efficiency_prediction.git && cd enzyme_efficiency_prediction && pip install -e ".[ci, doc]" && cd ..
