from collections.abc import MutableMapping


class DataDict(MutableMapping):
    """A container object that works like a dict.

    Attributes
    ----------
    data : dict
        Store the data for this container object.
    """

    def __init__(self):
        self.data: dict = {}

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value):
        self.data[key] = value

    def __delitem__(self, key: str):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"
