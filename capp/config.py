import openai

"""
    列出当前可用的模型，并提供有关每个模型的基本信息，例如所有者和可用性。
"""
openai.api_key = "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"
# print(openai.Model.list())


"""
    检索模型实例，提供有关模型的基本信息
"""
print(openai.Model.retrieve("text-ada-001"))


