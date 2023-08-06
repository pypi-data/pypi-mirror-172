from functools import partial, update_wrapper
from sanic import Sanic

class SanicRouter:
    '''
    路由器类
    '''

    def __init__(self, module):
        '''
        初始化。
        '''

        self.module = module
        self.actions = []

    def route(self, app: Sanic):
        '''
        添加路由到应用。
        '''

        for class_name, method_name, uri, args, kwargs in self.actions:
            if class_name != None:
                controller_class = getattr(self.module, class_name)
                controller = controller_class()
                method = getattr(controller_class, method_name)
                handler = partial(method, controller)
                update_wrapper(handler, method)
                app.add_route(handler, uri, *args, **kwargs)
            else:
                handler = getattr(self.module, method_name)
                app.add_route(handler, uri, *args, **kwargs)

    def append(
        self,
        class_name,  # 类名
        method_name,  # 方法名
        uri,  # 路由 URI
        args,  # 路由 数组参数
        kwargs  # 路由 键值参数
    ):
        '''
        存储路由参数。
        '''

        self.actions.append((
            class_name,
            method_name,
            uri,
            args,
            kwargs
        ))