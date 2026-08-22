import json
import jieba
import joblib
import lightgbm as lgb
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
from sklearn.preprocessing import MultiLabelBinarizer
# 多标签学习，将 多标签学习问题转化为多个独立的二分类问题
from skmultilearn.problem_transform import BinaryRelevance

from embedding import Embedding
from features import get_basic_feature, get_embedding_feature, get_lda_features, get_tfidf


class Classifier:
    def __init__(self, train_mode=False):
        # 向量初始化
        # 停用词初始化
        self.stopWords = [
            x.strip() for x in open('./data/stopwords.txt', 'r', encoding='UTF-8').readlines()
        ]
        # 编码初始化
        self.embedding = Embedding()
        self.embedding.load()
        # 标签索引字典初始化
        self.labelToIndex = json.load(
            open('./data/label2id.json', encoding='utf-8'))
        # id标签字典初始化
        self.ix2label = {v: k for k, v in self.labelToIndex.items()}
        # 区分训练集、验证集、测试集
        if train_mode:
            self.train = pd.read_csv('./data/train.csv', encoding='gbk',
                                     sep='\t').dropna().reset_index(drop=True)
            self.dev = pd.read_csv('./data/eval.csv', encoding='gbk',
                                   sep='\t').dropna().reset_index(drop=True)
            self.test = pd.read_csv('./data/test.csv', encoding='gbk',
                                    sep='\t').dropna().reset_index(drop=True)
        # 初始化中间变量列名
        self.exclusive_col = ['text', 'lda', 'bow', 'label']

    def feature_engineer(self, data):
        """
        特征工程
        :param data: 数据集
        :return:
        """
        # tf-idf编码
        data = get_tfidf(self.embedding.tfidf, data)
        # word2vec编码
        data = get_embedding_feature(data, self.embedding.w2v)
        # lda特征
        data = get_lda_features(data, self.embedding.lda)
        # 基础特征
        data = get_basic_feature(data)
        # 返回data
        return data

    def trainer(self):
        # 对训练集做特征工程
        self.train = self.feature_engineer(self.train)
        # 对验证集做特征工程
        dev = self.feature_engineer(self.dev)
        # 列特征
        cols = [x for x in self.train.columns if x not in self.exclusive_col]
        # 训练集
        X_train = self.train[cols]
        #         y_train = train['label'].apply(lambda x: eval(x))
        y_train = self.train['label']
        # 验证集
        X_test = dev[cols]
        #         y_test = dev['label'].apply(lambda x: eval(x))
        y_test = dev['label']
        # 多标签二值化
        mlb = MultiLabelBinarizer(sparse_output=False)
        y_train_new = []
        y_test_new = []
        for i in y_train:
            y_train_new.append([i])
        for i in y_test:
            y_test_new.append([i])

        y_train = mlb.fit_transform(y_train_new)
        y_test = mlb.transform(y_test_new)
        #         print(y_train)
        #         print(X_train)
        print('X_train: ', X_train.shape, 'y_train: ', y_train.shape)
        print(mlb.classes_)
        # 初始化多标签训练
        # 将多标签学习问题转化为多个独立的二分类问题，基分类器为lgb
        self.clf_BR = BinaryRelevance(classifier=lgb.LGBMClassifier(
            max_depth=5,
            learning_rate=0.1,
            n_estimators=100,
            silent=True,
            objective='binary',
            n_jobs=-1,
            reg_alpha=0,
            reg_lambda=1,
            device='cpu',  # gpu
            missing=None),
            require_dense=[False, True])
        # 训练
        print('开始训练')
        self.clf_BR.fit(X_train, y_train)
        # 预测
        print('开始预测')
        prediction = self.clf_BR.predict(X_test)
        print(prediction)
        print(y_test)
        print('----计算准确率----')
        print(metrics.accuracy_score(y_test, prediction))

    # 保存模型
    def save(self):
        joblib.dump(self.clf_BR, './model/clf_BR')
    # 加载模型
    def load(self):
        self.model = joblib.load('./model/clf_BR')

    # 预测
    def predict(self, text):
        df = pd.DataFrame([[text]], columns=['text'])
        # 预处理
        df['text'] = df['text'].apply(lambda x: " ".join(
            [w for w in jieba.cut(x) if w not in self.stopWords and w != '']))
        # 获取tf-idf编码
        df = get_tfidf(self.embedding.tfidf, df)
        # 获取word2vec编码
        df = get_embedding_feature(df, self.embedding.w2v)
        # 获取lda特征
        df = get_lda_features(df, self.embedding.lda)
        # 获取基础特征
        df = get_basic_feature(df)
        # 去除中间特征
        cols = [x for x in df.columns if x not in self.exclusive_col]
        # 预测
        pred = self.model.predict(df[cols]).toarray()[0]
        print(pred)
        print(self.ix2label)
        # 返回预测值
        return [self.ix2label.get(i) for i in range(len(pred)) if pred[i] > 0]


if __name__ == "__main__":
    bc = Classifier(train_mode=True)
    # 训练模型
    bc.trainer()
    # 保存模型
    bc.save()
