# -*- coding: utf-8 -*-
# description: 主程序入口
# author:xzh
# create time:2023-10-9
#coding:utf-8

from flask import Flask, url_for,render_template ,request ,flash,Response, make_response
import requests
import json
import openai
import datetime
import time


openai.api_base="https://api.aiwe.io/v1"
openai.api_key=""  

app = Flask(__name__)
@app.route('/')
def default():
    #return render_template('chat.html')
    return render_template('chat_test1.html')

@app.route('/test')
def index_test():
    ans_number = request.args.get('ans_number', '')
    
    #return render_template('testsse.html')
    return render_template('chat_test1.html',get_ans=ans_number)

@app.route('/index')
def index():
    return 'this is a ai chat application'

@app.route('/yiyan', methods=['GET' , 'POST'])
def chat_yiyan():
    pass

@app.route('/gptsse', methods=['GET' , 'POST'])
def chat_sse():
    prompt = request.args.get('prompt','')
    #prompt = request.form.get('prompt')
    #prompt = request.form['prompt']
    print(prompt)
    return Response(stream_response(prompt), mimetype='text/event-stream')
    #return Response(gpt_3dot5_turbo_stream(prompt), mimetype='text/event-stream')

def stream_response(prompt):
    #user_ip = request.remote_addr
    start_time = time.time()
    #print("user_ip:" + user_ip)
    print(prompt)
    response = openai.ChatCompletion.create(
        #url='https://api.aiwe.io/v1',
        model='gpt-3.5-turbo-16k-0613',
        messages=[
            {'role': 'user',
             'content': prompt}
        ],
        temperature=0.7,
        stream=True
    )
    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        #chunk_message = chunk['choices'][0]['delta']['content']
        collected_messages.append(chunk_message)  # save the message
        #输入到浏览器
        #yield f'event: {source}\ndata: {chunk_message}\n\n'
        #yield f'data: {chunk_message}\n\n'
        print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
        if chunk_message:
            message=chunk_message['content']
            message=message.replace('\n', '<br>')
            yield f'data: { message }\n\n'
            print(message)
        else:
            yield f'data:{"[done]"}\n\n'

    # print the time delay and text received
    print(f"Full response received {chunk_time:.2f} seconds after request")
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    print(f"Full conversation received: {full_reply_content}")
    return full_reply_content


@app.route('/gpt', methods=['GET' , 'POST'])
def chat_gpt():
    #user_ip = request.remote_addr
    start_time = time.time()
    #print("user_ip:"+user_ip)

    question_content="请简单介绍一下你自己"
    # if request.method == 'POST':
    #     token=request.headers.get("Authorization")
    #     question_content=request.get_data().decode("utf-8")
    print(question_content)

    # send a ChatCompletion request
    api_response = openai.ChatCompletion.create(
        #url='https://api.aiwe.io/v1',
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user',
             'content': question_content}
        ],
        temperature=0,
        stream=True  # again, we set stream=True
    )
    # response = request.headers(content_type='text/event-stream')
    # response = make_response('make_response')  # 获取响应对象
    # response.headers['content_type'] = 'text/event-stream'
    #
    # answer = ''
    # for part in api_response:
    #     finish_reason = part["choices"][0]["finish_reason"]
    #     if "content" in part["choices"][0]["delta"]:
    #         content = part["choices"][0]["delta"]["content"]
    #         answer += content
    #         content = content.replace('\n', '<br>')  # 将换行替换为<br>，用于前端显示。
    #         response.send(f"data: {content}\n\n")  # 使用 Server-Sent Events (SSE) 格式发送数据
    #     elif finish_reason:
    #         response.send(f"event: end\ndata: {answer}\n\n")

    # # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        #chunk_message = chunk['choices'][0]['delta']['content']
        #yield f'data: {chunk_message}'
        collected_messages.append(chunk_message)  # save the message
        print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text

    # print the time delay and text received
    print(f"Full response received {chunk_time:.2f} seconds after request")
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    print(f"Full conversation received: {full_reply_content}")
    return full_reply_content

def chat():
    #首先显示一下远程客户的IP
    user_ip = request.remote_addr
    start_time=datetime.datetime.now()
    print(user_ip +" start:"+str(start_time))

    question_text = ""

    if request.method == 'POST':
        #chat_content = request.get_json()['text']
        #chat_content=request.form.get('text')
        #chat_content=request.values.get('text')

        token=request.headers.get("Authorization")
        question_text = request.get_data().decode("utf-8")
        

    if (question_text==""):
        return "fail"
    return "abcd"

        # data={"role": role, "content": question_text}
        # datas.append(data)
        #以下这两种方案只能输出一种
        #return (get_for_Completions(datas))
    #return gpt_3dot5_turbo(question_text)
        # end_time=datetime.datetime.now()
        # spend_time=end_time -start_time
        # print(user_ip+" end:"+str(end_time)+"spend time:"+str(spend_time))
        #return baidu_wxyy_flow(question_text)
        #return "success"

