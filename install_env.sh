conda create --name temp
conda activate temp
conda config --add channels conda-forge
conda config --add channels pytorch
conda install pytorch==1.5.1 torchvision==0.6.1 cudatoolkit=10.2 -c pytorch 
conda install six scikit-learn stringcase ply slimit astunparse submitit
conda install -c conda-forge tensorboard
pip install transformers=="4.18.0"
pip install cython
pip install sacrebleu=="1.2.11" javalang tree_sitter=="0.20.0" psutil fastBPE sentencepiece pandas matplotlib

cd third_party
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-python.git

# install fairseq
git clone https://github.com/pytorch/fairseq
cd fairseq
git checkout 698e3b91ffa832c286c48035bdff78238b0de8ae
pip install .
cd ..

# install apex
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
cd ../