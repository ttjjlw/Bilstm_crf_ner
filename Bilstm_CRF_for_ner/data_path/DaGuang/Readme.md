数据格式：
train_file 原始数据集：txt文件  字1\ttag1\n
        #                  字2\ttag2\n
        # line1                    ...
        #                  字n\ttagn\n             需要注意的是每个line 隔一行
        #                       \n
        # line2                 同上
       ...
       最后一行以换行符结束

test_file 可同上带标签，也可不带标签,同train_file

注意在 data程序里添加 tag2label （非标签类的用'O'）

使用预训练词向量：字典 word2id,未登录词用'_'表示，'<PAD>'用0编码，保存的格式是pkl

训练的策略：

当f1score_valid小于最大的f1score_valid,并且f1score_train大于最大的f1socre_train-0.1，说明过拟合

则学习率减半，并且载入最大的f1socre_valid模型重新训练。

训练过程遇到的bug:1、test_data少了一个样本，因为test_data最后一行不是换行符结束

                2、f1socre_train 计算结果错误，因为train_data在训练时发生了shuffle,解决办法：在训练之前

                copy.deep()一份

输入：train_data,test_file='dg_valid.txt'即可训练。前提设置：use_pre_emb=False, mode='train',isload2train=False

载入最新模型重新训练：把 isload2train=True，demo_model=某个你需要模型的时间戳

输出：mode='test',test_file='dg_test.txt',demo_model=某个你需要模型的时间戳

最后得到的文件为txt,字1字2...字n\a 字1字2...字x\o.....

记录：模型参数，每个epoch的f1score_valid,f1score_train。lr的变化等等