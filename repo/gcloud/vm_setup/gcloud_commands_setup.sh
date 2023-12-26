# this script shows one way to setup a VM on gcloud
# it cannot be run as a script, but the commands can be run one by one

# ==== ADAPT THE VARIABLES BELOW ====
USERNAME="<username>"
CLOUDIP="<ip>"
PATHTOSSHKEY="<path_to_ssh_key>" # key to gcloud 
# ==== ADAPT THE VARIABLES ABOVE ====

# the ssh key should be added to the ssh-agent and the cloud

# connect to the cloud
ssh $USERNAME@$CLOUDIP -i $PATHTOSSHKEY
# you should now be connected to your VM

# if the instance has been setup with CUDA, then Cuda should be installed the first time you connect to the VM

# Update package list and upgrade packages (for Debian/Ubuntu systems)
sudo apt-get update && sudo apt-get upgrade -y

# Install Git
sudo apt-get install -y git-all

# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Screen - allows to run a script in the background - useful if you want to disconnect from the VM
sudo apt install screen
# https://www.gnu.org/software/screen/manual/screen.html
# https://linuxize.com/post/how-to-use-linux-screen/

# reinstalling NVIDIA drivers - if it does not work from a cuda image
sudo /opt/deeplearning/install-driver.sh
# check that it is working
nvidia-smi dmon

# porerequisite: create a ssh token, for example using ssh-keygen - add it to github
# to add the key to the ssh-agent
eval "$(ssh-agent)"
ssh-add
# ==== ADAPT BELOW ====
git config --global user.email "<email>"
git config --global user.name "<name>"
# ==== ADAPT ABOVE ====
