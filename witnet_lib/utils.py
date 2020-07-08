# class AttrDict(dict):
#     """
#     >>>o=AttrDict(**{"a":1,"b":{"c":1}})
#     >>>o.a
#     1
#     >>>o.b.c # errors
#     >>>o.b
#     {"c":1}
#     >>>a=AttrDict()
#     >>>a.update({"a":1})
#     >>>a.a
#     1

#     Args:
#         dict ([type]): [description]
#     """

#     def __init__(self, *args, **kwargs):
#         super(AttrDict, self).__init__(*args, **kwargs)
#         self.__dict__ = self


class AttrDict(object):
    """
    >>>o=AttrDict({"a":1,"b":[{"c":1}]})
    >>>o.a
    1
    >>o.b[0].c
    1

    Args:
        object (): inherits the object class
    """

    def __init__(self, d):
        """recursively converts dictionary to object

        Args:
            d (dictionary): object
        """
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [AttrDict(x) if isinstance(
                    x, dict) else x for x in b])
            else:
                setattr(self, a, AttrDict(b) if isinstance(b, dict) else b)


def resolve_url(url):
    """
    >>>resolve_url("127.0.0.1:21337")
    >>>"127.0.0.1", 21337

    >>>resolve_url("http://127.0.0.1:21337")
    >>>"127.0.0.1", 21337


    Args:
        url (string): {http,ws}://ip:port

    Returns:
        (string,int): ip, port
    """
    url = url.split("://")[-1]
    url = url.strip()
    host, port = url.split(":")
    return host, int(port)
