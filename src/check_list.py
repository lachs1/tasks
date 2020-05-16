class CheckList(object):
    def __init__(self, name: str, description: str, cid: int = None):
        self._name = name
        self._description = description
        self._cid = cid

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def cid(self) -> int:
        return self._cid
