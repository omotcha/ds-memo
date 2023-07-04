# ds-memo
memo dapp + semantic search

---
### WIP..

client dev using python sdk


### Dependencies
1. Transformers, Sentence Transformers

    `pip install transformers`

    `pip install sentence-transformers`

2. Faiss

    `conda install -c pytorch faiss-cpu`

    or

    `conda install -c pytorch faiss-gpu`

3. chainmaker python sdk

    `pip3 install git+https://git.chainmaker.org.cn/chainmaker/sdk-python.git`

### About deployment

This is a demo deployed on Chainmaker, key steps will be described in {project dir}/docs/deploy.md (WIP).

### About transformer models

It seems that in-script hf model downloading has been restricted recently, please download the files manually and place them into {project dir}/models/{model name}

- please also edit the value of **embedding_model_name** in {project dir}/configs/common.py, which to be same with {model name}

- my preference: [simcse](https://arxiv.org/abs/2104.08821)

