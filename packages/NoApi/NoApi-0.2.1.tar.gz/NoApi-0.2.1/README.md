NoApi (in beta)
===============

For when you want to have part of your program be executed on a different machine, and it would seem dumb to make a whole-ass API for literally every internal action.

With NoApi you can simply use objects and variables that exist on a remote machine as if they were working locally.


See what I mean
---------------

On the server:

    import noapi
    noapi.Server(port=1234, namespace=__import__(__file__)).start()
    
    some_object = SomeClass()


On the client:

    import noapi
    backend = noapi.Client(server_address='whatever ip', port=1234)
    
    print(backend.some_object.foo)
    backend.some_object.bar.some_method('args', 'work', 'too')


So you can use your remotely running backend just the same as if it was an imported package (here called 'backend')


Don't use this yet tho
----------------------

This library is still in active development and not polished, documented, or secure in the slightest. I'm testing how well it works by using it in another project I'm working on, and it's public in this phase only so that It's on PyPi and can easily be used with the other project.

So, use at your own risk!
