
class Cache:

    __cache_dict = {}

    def set(self, key, value):
        self.__cache_dict.update({key: value})

    def get(self, key):
        return self.__cache_dict.get(key)


cache_obj = Cache()
