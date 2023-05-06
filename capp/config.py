import openai

"""
    列出当前可用的模型，并提供有关每个模型的基本信息，例如所有者和可用性。
"""
# openai.api_key = "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"/
# print(openai.Model.list())


"""
    检索模型实例，提供有关模型的基本信息
"""
print(openai.Model.retrieve("text-ada-001"))

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

import os, openai


def info(request):
    return JsonResponse({'msg': '200'})


def list_info(request):
    # return JsonResponse({'msg': '彭跃欣'})

    # 账户认证
    openai.api_key = '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'

    # 生成文本
    # text = openai.Completion.create(
    #     engine="davinci",
    #     prompt="Hello, my name is",
    #     temperature=0.5,
    #     max_tokens=50
    # )

    # 打印文本
    # print(text.choices[0].text)

    # 生成文本
    # text = openai.Completion.create(
    #     # 使用这个模型
    #     engine="text-davinci-002",
    #     # 生成 Hello, my name is 样式的文本
    #     prompt="Hello, my name is",
    #     # 相似度0.5
    #     temperature=0.5,
    #     # 最多生成50字符的文本
    #     max_tokens=50
    # )
    #
    # return JsonResponse({'msg':text.choices[0].text})

    # openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = """
    Decide whether a Mike's sentiment is positive, neutral, or negative.
    Mike: I don't like homework!
    Sentiment:

    使用了文本生成模型"text-davinci-003"。它将一个文本"prompt"作为输入，
    生成一个最大长度为100个标记的文本响应。"temperature"参数控制生成文本的多样性，0表示完全确定性，值越高表示生成的文本越随机。
    """
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=100, temperature=0)
    return JsonResponse({'MSG': response})


"""
    代码生成一个序列，内容包含上海的温度
"""


def chat_info(request):
    #  设置API密钥(配完环境变量的方法用这种)
    # openai.api_key = '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'
    # 创建openai API请求，调用openai.Completion.create方法（该方法是生成文本的）
    response = openai.Completion.create(
        model="text-davinci-003",  # 使用的模型
        prompt="\"\"\"\n推荐几部好看的书籍\n\"\"\"",  # 生成样式
        temperature=0,  # temperature"参数控制生成文本的多样性，0表示完全确定性，值越高表示生成的文本越随机。
        max_tokens=256,  # 最大长度的文本响应
        top_p=1,  # 控制生成文本的多样性
        frequency_penalty=0,  # 控制生成文本中出现频率较高的单词的程度
        presence_penalty=0  # 控制生成文本中出现频率较低的单词的程度
    )

    print(response)

    return JsonResponse({'msg': response})













