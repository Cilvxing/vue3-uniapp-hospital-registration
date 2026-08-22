"""
特征工程
"""
import numpy as np
import pandas as pd
import joblib
import string
import jieba.posseg as pseg
import jieba
import json
import os


def label2idx(data):
    """
    构建label 与索引的映射字典
    :param data: 数据
    :return:返回label与索引的映射字典
    """
    # 如果存在label2id.json文件
    if os.path.exists('./data/label2id.json'):
        # json.load()函数将JSON数据解码成python字典对象
        labelToIndex = json.load(open('./data/label2id.json',
                                      encoding='utf-8'))
    # 如果不存在label2id.json文件
    else:
        # 统计label的独特值
        label = data['label'].unique()
        # 构建label与索引的映射字典
        labelToIndex = dict(zip(label, list(range(len(label)))))
        # 将映射字典写入到label2id.json文件中
        with open('./data/label2id.json', 'w', encoding='utf-8') as f:
            # json.dump()函数将python对象编码成JSON字符串并写入到文件中
            json.dump({k: v for k, v in labelToIndex.items()}, f)
    # 返回label与索引的映射字典
    return labelToIndex


def get_tfidf(tfidf, data):
    """
    得到文档的tf-idf编码
    :param tfidf: tfidf编码
    :param data: 数据
    :return:
    """
    print(data['text'])
    # 统计停用词
    stopWords = [x.strip() for x in open('./data/stopwords.txt', encoding='utf-8').readlines()]
    # 去除文本中的停用词与空白字符
    text = data['text'].apply(lambda x: " ".join([w for w in x.split() if w not in stopWords and w != '']))
    print(text)
    # 将文档转化成矩阵
    data_tfidf = pd.DataFrame(
        tfidf.transform(
            text.tolist()).toarray())
    # 列索引
    data_tfidf.columns = ['tfidf' + str(i) for i in range(data_tfidf.shape[1])]
    # 将原始数据与转换后的tf-idf矩阵拼接
    data = pd.concat([data, data_tfidf], axis=1)

    return data


def array2df(data, col):
    """
    从ndarray到DataFrame
    :param data: 数据
    :param col: 列索引
    :return:
    """
    return pd.DataFrame.from_records(
        data[col].values,
        columns=[col + "_" + str(i) for i in range(len(data[col].iloc[0]))])


def get_embedding_feature(data, embedding_model):
    '''
    word2vec -> max/mean, word2vec n-gram(2, 3, 4) -> max/mean, label embedding->max/mean
    data:输入数据
    embedding_model:模型
    '''
    # 构建label与索引的映射字典
    labelToIndex = label2idx(data)
    # 标签使用word2vec编码
    w2v_label_embedding = np.array([
        # 列求平均
        np.mean([
            # 单位标准化的向量表示每个字
            embedding_model.get_vector(word) for word in key
            if word in embedding_model.key_to_index.keys()
        ], axis=0) for key in labelToIndex
    ])
    # 将标签的word2vec编码保存至w2v_label_embedding.pkl文件中
    joblib.dump(w2v_label_embedding, './data/w2v_label_embedding.pkl')
    # 根据未聚合的embedding 数据， 获取各类embedding 特征
    print("transform w2v")
    #     data['w2v'] = data["text"].apply(
    #         lambda x: wam(x, embedding_model, aggregate=False))  # [seq_len * 300]
    # 获取embedding特征，并进行聚合
    tmp = data['text'].apply(lambda x: pd.Series(
        generate_feature(x, embedding_model, w2v_label_embedding)))
    # 拼接
    tmp = pd.concat([array2df(tmp, col) for col in tmp.columns], axis=1)
    data = pd.concat([data, tmp], axis=1)
    return data


def wam(sentence, w2v_model, method='mean', aggregate=True):
    '''
    @description: 通过word average model 生成句向量
    sentence: 以空格分割的句子
    w2v_model: word2vec模型
    method： 聚合方法 mean 或者max
    aggregate: 是否进行聚合
    @return:
    '''
    # 获取每一句话中每一个单词的映射
    arr = np.array([
        w2v_model.get_vector(s) for s in sentence
        if s in w2v_model.key_to_index.keys()
    ])
    # 如果不进行聚合，则直接返回
    if not aggregate:
        return arr
    # 如何进行聚合，则根据method进行操作
    if len(arr) > 0:
        # 第一种方法对一条样本中的词求平均
        if method == 'mean':
            return np.mean(np.array(arr), axis=0)
        # 第二种方法返回一条样本中的最大值
        elif method == 'max':
            return np.max(np.array(arr), axis=0)
        else:
            raise NotImplementedError
    else:
        return np.zeros(300)


def rename_column(data, suffix):
    data.columns += suffix
    return data


