# Dynamic-Backward-Attention-Transformer
This is the official repository of the paper "Enhancing Material Features Using Dynamic Backward Attention on Cross-Resolution Patches".

To install the dependencies, please refer to the conda env file.
```
conda env create -f environment.yml
```

Or, if you prefer using docker, please pull our prepared image:

```
docker pull 123mutouren/cv:1.0.0
```

## Local Material Dataset
Please download the original dataset from https://vision.ist.i.kyoto-u.ac.jp/codeanddata/localmatdb/, into the folder dataset/localmatdb. Then you can zip the folder localmatdb since our dataloader assumes the images are zipped.

## Train DBAT
To train our DBAT, you can use the code below:
```
python train_sota.py --data-root "./dataset" --batch-size 4 --tag dpglt --gpus 1 --num-nodes 1 --epochs 200 --mode 95 --seed 42
```
To test the trained model, you can specify the checkpoint path with the --test option
```
python train_sota.py --data-root "./dataset" --batch-size 4 --tag dpglt --gpus 1 --num-nodes 1 --epochs 200 --mode 95 --seed 42 --test accuracy/epoch\=126-valid_acc_epoch\=0.87.ckpt
```
