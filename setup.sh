# create Conda environment
conda create --name torch python==3.9
conda activate torch
# install requirements
pip install -r requirements.txt
# install Git LFS
sudo apt-get install git-lfs -y
# export training variables
export LOCAL_RANK="0,1,2,3,4,5,6,7"
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python