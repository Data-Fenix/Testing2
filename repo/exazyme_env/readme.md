
# Exaxyme repositories

## Creating a virtual environment 

deactivate any activated conda environment \
`conda deactivate`

Create a new conda environment \
Check and adapt `exazyme_env/initialize_conda_env.sh` \
Especially adapt the value of `env_name`

Then run: \
`<absolute_path>/exazyme_env/initialize_conda_env.sh` \
A new conda environement should have been created 

## Activate the virtual environment
`conda activate <env_name>`

## Installing dependencies in the virtual environment  
Once the conda environment has been activated, you can install the dependencies.
First adapt the `DEVDIR` variable value to match your exasyme developement directory (if you have one already) 

Then run the following script: \
`<absolute_path>exazyme_env/install_exazyme_dependencies.sh`

## Updating dependencies
In case you just want to **update** your already existing repos and environment, this should work as well.\ 
Beware that if the repos have been cloned before (already in your woorking dev), then the script will `pull` and install. If you want to update, maybe it is safer to do things more manually to be safe.