#使用函数调用获取chatGPT3.5 的问题答案
def get_for_Completions(message_text):
    #将请求信息输出一次
    print(message_text)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            #max_tokens=7,
            temperature=0.7,
            messages=message_text
        # messages=[{"role": "system", "content": "Python怎么从入门到精通，具体的学习方法是什么？"},
        #     {"role": "user", "content": "Who won the world series in 2020?"},
        #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        #     {"role": "user", "content": "Where was it played?"}
        #     ]
        )
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")

    #response 的数据类型为<class 'openai.openai_object.OpenAIObject'>
    #print (type(response))
    #result = response.choices[0].message
    result = ""
    try:
        for re in response.choices:
            result += re.message.content
    except:
        result=response.error.message

    print(result)
    return result.replace('\n\n', '<br>')

#使用网页版方案获取chatGPT3.5 的问题答案
def gpt_3dot5_turbo_stream(message_text):
    start_time = time.time()
    #print(message_text)
    #api = "https://api.foforise.xyz/v1/chat/completions"
    #api = "https://aibros.top/v1/chat/completions"
    api = "https://api.aiwe.io/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "
        
    }
    json_data = {
        "model": "gpt-3.5-turbo-16k-0613",
        "stream":True,
        #"model": "gpt-3.5-turbo",
        "messages": [
            {'role': 'user',
             'content': message_text}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url=api, headers=headers, json=json_data,stream=True)
        #response.encoding = "utf-8"
        #response.raise_for_status()
    
    except requests.exceptions.HTTPError as e:
        print(f'HTTP错误, 状态码: {e.response.status_code}, {e}')
    

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                res=chunk.decode('utf-8')[5:]
                print(res)
                #content_dict = json.loads(res)
                if res:
                    pass
                    #chunk_decoded = chunk.decode('utf-8')  # Decode the chunk
                    #content_dict = json.loads(res)
                    #content = content_dict['choices'][0]['delta']
                    #print(content)
                else:
                    pass
                #print(res.json()['choices'][0]['delta'])
                #res_json = json.loads(chunk[5:])

                # 解析响应数据
                #parsed_data = parse_response(chunk)
                #print(chunk.decode('utf-8')[5:])
                # 处理解析后的数据
                #process_data(parsed_data)
            else:
                pass
    else:
        print("请求失败，状态码：", response.status_code)

    collected_chunks = []
    collected_messages = []
    

#获取百度文心一言的token
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    api_key = ""
    secret_key = ""

    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=" + api_key + "&client_secret=" + secret_key + "&grant_type=client_credentials"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_access_token_flow():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    api_key = ""
    secret_key = ""
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+secret_key

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def baidu_wxyy_flow():
    # user_ip = request.remote_addr
    # print(user_ip)
    # remote_url=request.url
    # print (remote_url)
    value=''
    if request.method == 'POST':
        value=request.get_data().decode("utf-8")
    print(value)

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token_flow()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": value
            }
        ],
        "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, stream=True)

    for line in response.iter_lines():
        print(response.status_code)
        # print(response.)
        str = line.decode('utf-8')
        data_str=str[5:]
        # print (data_str)
        if len(data_str) >1:
            data_dict = json.loads(data_str)
            print(data_dict['result'])
            return data_dict['result']
            #return Response(stream_with_context(generate()))

@app.route('/wxyy', methods=['GET','POST'])
#def baidu_wxyy(message_text):
def baidu_wxyy():
    # 将请求信息输出一次
    #print(message_text)
    value = ''
    if request.method == 'POST':
        value = request.get_data().decode("utf-8")
    print(value)
    start_time = datetime.datetime.now()
    print("start:" + str(start_time))

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": value
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = json.loads(response.text)

    end_time=datetime.datetime.now()
    #spend_time=end_time -start_time
    print("end:"+str(end_time))

    print(res["result"])
    return res["result"].replace('\n\n', '<br>')

if __name__ == '__main__':
    # baidu_wxyy_flow('给我推荐一些自驾游路线')
    app.run(debug=True, host='0.0.0.0', port=5000)
