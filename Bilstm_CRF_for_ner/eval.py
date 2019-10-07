import os
from TJl_function import iobes_iob,BIO_F1score
def get_result_file(dg_file,result_file):
    f_write = open(result_file, 'w', encoding='utf-8')
    with open(dg_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n')
        for line in lines:
            if line == '':
                continue
            tokens = line.split('\n')
            features = []
            tags = []
            for token in tokens:
                feature_tag = token.split()
                if len(feature_tag) < 2:
                    print(feature_tag)
                    continue
                features.append(feature_tag[0])
                tags.append(feature_tag[-1])
            samples = []
            i = 0
            while i < len(features):
                sample = []
                if tags[i] == 'O':
                    sample.append(features[i])
                    j = i + 1
                    while j < len(features) and tags[j] == 'O':
                        sample.append(features[j])
                        j += 1
                    samples.append('_'.join(sample) + '/o')

                else:
                    if tags[i][0] != 'B':
                        print(tags[i][0] + ' error start')
                    sample.append(features[i])
                    j = i + 1
                    while j < len(features) and tags[j][0] == 'I' and tags[j][-1] == tags[i][-1]:
                        sample.append(features[j])
                        j += 1
                    samples.append('_'.join(sample) + '/' + tags[i][-1])
                i = j
            f_write.write('  '.join(samples) + '\n')
    f_write.close()
def get_f1score(result_file, target_file):
    result = open(result_file, 'r', encoding='utf-8')
    target = open(target_file, 'r', encoding='utf-8')
    r_lines = result.readlines()
    t_lines = target.readlines()
    total_tags = 0  # target样本的字段数
    correct_tags = 0  # result中抽取出的正确字段数
    total_tab_tags = 0  # result中抽取出的字段数
    for r_line, t_line in zip(r_lines, t_lines):
        r_lis = r_line.split('  ')
        t_lis = t_line.split('  ')
        for r_tag, t_tag in zip(r_lis, t_lis):
            if t_tag[-1] in ['a', 'b', 'c']:
                total_tags += 1
            if r_tag[-1] in ['a', 'b', 'c']:
                total_tab_tags += 1
                if r_tag[-1] == t_tag[-1] and len(r_tag) == len(t_tag):
                    correct_tags += 1
    recall = round(correct_tags / total_tags, 4)
    precise = round(correct_tags / total_tab_tags, 4)
    f1score = round(2 * recall * precise / (recall + precise), 4)
    result.close()
    target.close()
    return f1score

def conlleval(label_predict, dg_file, metric_path,raw_test,result_file):
    """
    :param label_predict:
    :param label_path:
    :param metric_path:
    :return:
    """
    with open(dg_file, "w") as fw:
        line = []
        line_pre=[]
        line_real=[]
        for sent_result in label_predict:
            for char, tag, tag_ in sent_result: #字 真实标签 预测标签
                # tag = '0' if tag == 'O' else tag  为什么把tag转换成‘0’？
                # char = char.encode("utf-8")
                tag_=iobes_iob([tag_])[0]
                line.append("{} {}\n".format(char, tag_)) #字 预测标签
                line_pre.append(tag_)
                line_real.append(tag)
            line.append("\n")
        while line[-1]=='\n':
            line.pop()
        fw.writelines(line)
    if result_file[-4:]=='test':
        result_file+='.txt'
        get_result_file(dg_file, result_file)
        exit()
    else:
        print("BIOf1score: {}".format(BIO_F1score(predict=line_pre,target=line_real)))
        get_result_file(dg_file, result_file)
    result_target_file='tmp.txt'
    get_result_file(raw_test,result_file=result_target_file)
    f1score=get_f1score(result_file=result_file,target_file=result_target_file)
    return f1score
    