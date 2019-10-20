

def deco(func):
    from core import src
    def wrapper(*args,**kwargs):
        if src.user_info['user']:
            res = func(*args,**kwargs)
            return res
        else:
            print('请先登录')
            src.login()
    return  wrapper