class Functions(object):
    def __init__(self):
        self._funcs = {}

    def has(self, name, code_hash=None):
        if name in self._funcs:
            if code_hash is None:
                return True
            return code_hash in self._funcs[name]
        return False

    def get(self, name, code_hash):
        return self._funcs[name][code_hash]

    def put(self, func):
        self._funcs.setdefault(func.name, {})[func.code_hash] = func


functions = Functions()
