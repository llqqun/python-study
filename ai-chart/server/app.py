from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # 简单的规则引擎生成回复
    response = generate_response(user_message)
    
    def generate():
        for char in response:
            yield f"data: {json.dumps({'char': char})}\n\n"
            time.sleep(0.03)  # 模拟打字效果的延迟
    
    return Response(generate(), mimetype='text/event-stream')

def generate_response(user_message):
    # 转换为小写以便于匹配
    lower_message = user_message.lower()
    
    # 简单的规则匹配
    if any(word in lower_message for word in ['你好', '嗨', 'hi', 'hello']):
        return '你好！很高兴与你交流。我是AI助手，有什么可以帮助你的吗？'
    elif any(word in lower_message for word in ['谢谢', '感谢']):
        return '不客气！如果还有其他问题，随时可以问我。'
    elif any(word in lower_message for word in ['再见', '拜拜']):
        return '再见！有需要随时回来找我。'
    elif any(word in lower_message for word in ['名字', '叫什么']):
        return '我是AI助手，很高兴为你服务！'
    elif any(word in lower_message for word in ['时间', '几点']):
        return f'当前时间是：{time.strftime("%H:%M:%S")}'
    elif any(word in lower_message for word in ['日期', '几号']):
        return f'今天日期是：{time.strftime("%Y-%m-%d")}'
    elif '天气' in lower_message:
        return '抱歉，我目前无法获取实时天气信息。你可以查看天气预报应用或网站获取准确信息。'
    elif any(word in lower_message for word in ['笑话', '段子']):
        jokes = [
            '为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 = Dec 25。',
            '一个程序员走进酒吧，点了一杯啤酒。酒保问："要不要再来一杯？" 程序员回答："不，我不处理递归。"',
            '为什么程序员不喜欢大自然？因为那里有太多的bugs。',
            '程序员的三大谎言：代码没问题；这个很容易修复；我们明天就发布。'
        ]
        return jokes[int(time.time()) % len(jokes)]
    else:
        # 默认回复
        default_replies = [
            '这是个有趣的问题。让我思考一下...',
            '我理解你的问题，不过这个领域我还在学习中。',
            '谢谢你的提问！这让我有机会学习新知识。',
            '我不太确定，但我可以尝试帮你找到答案。',
            '这是个好问题！我需要更多信息来给你一个准确的回答。'
        ]
        return default_replies[int(time.time()) % len(default_replies)]

if __name__ == '__main__':
    app.run(debug=True, port=5000)