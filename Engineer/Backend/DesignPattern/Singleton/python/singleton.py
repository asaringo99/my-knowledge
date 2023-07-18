""" Singletonパターンの実装

"""

class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "singleton"):
            cls.singleton.__launch()
            cls.singleton = super(Singleton, cls).__new__(cls)
        return cls.singleton

    def __launch(cls):
        """サービスの中で1度だけ行いたい処理を書く"""
        pass

    def __init__(self):
        pass
