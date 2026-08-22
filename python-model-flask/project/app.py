
from flask import Flask, request
import json
from text_classifier_model import Classifier

# 初始化模型， 避免在函数内部初始化，耗时过长
bc = Classifier()
bc.load()

# 初始化flask
app = Flask(__name__)

@app.route('/check/<text>')
# 定义函数，初始化username = None
def check_text(text=None):
    '''
    @description: 以RESTful的方式获取模型结果, 传入参数为title: 图书标题， desc: 图书描述
    @param {type}
    @return: json格式， 其中包含标签和对应概率
    '''
    result = {}
    label = bc.predict(text)
    result = {
        "label": label
    }
    return json.dumps(result, ensure_ascii=False)



# python3 -m flask run
if __name__ == '__main__':
    app.run(port=3389, debug=True)
