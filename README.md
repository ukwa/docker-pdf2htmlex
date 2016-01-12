pdf2htmlEX in Docker
====================

A python web service that runs [pdf2htmlEX][1] on a URL.

Usage:

    $ docker run -ti -p 5000:5000 ukwa/pdf2htmlex

This runs an instance on port 5000 with a terminal connection so you can Ctrl-C to stop it.

Once running, you can use it as follows. To convert a whole PDF:

    $ curl http://localhost:5000/convert?url=http://stlab.adobe.com/wiki/images/d/d3/Test.pdf

There are also optional parameters: ```first_page``` (defaults to 1) and ```last_page```

TODO
----

* Suggest we switch to [nigit][2] and reduce the code we have to use.

[1]: http://coolwanglu.github.io/pdf2htmlEX/
[2]: https://github.com/lukasmartinelli/nigit
