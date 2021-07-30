import hashlib



# 创建获取token的对象
def get_token(username):

    strs = 'd3jf4hr'+username+'h2ur4gwi1b'
    hl = hashlib.md5()
    hl.update(strs.encode("utf8"))  # 指定编码格式，否则会报错
    token = hl.hexdigest()
    # print('MD5加密前为 ：', strs)
    # print('MD5加密后为 ：', token)
    return username+'.'+token


def check_token(token):
    username=token.split('.',1)[0]
    t=token.split('.',1)[1]
    check = get_token(username)

    if check.split('.',1)[1] == t:

        return True
    else:

        return False


if __name__ == '__main__':
    get_token('a')  # 调用token对象
    print(check_token('a',get_token('a')))