def generate_feature(sentence, embedding_model, label_embedding):
    '''
    获取embedding特征，并进行聚合
    data， input data, DataFrame
    label_embedding, all label embedding
    model_name, w2v means word2vec
    @return: data, DataFrame
    '''
    # 首先在预训练的词向量中获取标签的词向量句子,每一行表示一个标签表示，每一行表示一个标签的embedding
    # 计算label embedding

    # 获取embedding 特征 不进行聚合
    w2v = wam(sentence, embedding_model, aggregate=False)  # [seq_len * 300]
    # 如果embedding 特征为0，则初始化为0矩阵
    if len(w2v) < 1:
        return {
            'w2v_label_mean': np.zeros(300),
            'w2v_label_max': np.zeros(300),
            'w2v_mean': np.zeros(300),
            'w2v_max': np.zeros(300),
            'w2v_2_mean': np.zeros(300),
            'w2v_3_mean': np.zeros(300),
            'w2v_4_mean': np.zeros(300),
            'w2v_2_max': np.zeros(300),
            'w2v_3_max': np.zeros(300),
            'w2v_4_max': np.zeros(300)
        }

    # 如果大于0，则进行如下标签初始化
    w2v_label_mean = Find_Label_embedding(w2v, label_embedding, method='mean')
    w2v_label_max = Find_Label_embedding(w2v, label_embedding, method='max')

    # 将embedding 进行max, mean聚合
    w2v_mean = np.mean(np.array(w2v), axis=0)

    w2v_max = np.max(np.array(w2v), axis=0)

    # 滑窗处理embedding 然后聚合
    w2v_2_mean = Find_embedding_with_windows(w2v, 2, method='mean')

    w2v_3_mean = Find_embedding_with_windows(w2v, 3, method='mean')

    w2v_4_mean = Find_embedding_with_windows(w2v, 4, method='mean')

    w2v_2_max = Find_embedding_with_windows(w2v, 2, method='max')

    w2v_3_max = Find_embedding_with_windows(w2v, 3, method='max')

    w2v_4_max = Find_embedding_with_windows(w2v, 4, method='max')

    # 返回处理好的编码
    return {
        'w2v_label_mean': w2v_label_mean,
        'w2v_label_max': w2v_label_max,
        'w2v_mean': w2v_mean,
        'w2v_max': w2v_max,
        'w2v_2_mean': w2v_2_mean,
        'w2v_3_mean': w2v_3_mean,
        'w2v_4_mean': w2v_4_mean,
        'w2v_2_max': w2v_2_max,
        'w2v_3_max': w2v_3_max,
        'w2v_4_max': w2v_4_max
    }


def softmax(x):
    '''
    calculate softmax
    x, ndarray of embedding
    @return: softmax result
    '''
    return np.exp(x) / np.exp(x).sum(axis=0)


def Find_Label_embedding(example_matrix, label_embedding, method='mean'):
    '''
    根据论文《Joint embedding of words and labels》获取标签空间的词嵌入
    实际上就是通过计算单词与标签的相似度，赋予每个单词不同权重
    example_matrix(np.array 2D): denotes words embedding of input
    label_embedding(np.array 2D): denotes the embedding of all label
    @return: (np.array 1D) the embedding by join label and word
    '''

    # 根据矩阵乘法来计算label与word之间的相似度
    # # (seq_len,300)*(300,11) = (seq_len,11)
    similarity_matrix = np.dot(example_matrix, label_embedding.T) / (
            np.linalg.norm(example_matrix) * (np.linalg.norm(label_embedding)))

    # 然后对相似矩阵进行均值池化，则得到了“类别-词语”的注意力机制
    # 这里可以使用max-pooling和mean-pooling
    attention = similarity_matrix.max(axis=1)
    # (seq_len,1)
    attention = softmax(attention).reshape(-1, 1)
    # 将样本的词嵌入与注意力机制相乘得到
    # (seq_len,300):给与每个单词不同的权重
    attention_embedding = example_matrix * attention
    if method == 'mean':
        return np.mean(attention_embedding, axis=0)
    else:
        return np.max(attention_embedding, axis=0)


def Find_embedding_with_windows(embedding_matrix, window_size=2,
                                method='mean'):
    '''
    generate embedding use window
    滑窗处理embedding 然后聚合
    embedding_matrix, input sentence's embedding
    window_size, 2, 3, 4
    method, max/ mean
    @return: ndarray of embedding
    '''
    # 最终的词向量
    result_list = []
    # 遍历input的长度， 根据窗口的大小获取embedding， 进行mean操作， 然后将得到的结果extend到list中， 最后进行mean max 聚合
    for k1 in range(len(embedding_matrix)):
        # 如何当前位置 + 窗口大小 超过input的长度， 则取当前位置到结尾
        # mean 操作后要reshape 为 （1， 300）大小
        if int(k1 + window_size) > len(embedding_matrix):
            result_list.extend(
                np.mean(embedding_matrix[k1:], axis=0).reshape(1, 300))
        else:
            result_list.extend(
                np.mean(embedding_matrix[k1:k1 + window_size],
                        axis=0).reshape(1, 300))
    if method == 'mean':
        return np.mean(result_list, axis=0)
    else:
        return np.max(result_list, axis=0)


