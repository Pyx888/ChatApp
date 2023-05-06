# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# import os
# from PyPDF2 import PdfReader
# import docx
# from docx2pdf import convert
# import pdfplumber
#
# """
#          打开文件filepath，并且以二进制的方式进行读取，并且使用f来引用这个文件
#          使用PdfReader函数读取PDF文件内容，并且将结果赋值给pdf变量
#          返回pdf变量中的页面数量，也就是pdf.pages的长度
# """
#
#
# def get_pdf_page_count(filepath):
#     with open(filepath, 'rb') as f:
#         pdf = PdfReader(f)
#         return len(pdf.pages)
#
#
# def read_pdf(filepath):
#     with open(filepath, 'rb') as f:
#         pdf = PdfReader(f)
#         text = ''
#         paragraph = ""
#         results = []
#
#         for page in range(len(pdf.pages)):
#
#             lines = pdf.pages[page].extract_text().split("\n")
#             for i in lines:
#                 paragraph += i
#                 if i.endswith("。") or i.endswith(".") or i.endswith("!") or i.endswith("?"):
#                     results.append(paragraph)
#                     paragraph = ""
#
#         return results
#
#
# def split_paragraphs(text):
#     return text.split('\n\n')
#
#
# def uploadfile(request):
#     my_file = request.FILES.get('file')
#     ext = os.path.splitext(my_file.name)[1]  # 获取文件扩展名
#     if ext not in ['.pdf', '.doc', '.docx']:
#         return JsonResponse({"code": 9998, "message": "格式错误"})
#
#     print(my_file)
#     filename = "./static/file/" + my_file.name
#     if my_file:
#         with open(filename, 'wb+') as f:
#
#             for chunk in my_file.chunks():
#                 f.write(chunk)
#         print(ext)
#         if ext in ['.doc', '.docx']:
#             print("+++++++")
#             convert(filename, "./static/file/output.pdf")
#             print("------")
#             filename = "./static/file/output.pdf"
#
#         page_count = get_pdf_page_count(filename)  # 获取页码数
#
#         print(page_count)
#         if page_count <= 10:
#             paragraphs = read_pdf(filename)  # 获取文本内容
#             print(paragraphs)
#             return JsonResponse(
#                 {"code": 0000, "message": "成功", "data": {"page_count": page_count, "paragraphs": paragraphs}})
#
#         return JsonResponse({"code": 0000, "message": "成功", "data": {"page_count": page_count}})
#
#
#
#
#
#
#





import os
import fitz
import docx


from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from PyPDF2 import PdfReader
from docx2pdf import convert
from pdf2docx import Converter, parse


# 获取页数
def get_pdf_page_count(filepath):
    with open(filepath, 'rb') as f:
        pdf = PdfReader(f)
        return len(pdf.pages)

# 读取文件内容
def read_pdf(filepath):
    doc = docx.Document(filepath)
    paras = ""
    result = []
    # 遍历所有段落
    for i in doc.paragraphs:
        # 打印段落文本
        i = i.text.replace("\t", " ").strip()
        if i == "":
            continue

        paras += i

        if i.endswith("。") or i.endswith(".") or i.endswith("!") or i.endswith("?"):
            result.append(paras)
            paras = ""
    return result



#定义删除pdf链接的函数
def deletelink(filepath,save_file_path):
    pdf_document = fitz.open(filepath)

    # 遍历每一页
    for page in range(pdf_document.page_count):
        # 获取页面对象
        page_obj = pdf_document[page]

        # 遍历页面中的所有链接
        for link in page_obj.get_links():
            # 删除链接
            page_obj.delete_link(link)

    # 保存更改后的 PDF 文件
    return pdf_document.save(save_file_path)



# 定义以段落为单位分割文本的函数
def split_paragraphs(text):
    return text.split('\n\n')


# 文件上传
def uploadfile(request):
    # 获取上传对象
    my_file=request.FILES.get('file')
    ext = os.path.splitext(my_file.name)[1]  # 获取文件扩展名
    # 判断格式
    if ext not in ['.pdf','.doc','.docx']:
        return JsonResponse({"code":'9998',"message":"格式错误"})

    print(my_file)
    filename="./static/file/"+ my_file.name
    if my_file:
        with open(filename, 'wb+') as f:


            for chunk in my_file.chunks():
                f.write(chunk)
        #  如果是.doc或.docx文件，先将其转换为.pdf文件
        if ext in ['.doc','.docx']:
            convert(filename, "./static/file/output.pdf")
            pdffilename="./static/file/output.pdf"
            wordfilename=filename
        else:
            wordfilename="./static/file/output.docx"
            pdffilename="./static/file/output.pdf"

            #  删除PDF中的链接
            deletelink(filename,pdffilename)

            #  将PDF文件转换为.docx文件
            cv = Converter(pdffilename)
            cv.convert(wordfilename)  # 默认参数start=0, end=None
            cv.close()


        page_count = get_pdf_page_count(pdffilename)  # 获取页码数

        print(page_count)
        if page_count<=10:

            paragraphs = read_pdf(wordfilename)  # 获取文本内容
            print(paragraphs)
            # print(paragraphs)
            return JsonResponse({"code": '0000', "message": "成功", "data": {"page_count": page_count,"paragraphs":paragraphs}})

        return JsonResponse({"code":'0000',"message":"成功","data":{"page_count":page_count}})

