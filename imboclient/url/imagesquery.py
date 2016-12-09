class Query:
    def __init__(self):
        self._page = 1
        self._limit = 20
        self._metadata = False
        self._query = None
        self._q_from = None
        self._q_to = None

    def q_to(self, q_to=None):
        if not q_to:
            return self._q_to

        self._q_to = q_to
        return self

    def q_from(self, q_from=None):
        if not q_from:
            return self._q_from

        self._q_from = q_from
        return self

    def query(self, query=None):
        if not query:
            return self._query

        self._query = query
        return self

    def metadata(self, metadata=None):
        if metadata is None:
            return self._metadata

        self._metadata = metadata
        return self

    def limit(self, limit=None):
        if not limit:
            return self._limit

        self._limit = limit
        return self

    def page(self, page=None):
        if not page:
            return self._page

        self._page = page
        return self

