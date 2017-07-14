# Middleware for Python

**Copyright (c) 2016 David Betz**

## Installation

    pip install middleware

[![Build Status](https://travis-ci.org/davidbetz/middleware.svg?branch=master)](https://travis-ci.org/davidbetz/middleware)
[![PyPI version](https://badge.fury.io/py/middleware.svg)](https://badge.fury.io/py/middleware)

## Compatibility

Python 2 and 3

## Purpose

Most everyone needs a concept of middleware.

Following are examples of using this, see ```test_middleware.py``` for full examples.

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

When using a class, add a ```create``` function which returns a function. This inner fuction accepts the middleware array and the data context and returns ```next(mwa)``` to create a middleware chain.

For this example, I'll add two more:

    class AdditionMiddleware2(AdditionMiddleware1):
        pass


    class AdditionMiddleware3(AdditionMiddleware2):
        pass

Now to run it. Use ```set``` to set an array of middleware and ```add``` to add one to the array. ```set``` overwrites everything. That's just what ```set``` means.

        handler = Handler()
        handler.set([AdditionMiddleware1, AdditionMiddleware2])
        handler.add(AdditionMiddleware3)
        handler.execute()

        # handler['counter'] == 3

In this case, there is no initial context and each of the three middleware increment a counter ending with ```handler['counter'] == 3```.

You can skip the entire class stuff too:

    handler = Handler()
    def inline(wma, context):
        context['myvalue'] = 12
    handler.add(inline)
    handler.execute()
    # handler['myvalue'] == 12
    
Use the following to send initial context:

    handler = Handler(counter=1)

It's actually ```kwargs```, so you can load it up:

    handler = Handler(**{'a': 1, 'b': 2})
    def inline(wma, context):
        context['a'] = context['a'] + context['b']
    handler.add(inline)
    handler.execute()
