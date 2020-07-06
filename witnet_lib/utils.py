class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


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
    url = url.trim()
    host, port = url.split(":")
    return host, int(port)
