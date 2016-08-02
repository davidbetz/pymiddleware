import unittest

from middleware import Middleware, Handler

class AdditionMiddleware1(Middleware):
    def create(self):
        def func(mwa, context):
            try:
                counter = context['counter']
            except:
                counter = 0
            context['counter'] = counter + 1

            return next(mwa)

        return func


class AdditionMiddleware2(AdditionMiddleware1):
    pass


class AdditionMiddleware3(AdditionMiddleware2):
    pass


class TestBuilderCreator(unittest.TestCase):
    def test_chain(self):
        handler = Handler()
        handler.set([AdditionMiddleware1, AdditionMiddleware2])
        handler.add(AdditionMiddleware3)
        handler.execute()
        self.assertEquals(handler['counter'], 3)

    def test_init(self):
        handler = Handler(counter=1)
        handler.set([AdditionMiddleware1, AdditionMiddleware2])
        handler.add(AdditionMiddleware3)
        handler.execute()
        self.assertEquals(handler['counter'], 4)

    def test_hybrid(self):
        handler = Handler(counter=1)
        handler.set([AdditionMiddleware1, AdditionMiddleware2])
        handler.add(AdditionMiddleware3)
        def inline(wma, context):
            context['myvalue'] = 12
        handler.add(inline)
        handler.execute()
        self.assertEquals(handler['counter'], 4)
        self.assertEquals(handler['myvalue'], 12)

    def test_adhoc(self):
        handler = Handler()
        def inline(wma, context):
            context['myvalue'] = 12
        handler.add(inline)
        handler.execute()
        self.assertEquals(handler['myvalue'], 12)

    def test_kwargs(self):
        handler = Handler(**{'a': 1, 'b': 2})
        def inline(wma, context):
            context['a'] = context['a'] + context['b']
        handler.add(inline)
        handler.execute()
        self.assertEquals(handler['a'], 3)



if __name__ == '__main__':
    unittest.main()
