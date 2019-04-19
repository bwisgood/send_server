import os
import requests
from urllib import parse
from .alioss import AliOSS

from xpinyin import Pinyin

p = Pinyin()


class DocReplace(object):
    """
    doc文本替换
    """

    def __init__(self, f_path, to_path):
        """
        :param f_path: 需要操作的文件路径
        :param to_path: 转换后要生成文件的路径
        :param replace_dict: 转换的字典{"{{id}}":1,"{{name}}":白维}
        """

        if f_path == to_path:
            raise FileExistsError("目标文件不能与源文件重复")

        self.f_path = f_path
        self.to_path = to_path

    def replace(self, context):
        from docxtpl import DocxTemplate

        doc = DocxTemplate(self.f_path)
        # context = {'name': "World company", "address": "你好"}
        doc.render(context=context)
        filename = p.get_initials(self.to_path.split("/")[-1], "")

        self.to_path = self.to_path.split("/")[0:-1]
        self.to_path.extend([filename])

        self.to_path = "/".join(self.to_path)
        print(self.to_path)
        doc.save(self.to_path)

    def upload(self):
        with open(self.to_path, "rb") as file_obj:
            file_name = p.get_initials(self.to_path.split("/")[-1], "")
            print("filename:", file_name)
            file_path = "letter/" + file_name
            ali = AliOSS()
            result = ali.upload_file(file_path, file_obj)
            print("=" * 100)
            print(result)
            print("=" * 100)
            # file_url = 'https://ai-community.oss-cn-beijing.aliyuncs.com/' + file_path

            after_trans_name = file_name[:file_name.index(".")] + ".pdf"
            data = {
                'file_url':
                    'https://ai-community.oss-cn-beijing.aliyuncs.com/trans_pdf_temp/' + parse.quote(after_trans_name),
                'file_name': after_trans_name
            }
            print(data)
            params = {"src": p.get_initials(file_name, "")}

            resp = requests.get(url="http://127.0.0.1:5000/trans", params=params)
            print(resp.url)
            return data


if __name__ == '__main__':
    old_filepath = os.path.dirname(os.path.dirname(__file__)) + "/static/律师函.docx"
    to_path = os.path.dirname(__file__) + "/1.docx"

    print(old_filepath)
    print(to_path)

    d = DocReplace(old_filepath, to_path=to_path)

    replace_dict = {
        "#业主姓名#": "白维",
        "#楼号#": "100号",
        "#律所地址#": "建外soho东区B座"
    }

    d.replace(replace_dict)
