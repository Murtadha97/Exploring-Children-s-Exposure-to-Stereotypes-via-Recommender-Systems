## Install CUDA + CudNN correct way on Ubuntu 20.04

1. sudo apt --purge remove "cublas*" "cuda*"

2. sudo apt --purge remove "nvidia*"
3. sudo rm -rf /usr/local/cuda*
4. sudo apt-get autoremove && sudo apt-get autoclean

**reboot**

1. sudo apt-get install g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev

2. wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
3. sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
4. sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
5. sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
6. sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
7. sudo apt-get update
8. sudo apt-get -y install cuda-11.2

**reboot**

1. echo 'export PATH=/usr/local/cuda-11.2/bin:$PATH' >> ~/.bashrc
2. echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

**reboot**

1. tar -xzvf <file>

2. sudo cp -P cuda/include/cudnn.h /usr/local/cuda-11.2/include
3. sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda-11.2/lib64/
4. sudo chmod a+r /usr/local/cuda-11.2/lib64/libcudnn*


For more information check out this video. https://www.youtube.com/watch?v=5eJTzhGe2QE

## Install Anaconda

1. sudo apt update
2. wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
3. bash Anaconda3-2021.11-Linux-x86_64.sh
4. source ~/.bashrc
5. conda config --set auto_activate_base false
6. source ~/.bashrc
