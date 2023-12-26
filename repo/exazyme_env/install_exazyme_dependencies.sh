# this would work to install from scratch or update a folder that already exists
# IMPORTANT - if updating existing folders - the git directories should be clean (no uncommitted changes) before running this script 
pwd
cd ~
pwd
DEVDIR=exazyme
mkdir -p $DEVDIR
cd $DEVDIR
ROOT_DIR=$(pwd)

# ===== install jaxrk ======
if [ ! -d "JaxRK" ]; then
    # If it doesn't exist, clone the repository
    git clone "git@github.com:exazyme/JaxRK.git"
else
    # If it does exist, navigate to the repository directory and pull the latest changes
    cd "JaxRK"
    git checkout main
    git pull
    cd ..
fi
pip install -e "./JaxRK[ci]"  

# ===== install pedata ======
if [ ! -d "protein_engineering_data" ]; then
    # If it doesn't exist, clone the repository
    git clone "git@github.com:exazyme/protein_engineering_data.git"
else
    # If it does exist, navigate to the repository directory and pull the latest changes
    cd "protein_engineering_data"
    git checkout dev
    git pull
    cd ..
fi
pip install -e "./protein_engineering_data[ci, doc]"  

# ===== install eep ======
if [ ! -d "enzyme_efficiency_prediction" ]; then
    # If it doesn't exist, clone the repository
    git clone "git@github.com:exazyme/enzyme_efficiency_prediction.git"
else
    # If it does exist, navigate to the repository directory and pull the latest changes
    cd "enzyme_efficiency_prediction"
    git checkout dev
    git pull
    cd ..
fi
pip install -e "./enzyme_efficiency_prediction[ci, doc]"