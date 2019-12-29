import urllib.request


class BaseService:

    def send_url_request(url):
        def request_generator(old_function):
            def new_function(*args, **kwds):
                try:
                    formatUrl = url.format(old_function(*args, **kwds))
                    print(formatUrl)

                    uf = urllib.request.urlopen(formatUrl)
                    return uf.read()
                except:
                    print(formatUrl)
                    err = "Error while reading url: {0}".format(formatUrl)

            return new_function

        return request_generator
