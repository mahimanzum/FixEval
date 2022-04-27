conda create --name codenet
conda activate temp
conda config --add channels conda-forge
conda config --add channels pytorch
conda install pytorch==1.5.1 torchvision==0.6.1 cudatoolkit=10.2 -c pytorch 
conda install six scikit-learn stringcase ply slimit astunparse submitit
conda transformers=="4.18.0"
pip install cython
pip install sacrebleu=="1.2.11" javalang tree_sitter=="tree_sitter==0.2.1" psutil fastBPE sentencepiece pandas matplotlib