def get_lda_features_helper(lda_model, document):
    '''
    Transforms a bag of words document to features.
    它返回每个主题在文档中所占的比例
    lda_model: lda_model
    document, input
    @return: lda feature
    '''
    # 基于bag of word 格式数据获取lda的特征，获取给定文档的主题分布
    topic_importances = lda_model.get_document_topics(document,
                                                      minimum_probability=0)
    # 将list转化成ndarray
    topic_importances = np.array(topic_importances)
    return topic_importances[:, 1]


def get_lda_features(data, LDAmodel):
    """
    获取lda特征
    :param data: 数据
    :param LDAmodel:lda模型
    :return:
    """
    # isinstance()函数来判断一个对象是否是一个已知的类型
    if isinstance(data.iloc[0]['text'], str):
        # 以空格为分隔符进行分割
        data['text'] = data['text'].apply(lambda x: x.split())
    # 将文档转换为单词袋(BoW)格式= (token_id, token_count)元组的列表
    data['bow'] = data['text'].apply(
        lambda x: LDAmodel.id2word.doc2bow(x))
    # 得到每个主题在文档中所占的比例
    data['lda'] = list(
        map(lambda doc: get_lda_features_helper(LDAmodel, doc), data['bow']))
    cols = [x for x in data.columns if x not in ['lda', 'bow']]
    # 返回拼接后的lda特征
    return pd.concat([data[cols], array2df(data, 'lda')], axis=1)


def tag_part_of_speech(data):
    '''
    语言的词性部分，然后计算名词，形容词和动词的数目
    data, input data.
    @return:
    noun_count,num of noun
    adjective_count, num of adj
    verb_count, num of verb
    '''
    # 获取文本的词性， 并计算名词，动词，形容词的个数
    # 采用jieba默认模式进行词性标注
    words = [tuple(x) for x in list(pseg.cut(data))]
    # 名词个数统计
    noun_count = len(
        [w for w in words if w[1] in ('NN', 'NNP', 'NNPS', 'NNS')])
    # 形容词个数统计
    adjective_count = len([w for w in words if w[1] in ('JJ', 'JJR', 'JJS')])
    # 动词个数统计
    verb_count = len([
        w for w in words if w[1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
    ])
    # 返回名词，动词，形容词的个数
    return noun_count, adjective_count, verb_count


# 将英文中的标点符号映射成中文中的标点符号
ch2en = {
    '！': '!',
    '？': '?',
    '｡': '.',
    '（': '(',
    '）': ')',
    '，': ',',
    '：': ':',
    '；': ';',
    '｀': ','
}


def get_basic_feature_helper(text):
    '''
    得到基本的特征： 词的个数，大写个数统计，大写占比，感叹号的个数
    @param {type}
    df, dataframe
    @return:
    df, dataframe
    '''
    # 如果test是字符串，则进行分割
    if isinstance(text, str):
        text = text.split()
    # 分词
    queryCut = [i if i not in ch2en.keys() else ch2en[i] for i in text]
    # 词的个数
    num_words = len(queryCut)
    # 大写的个数
    capitals = sum(1 for c in queryCut if c.isupper())
    # 大写的占比
    caps_vs_length = capitals / num_words
    # 感叹号的个数
    num_exclamation_marks = queryCut.count('!')
    # 问号个数
    num_question_marks = queryCut.count('?')
    # 标点符号个数
    # string.punctuation:标点符号
    num_punctuation = sum(queryCut.count(w) for w in string.punctuation)
    # *&$%字符的个数
    num_symbols = sum(queryCut.count(w) for w in '*&$%')
    # 唯一词的个数
    num_unique_words = len(set(w for w in queryCut))
    # 唯一词 与总词数的比例
    words_vs_unique = num_unique_words / num_words
    # 获取名词， 形容词， 动词的个数， 使用tag_part_of_speech函数
    nouns, adjectives, verbs = tag_part_of_speech("".join(text))
    # 名词占词的个数的比率
    nouns_vs_length = nouns / num_words
    # 形容词占词的个数的比率
    adjectives_vs_length = adjectives / num_words
    # 动词占词的个数的比率
    verbs_vs_length = verbs / num_words
    # 首字母大写其他小写的个数
    count_words_title = len([w for w in queryCut if w.istitle()])
    # 平均词的个数
    mean_word_len = np.mean([len(w) for w in queryCut])
    return {
        'num_words': num_words,
        'capitals': capitals,
        'caps_vs_length': caps_vs_length,
        'num_exclamation_marks': num_exclamation_marks,
        'num_question_marks': num_question_marks,
        'num_punctuation': num_punctuation,
        'num_symbols': num_symbols,
        'num_unique_words': num_unique_words,
        'words_vs_unique': words_vs_unique,
        'nouns': nouns,
        'adjectives': adjectives,
        'verbs': verbs,
        'nouns_vs_length': nouns_vs_length,
        'adjectives_vs_length': adjectives_vs_length,
        'verbs_vs_length': verbs_vs_length,
        'count_words_title': count_words_title,
        'mean_word_len': mean_word_len
    }


def get_basic_feature(data):
    """
    得到基础特征
    :param data: 数据
    :return: 返回基础特征
    """
    tmp = data['text'].apply(
        lambda x: pd.Series(get_basic_feature_helper(x)))
    return pd.concat([data, tmp], axis=1)
