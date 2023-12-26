# this script can be run as a script and should
# - setup a VM on gcloud
# - setup a cuda environment, install dependencies 
# - run pytest on eep / dev branch

echo "--------------------------"   
echo "Setting up the VM"

# ==== ADAPT THE VARIABLES BELOW ====
USERNAME="<username>"
CLOUDIP="<ip>"
PATHTOSSHKEY="<path_to_ssh_key>" # key to gcloud 
# ==== ADAPT THE VARIABLES ABOVE ====

ssh $USERNAME@$CLOUDIP -i $PATHTOSSHKEY <<'ENDSSH'
    sudo apt-get update && sudo apt-get upgrade -y

    # Install Git
    sudo apt-get install -y git-all

    # Download and install Miniconda
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash Miniconda3-latest-Linux-x86_64.sh

    # Screen
    sudo apt install screen

    # reinstalling NVIDIA drivers - if it does not work from a cuda image
    sudo /opt/deeplearning/install-driver.sh
    
    # check that it is working
    # nvidia-smi dmon

ENDSSH


echo "--------------------------"
echo "Setting up github connection"

ssh $USERNAME@$CLOUDIP -i $PATHTOSSHKEY <<'ENDSSH'

    # porerequisite: create a ssh token, for example using ssh-keygen - add it to github
    # to add the key to the ssh-agent
    eval "$(ssh-agent)"
    ssh-add

    # ==== ADAPT BELOW ====
    git config --global user.email "<email>"
    git config --global user.name "<name>"
    # ==== ADAPT ABOVE ====

ENDSSH

echo "--------------------------"   
echo "Action in the VM"

ssh $USERNAME@$CLOUDIP -i $PATHTOSSHKEY <<'ENDSSH'

    rm -rf test_eep
    mkdir test_eep
    cd test_eep
    env_name="pe_env"
    conda create -n $env_name python=3.11 -y
    conda activate "$env_name"

    python -m pip install --upgrade pip
    git clone https://github.com/exazyme/JaxRK.git && cd JaxRK && pip install ".[ci]" && cd .. && rm -rf JaxRK
    git clone -b dev --single-branch git@github.com:exazyme/protein_engineering_data.git && cd protein_engineering_data && pip install ".[ci]" && cd .. && rm -rf protein_engineering_data
    git clone -b dev --single-branch git@github.com:exazyme/enzyme_efficiency_prediction.git && cd enzyme_efficiency_prediction && pip install ".[ci, doc]"

    pytest test

ENDSSH

