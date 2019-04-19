import datetime
import hashlib
import base64
import time
import hmac
import uuid
import json
import oss2
from flask.views import MethodView
from flask import jsonify
OSSConfig = {
    'OSS_TEST_ACCESS_KEY_ID': 'LTAIMlj4UXTdI427',
    'OSS_TEST_ACCESS_KEY_SECRET': 'eRNZsINDX46wI5AsXv9wCKMeJlzRAD',
    'OSS_TEST_BUCKET': 'ai-community',
    'OSS_TEST_ENDPOINT': 'oss-cn-beijing.aliyuncs.com',
    'OSS_HOST': 'ai-community.oss-cn-beijing.aliyuncs.com',
}

OSS_TEST_ACCESS_KEY_ID = OSSConfig.get('OSS_TEST_ACCESS_KEY_ID')
OSS_TEST_ACCESS_KEY_SECRET = OSSConfig.get('OSS_TEST_ACCESS_KEY_SECRET')
OSS_TEST_BUCKET = OSSConfig.get('OSS_TEST_BUCKET')
OSS_TEST_ENDPOINT = OSSConfig.get('OSS_TEST_ENDPOINT')
OSS_HOST = OSSConfig.get('OSS_HOST')



class AliOSS:
    def __init__(self):
        self.auth = oss2.Auth(OSS_TEST_ACCESS_KEY_ID, OSS_TEST_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, OSS_TEST_ENDPOINT, OSS_TEST_BUCKET)

    def get_uuid(self):
        uuid_str = uuid.uuid1()

        return uuid_str

    def get_dict_become_bytes(self, dict_data):
        '''字典转成base'''
        bytes_data = json.dumps(dict_data).encode('utf-8')
        return bytes_data

    def get_dict_become_base64(self, dict_data):
        '''字典转成base64'''
        bytes_data = json.dumps(dict_data).encode('utf-8')
        base64_data = base64.b64encode(bytes_data).decode('utf-8')

        return base64_data

    def download_file(self, oss_path, local_path):
        '''下载文件'''
        remote_stream = self.bucket.get_object_to_file(oss_path, local_path)

    def upload_img(self, oss_path, local_path, headers=None):
        '''上传图片'''
        result = self.bucket.put_object_from_file(oss_path, local_path, headers)
        return result

    def upload_file(self, oss_path, local_path, headers=None):
        '''普通上传文件'''
        result = self.bucket.put_object(oss_path, local_path, headers)
        return result

    def callback_headers(self):
        base64_callback_body = self.get_oss_callback()
        headers = {'x-oss-callback': base64_callback_body}
        return headers

    def convert_base64(self, input):
        return base64.b64encode(input)

    def get_sign_policy(self, key, policy):
        return base64.b64encode(hmac.new(key, policy, hashlib.sha1).digest())

    def get_expiration(self):
        expire_datetime = datetime.datetime.now() + datetime.timedelta(minutes=20)
        # expire_str = self.trans_datetime_str(expire_datetime)
        iso8086_str = self.trans_datetimestr_iso8601(expire_datetime)
        return iso8086_str

    # @property
    def get_policy_signature(self):
        '''获取政策和签名'''

        # 1 构建一个Post Policy
        policy = "{\"expiration\":\"%s\",\"conditions\":[[\"content-length-range\", 0, 1048576]]}" % self.get_expiration()
        policy = policy.encode('utf-8')

        # 2 将Policy字符串进行base64编码
        base64policy = self.convert_base64(policy)

        # 3 用OSS的AccessKeySecret对编码后的Policy进行签名
        signature = self.get_sign_policy(OSS_TEST_ACCESS_KEY_SECRET.encode('utf-8'), base64policy)

        data = {'base64policy': base64policy.decode('utf-8'), 'signature': signature.decode('utf-8')}

        return data

    def get_oss_callback(self):
        '''获取回调参数'''
        callback = {
            'callbackUrl': '',
            'callbackHost': 'oss-cn-beijing.aliyuncs.com',
            'callbackBody': 'bucket=${bucket}&object=${object}&etag=${etag}&size=${size}&mimeType=${mimeType}&imageInfo.height=${imageInfo.height}&imageInfo.width=${imageInfo.width}&imageInfo.format=${imageInfo.format}&my_var=${x:my_var}',
            'callbackBodyType': 'application/json',
        }
        bytes_callback = self.get_dict_become_bytes(callback)
        base64_callback = self.convert_base64(bytes_callback).decode('utf-8')

        return base64_callback

    def get_callbackbady(self):
        callbackbady = {

        }

    def response_oss_form_args(self):
        '''获取所有表单上传的参数'''
        param = {"accessid": OSS_TEST_ACCESS_KEY_ID,
                 "host": OSS_HOST,
                 "expire": self.get_expire_time(),
                 "callback": self.get_oss_callback(),
                 "dir": "user-dir"}

        param.update(**self.get_policy_signature())

        return param

    def trans_datetime_str(self, datetime_obj):
        '''datetime obj 转化为格式化时间字符串'''
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    def trans_str_type(self, datetime_str):
        '''格式化时间字符串转化为元祖'''
        return time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    def trans_type_stamp(self, time_type):
        '''时间元祖转化为时间戳'''
        return time.mktime(time_type)

    def trans_datetimestr_iso8601(self, datetime_str):
        return oss2.date_to_iso8601(datetime_str)

    def get_expire_time(self):
        expire_datetime = datetime.datetime.now() + datetime.timedelta(minutes=20)
        expire_str = self.trans_datetime_str(expire_datetime)
        expire_type = self.trans_str_type(expire_str)
        stamp = self.trans_type_stamp(expire_type)
        unix_time = int(stamp)
        return unix_time

    def get_files_list(self, prefix=None, delimiter=None):
        f = oss2.ObjectIterator(self.bucket, prefix=prefix, delimiter=delimiter)
        return [i.key for i in f]

    def delete_file(self, file_name):
        '''删除一个文件'''
        self.bucket.delete_object(file_name)

    def delete_many_file(self, file_name_list):
        '''删除多个文件'''
        self.bucket.batch_delete_objects(file_name_list)

    def copy_file(self, old_file_name, new_file_name, source_bucket_name=OSS_TEST_BUCKET, ):
        '''拷贝文件'''
        self.bucket.copy_object(source_bucket_name, old_file_name, new_file_name)

    def get_file_acl(self, file_name):
        '''查看文件的管理权限'''
        self.bucket.get_object_acl('file_name')

    def put_file_acl(self, file_name):
        '''修改文件管理权限'''
        self.bucket.put_object_acl(file_name, oss2.OBJECT_ACL_PUBLIC_READ)

    def put_file_meta(self):
        self.bucket.update_object_meta()


class GetDownloadParamView(MethodView):
    def __init__(self):
        self.ali_obj = AliOSS()
        super(GetDownloadParamView, self).__init__()

    def get(self):
        try:
            data = self.ali_obj.response_oss_form_args()

            code = 0
            msg = "success"
        except Exception as e:
            code = 1
            msg = str(e)
            data = []
        context = {'code': code, 'msg': msg, 'data': data}
        return jsonify(context)


class OSSCallbackView(MethodView):
    '''处理阿里OSS存储的回调请求'''
    # todo 处理阿里OSS存储的回调请求
    def post(self):
        return jsonify({})

