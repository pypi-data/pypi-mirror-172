from pkgutil import iter_modules
from importlib import import_module
from sanic import Sanic
from .router import SanicRouter

def attach(app: Sanic, module, deep=True):
    '''
    附加上路由
    '''

    # 如果传模块名则加载。
    if isinstance(module, str):
        module = import_module(module)

    # 加载路由。
    if hasattr(module, '___sanic_router___'):
        router = getattr(module, '___sanic_router___')
        router.route(app)

    # 是否深入解析。
    name = module.__name__
    if deep and module.__loader__.is_package(name):
        for _, child, _ in iter_modules(module.__path__):
            child_module_name = f'{name}.{child}'
            child_module = import_module(child_module_name)
            attach(app, child_module, deep)

def action(uri: str,  *args, **kwargs):
    '''
    路由信息设置。
    '''

    def decorator(method):
        '''
        装饰器。
        '''

        n = method.__name__
        qn = method.__qualname__
        cn = qn[:-len(n) - 1] if qn != n else None
        module_name = method.__module__
        m = import_module(module_name)
        if not hasattr(m, '___sanic_router___'):
            setattr(m, '___sanic_router___', SanicRouter(m))
        m.___sanic_router___.append(cn, n, uri, args, kwargs)
        return method
    return decorator


def http_any(uri: str, *args, **kwargs):
    '''
    接受所有方法类型。
    '''

    kwargs['methods'] = [
        'HEAD',
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'PATCH',
    ]
    return action(uri, *args, **kwargs)


def http_get(uri: str,  *args, **kwargs):
    '''
    接受 GET 请求。
    '''

    kwargs['methods'] = ['GET']
    return action(uri, *args, **kwargs)


def http_put(uri: str,  *args, **kwargs):
    '''
    接受 PUT 请求。
    '''

    kwargs['methods'] = ['PUT']
    return action(uri, *args, **kwargs)


def http_delete(uri: str,  *args, **kwargs):
    '''
    接受 DELETE 请求。
    '''

    kwargs['methods'] = ['DELETE']
    return action(uri, *args, **kwargs)


def http_post(uri: str,  *args, **kwargs):
    '''
    接受 POST 请求。
    '''

    kwargs['methods'] = ['POST']
    return action(uri, *args, **kwargs)

def http_prefix(prefix: str):
    '''
    TODO
    给控制器添加前缀。
    '''