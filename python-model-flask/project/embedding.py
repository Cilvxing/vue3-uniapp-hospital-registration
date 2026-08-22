import pandas as pd
import numpy as np
from gensim import models
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import jieba
from gensim.models import LdaMulticore
from features import label2idx
import gensim
import config
from gensim.test.utils import datapath


class SingletonMetaclass(type):
    '''
    metaclass是创建类，所以必须从`type`类型派生
    定义一个元类，作为创建类的模板:这部分知识可以参考：https://realpython.com/python-metaclasses/
    元类的作用是允许自定义类 实例化
    '''

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(SingletonMetaclass,
                                    self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Embedding(metaclass=SingletonMetaclass):
    # 指定它的元类是自定义元类Meta，而不是标准的元类类型。这是通过在类定义中使用metaclass关键字完成的
    """
    这是嵌入类，可能调用多次，使用单例模式
    在这个类中，我们可以使用tfidf、word2vec、fasttext、autoencoder词嵌入
    """

    def __init__(self):
        # 停用词
        self.stopWords = [x.strip() for x in open('./data/stopwords.txt', 'r', encoding='UTF-8').readlines()]

    def load_data(self, path):
        '''
        加载所有数据，然后做分词
        '''
        # 读取训练数据
        data = pd.read_csv(path, encoding='gbk', sep='\t')
        # 用空字符串填充缺失值
        data = data.fillna("")
        # 对series的每一行调用匿名函数处理
        # 匿名函数处理流程为:每一行文本按空格分割，循环每一个词语，如果词语不是停用词与空白字符，则以空格为连接拼接成字符串
        data["text"] = data['text'].apply(lambda x: " ".join([w for w in x.split()
                                                              if w not in self.stopWords and w != '']))
        # 构建label与索引的映射字典
        self.labelToIndex = label2idx(data)
        # 将科室做映射，映射成科室编码
        data['label'] = data['label'].map(self.labelToIndex)
        # 将科室编码取浮点数
        data['label'] = data.apply(lambda row: float(row['label']), axis=1)
        data = data[['text', 'label']]

        # 返回值的列表
        self.train = data['text'].tolist()

    def trainer(self):
        '''
        Train tfidf,  word2vec, fasttext and autoencoder
        '''
        """
        一、tf-idf
        """
        # 定义tf-idf模型:将原始文档转化为TF-IDF矩阵，相当于相当于CountVectorizer后跟TfidfTransformer
        # max_df：在构建词汇表时，忽略文档频率严格高于给定阈值的术语
        # min_df：在构建词汇表时，忽略文档频率严格低于给定阈值的术语
        # ngram_range:使用unigrams and bigrams
        count_vect = TfidfVectorizer(stop_words=self.stopWords,
                                     max_df=0.4,
                                     min_df=0.001,
                                     ngram_range=(1, 2))
        print(self.train[:5])
        # 训练tf-idf模型
        self.tfidf = count_vect.fit(self.train)

        """
        二、word2vec
        """
        # 将文本转变成单词列表
        self.train = [sample.split() for sample in self.train]

        # 加载Word2Vec模型
        # min_count：忽略所有总频率低于此的单词
        # window:句子中当前词和预测词之间的最大距离
        # vector_size:单词向量维度
        # sample：设置高频词随机下采样的阈值，有效范围是(0,1e -5)
        # alpha：初始学习率
        # min_alpha：随着训练的进行，学习率将线性下降到min_alpha
        # negative：如果> 0，将使用负采样，如果设置为0，则不使用负采样。
        # workers：多核
        # epochs：在语料库上的迭代次数
        # max_vocab_size：在词汇建立过程中限制内存
        self.w2v = models.Word2Vec(min_count=2,
                                   window=5,
                                   size=300,
                                   sample=6e-5,
                                   alpha=0.03,
                                   min_alpha=0.0007,
                                   negative=15,
                                   workers=4,
                                   iter=30,
                                   max_vocab_size=50000)
        # 从一个句子序列构建词汇表
        self.w2v.build_vocab(self.train)
        # 根据句子序列更新模型的神经权重，为了支持从alpha到min_alpha的学习率衰减，必须提供必须提供total_examples(句子的数量)
        # 如果句子与之前为build_vocab()提供的语料库相同，则可以简单地使用total_examples=self.corpus_count
        # total_examples：句子的数目
        # epochs：在语料库上的迭代次数
        # report_delay：几秒钟后报告进度
        self.w2v.train(self.train,
                       total_examples=self.w2v.corpus_count,
                       epochs=15,
                       report_delay=1)

        """
        三、LDA主题特征
        """
        # 实现单词和它们的整数id之间的映射
        self.id2word = gensim.corpora.Dictionary(self.train)
        # 将文档转换为单词袋(BoW)格式= (token_id, token_count)元组的列表
        corpus = [self.id2word.doc2bow(text) for text in self.train]
        # LDA算法的优化实现，能够利用多核cpu的能力
        # corpus:稀疏矩阵(num_documents, num_terms)
        # id2word:实现单词和它们的整数id之间的映射
        # num_topics:要求从训练语料库中提取的潜在主题的数量
        # workers:进程数
        # chunksize：每个训练块中使用的文档数量
        # passes：训练时通过语料库的次数
        # alpha：使用固定的归一化非对称先验值
        self.LDAmodel = LdaMulticore(corpus=corpus,
                                     id2word=self.id2word,
                                     num_topics=30,
                                     workers=4,
                                     chunksize=4000,
                                     passes=7,
                                     alpha='asymmetric')

    def saver(self):
        '''
        保存所有模型
        '''
        # json.dump()函数将python对象编码成JSON字符串并写入到文件中
        joblib.dump(self.tfidf, './model/tfidf')
        # 加载经过训练的单词向量
        self.w2v.wv.save_word2vec_format('./model/w2v.bin',
                                         binary=False)
        # 保存预训练模型到disk
        self.LDAmodel.save('./model/lda')

    def load(self):
        '''
        加载所有编码模型
        '''
        # json.load()函数将JSON数据解码成python字典对象
        self.tfidf = joblib.load('./model/tfidf')
        # 加载word2vec模型
        self.w2v = models.KeyedVectors.load_word2vec_format('./model/w2v.bin', binary=False)
        # 加载lda模型
        self.lda = models.ldamodel.LdaModel.load('./model/lda')


if __name__ == "__main__":
    em = Embedding()
    # 加载训练数据
    em.load_data(config.train_data_file)
    # 训练tfidf,  word2vec, fasttext and autoencoder模型
    em.trainer()
    # 保存模型
    em.saver()
    print('模型已经保存')
