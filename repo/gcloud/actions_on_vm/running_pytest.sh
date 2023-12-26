# =========================================================================================
## ====  Example usage: running enzyme_efficiency_prediction dev branch tests on a VM ====
conda deactivate
env_name="pe_env_test"
rm -rf $env_name
mkdir $env_name
cd $env_name
conda deactivate
conda remove --name $env_name --all -y
conda create -n $env_name python=3.11 -y
conda activate "$env_name"

pip install --upgrade pip
git clone https://github.com/exazyme/JaxRK.git && cd JaxRK && pip install -e ".[ci]" && cd .. 
git clone -b dev git@github.com:exazyme/protein_engineering_data.git && cd protein_engineering_data && pip install -e ".[ci, doc]" && cd .. 
git clone -b dev git@github.com:exazyme/enzyme_efficiency_prediction.git && cd enzyme_efficiency_prediction && pip install -e ".[ci, doc]"

pytest test
conda deactivate

## ====  Example usage: running protein_engineering_data feature/pre-trained  branch tests on a VM ====

env_name="pedata_test"
rm -rf $env_name
mkdir $env_name
cd $env_name
conda deactivate
conda remove --name $env_name --all -y
conda create -n $env_name python=3.11 -y
conda activate "$env_name"

pip install --upgrade pip
git clone https://github.com/exazyme/JaxRK.git && cd JaxRK && pip install ".[ci]" && cd .. && rm -rf JaxRK
git clone -b dev git@github.com:exazyme/protein_engineering_data.git && cd protein_engineering_data && pip install ".[ci, doc]"

pytest --junit-xml=$TEST_REPORT_XML --html=$TEST_REPORT_HTML --self-contained-html --cov=$SOURCE_DIR --cov-report=html:$TEST_COV --cov-report=xml:$TEST_COV_XML test

conda deactivate