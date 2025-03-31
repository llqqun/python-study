document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // 初始化变量
    let isWaitingForResponse = false;

    // 发送按钮点击事件
    sendButton.addEventListener('click', sendMessage);

    // 输入框回车键发送消息
    userInput.addEventListener('keydown', function(event) {
        // 检测是否按下了Enter键且没有按住Shift键
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // 阻止默认的换行行为
            sendMessage();
        }
    });

    // 发送消息函数
    function sendMessage() {
        const message = userInput.value.trim();
        
        // 检查消息是否为空或者是否正在等待响应
        if (message === '' || isWaitingForResponse) {
            return;
        }

        // 添加用户消息到聊天区域
        addMessage(message, 'user');
        
        // 清空输入框
        userInput.value = '';
        
        // 设置等待响应状态
        isWaitingForResponse = true;
        
        // 调用服务端API获取AI响应
        getAIResponse(message);
    }

    // 添加消息到聊天区域
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // 滚动到底部
        scrollToBottom();
    }

    // 从服务端获取AI响应
    function getAIResponse(userMessage) {
        // 创建一个空的AI消息容器
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = ''; // 初始为空
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // 滚动到底部
        scrollToBottom();

        // 发送POST请求到后端服务器
        fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => {
          console.log(response)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            function readStream() {
                return reader.read().then(({done, value}) => {
                    if (done) {
                        isWaitingForResponse = false;
                        return;
                    }

                    buffer += decoder.decode(value, {stream: true});
                    const lines = buffer.split('\n');
                    console.log(lines)
                    // 保留最后一个不完整的行
                    buffer = lines.pop() || '';
                    
                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.slice(6));
                                if (data.char) {
                                    messageContent.textContent += data.char;
                                    scrollToBottom();
                                }
                            } catch (e) {
                                console.error('Error parsing JSON:', e);
                            }
                        }
                    });

                    return readStream();
                }).catch(error => {
                    console.error('Stream reading error:', error);
                    messageContent.textContent += '\n[读取响应时出错]';
                    isWaitingForResponse = false;
                });
            }

            return readStream();
        })
        .catch(error => {
            console.error('Fetch error:', error);
            messageContent.textContent = '抱歉，无法连接到服务器，请检查服务器是否正常运行。';
            isWaitingForResponse = false;
        });
    }
    // 生成AI响应（简单的规则引擎）
    function generateResponse(userMessage) {
        // 转换为小写以便于匹配
        const lowerMessage = userMessage.toLowerCase();
        
        // 简单的规则匹配
        if (lowerMessage.includes('你好') || lowerMessage.includes('嗨') || lowerMessage.includes('hi') || lowerMessage.includes('hello')) {
            return '你好！很高兴与你交流。我是AI助手，有什么可以帮助你的吗？';
        } else if (lowerMessage.includes('谢谢') || lowerMessage.includes('感谢')) {
            return '不客气！如果还有其他问题，随时可以问我。';
        } else if (lowerMessage.includes('再见') || lowerMessage.includes('拜拜')) {
            return '再见！有需要随时回来找我。';
        } else if (lowerMessage.includes('名字') || lowerMessage.includes('叫什么')) {
            return '我是AI助手，很高兴为你服务！';
        } else if (lowerMessage.includes('时间') || lowerMessage.includes('几点')) {
            return '当前时间是：' + new Date().toLocaleTimeString();
        } else if (lowerMessage.includes('日期') || lowerMessage.includes('几号')) {
            return '今天日期是：' + new Date().toLocaleDateString();
        } else if (lowerMessage.includes('天气')) {
            return '抱歉，我目前无法获取实时天气信息。你可以查看天气预报应用或网站获取准确信息。';
        } else if (lowerMessage.includes('笑话') || lowerMessage.includes('段子')) {
            const jokes = [
                '为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 = Dec 25。',
                '一个程序员走进酒吧，点了一杯啤酒。酒保问："要不要再来一杯？" 程序员回答："不，我不处理递归。"',
                '为什么程序员不喜欢大自然？因为那里有太多的bugs。',
                '程序员的三大谎言：代码没问题；这个很容易修复；我们明天就发布。'
            ];
            return jokes[Math.floor(Math.random() * jokes.length)];
        } else {
            // 默认回复
            const defaultReplies = [
                '这是个有趣的问题。让我思考一下...',
                '我理解你的问题，不过这个领域我还在学习中。',
                '谢谢你的提问！这让我有机会学习新知识。',
                '我不太确定，但我可以尝试帮你找到答案。',
                '这是个好问题！我需要更多信息来给你一个准确的回答。'
            ];
            return defaultReplies[Math.floor(Math.random() * defaultReplies.length)];
        }
    }

    // 滚动聊天区域到底部
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});