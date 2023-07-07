from urllib import parse

from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    page_size_query_param = "limit"
    max_page_size = 100

    def encode_cursor(self, cursor):
        url = super().encode_cursor(cursor)
        queries = parse.parse_qs(parse.urlparse(url).query)
        cursor = queries.get("cursor", [None])[0]

        return cursor
