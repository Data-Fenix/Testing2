if [ -n "$CONDA_DEFAULT_ENV" ]; then
    conda deactivate
else
    echo "No conda environment is currently activated."
fi

env_name="exazyme"
conda create -n $env_name python=3.11 -y
conda activate "$env_name"
