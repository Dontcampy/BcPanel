import src.dao.user as user

from flask_tokenauth import TokenAuth, TokenManager

from src.utils.load_config import config

token_manager = TokenManager(secret_key=config.SECRET_KEY)
token_auth = TokenAuth(secret_key=config.SECRET_KEY)


def get_token(username):
    """
    token生成器
    :param username: 用户名
    :return: token str
    """
    token = token_manager.generate(username, expiration=2592000)
    return token.decode()


def verify_normal(username, pwd):
    """
    普通账号验证
    :param username:
    :param pwd:
    :return:
    """
    data = user.select_username(username)
    if data is not None and data["pwd"] == pwd:
        return True
    else:
        return False


@token_auth.verify_token
def verify_t(token):
    """
    Token验证
    :param token:
    :return: username
    """
    return token_manager.verify(token)


def verify_arguments(ver_list, args):
    for x in ver_list:
        if args[x] is None:
            return False
    return True


def verify_perm(username):
    """
    权限验证
    :param username: 用户名
    :return:
    """
    return user.select_username(username)["admin"]
