# D:\localE\python
# -*-coding:utf-8-*-
# Author ycx
#1、导入语料库，分词，
import numpy as np
import tensorflow as tf
# import re
# import jieba
import collections
# import codecs
import pickle
import os

vocabulary_size=120000
#1/读取文库，正则过滤，分词，编码  词列表——count——词典——反词典（+词列表）——data_num
def build_corpus(filename,sep=' '):
    '''
    :param filename:
    :param sep:
    :return:
    '''
    f=open(filename,'r',encoding='utf8')
    # # file=f.read().decode('utf-8') 最好一行一行读，否则占用太多内存而且慢
    line=f.readline()
    txt_seg_list=[]
    k=0
    while line :
        if k%500==0:
            print('处理第{}行中...'.format(k))
        line=line.replace('\n','')
        k+=1
        txt_seg_=[word for word in line.split(sep) if len(word)>1]
        txt_seg_list.extend(txt_seg_)

        line=f.readline()

    count=collections.Counter(txt_seg_list).most_common(vocabulary_size-2)#[(词，词频),...]#这个过程30秒左右
    dictionary={}
    i_=1

    print('开始构建词典')
    for word,_ in count:
        if i_%50000==0:
            print('dealwith{}word'.format(i_))
        #构建一个字典，单词长度为1的舍弃


        dictionary[word]=i_
        i_+=1
    print('length: {} VS 字典长度{}:'.format(i_-1,len(dictionary)))
    dictionary_reverse=dict(zip(dictionary.values(),dictionary.keys()))#{1：我，2：他。。。}
    #print(dictionary_reverse)
    count_unk=0
    data=[]
    print('开始编码词列表')
    for word in txt_seg_list:
        if word in dictionary:
            index=dictionary[word]
            data.append(index)
        else:
            index=len(dictionary)+1
            count_unk+=1
            data.append(index)
    dictionary_reverse[len(dictionary)+1]='[<UNK>]'  #{1：‘我们’，2：‘他吗’}
    dictionary['[<UNK>]']=len(dictionary)+1  #不能取名未知，会覆盖原来的，导致长度减一
    count.append(('[<UNK>]',count_unk))
    dictionary['[<PAD>]']=0
    dictionary_reverse[0]='[<PAD>]'
    del txt_seg_list
    return data,dictionary_reverse,count,dictionary



#预处理文本，生成数字编码的语料库，和字典
filename=r'D:\localE\code\Word2Vec\tu_zh.jian.wiki.seg-1.3g.txt'
if not os.path.exists(filename):print('不存在原始的语料库')
data_num,dictionary_reverse,count,dictionary=build_corpus(filename,sep=' ')

#保存字典
if not os.path.exists('data_path//DaGuang'):os.mkdir('data_path//DaGuang')
with open('data_path//DaGuang//dr_d_td_zh.pkl','wb') as f1:
    pickle.dump(dictionary_reverse,f1)
    pickle.dump(dictionary, f1)
    pickle.dump(data_num, f1)


'''def cal_similarity(word,similarity=similarity,top_k=8):
    if word not in dictionary:
        return 'none'
    value_int=dictionary[word]
    value_int=np.array([value_int])

    sim,word_emberdding=sess.run([similarity,valid_embeddings],feed_dict={valid_data:value_int})
    sim_sort=(-sim[0,:]).argsort()   #index从大到小排序，index对应dictionary_reverse字典
    nearest=sim_sort[1:top_k+1]  #前top_k个,不包括自己
    log_str = "Nearest to %s:" % (word)
    for index in nearest:
        close_word_similarity=sim[0,index]
        close_word = dictionary_reverse[index]
        log_str="%s: %s(%s),"%(log_str,close_word,close_word_similarity)
    return log_str'''






