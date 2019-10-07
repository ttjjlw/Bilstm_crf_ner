# Bilstm_crf_ner
2019 DaGuan 信息抽取比赛 <br>
我使用的环境是 tensorflow 1.10.0  python3 <br>

`tricks:把bio格式转变为bioes格式，输入进行训练，然后输出时又转变成bio格式（已封装在脚本内，无需你单独处理）`

# 使用步骤 <br>
使用非常简单，具体过程如下： <br>
1、把数据集放入指定文件夹（Bilstm_CRF_for_ner\data_path下面） <br>
`dg_train_t_8.txt 训练集  train_v_8.txt 验证集 如果不用预训练的word embedings,则其他都可以删掉。` <br>
2、进入Bilstm_CRF_for_ner\main.py脚本，设置超参数，然后运行即可 <br>

# 模型训练时输出结果解释：
```
===========validation / test===========
Precision: 0.8474
recall: 0.8371
BIOf1score: 0.8422
I error start
I error start
I error start
I error start
I error start
...
[]
epochs: 1 验证集f1score: 0.7315
以上是验证集结果

Precision: 0.8854
recall: 0.8746
BIOf1score: 0.88
I error start
I error start
I error start
I error start
...
[]
epochs: 1 训练集f1score: 0.7792
以上是训练集的测试结果
```
# 模型训练策略解释： <br>
> 当f1score_valid小于最大的f1score_valid,并且f1score_train大于最大的f1socre_train-0.1，说明过拟合

则学习率减半，并且载入最大的f1socre_valid模型重新训练。

