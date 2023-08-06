from threading import Thread as BaseThread


class Thread:  # 将线程封装，更容易使用
    class Wrapper:
        def __init__(self, func):
            self.func = func
            self.res = None

        def __call__(self, *args, **kwargs):
            self.res = self.func(*args, **kwargs)

    def __init__(self, func, *args, **kwargs):
        self.wrapper = self.Wrapper(func)
        self._thread = BaseThread(target=self.wrapper, args=args, kwargs=kwargs)
        self.running = False

    @property
    def res(self):
        """
        线程的返回值
        :return:
        """
        return self.wrapper.res

    @property
    def done(self):
        """
        线程任务结束否
        :return:
        """
        return not self._thread.is_alive()

    def start(self):
        if not self.running:
            self._thread.start()
            self.running = True


__all__ = ['Thread']
