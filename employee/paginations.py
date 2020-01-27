from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class SmallPagesPagination(pagination.LimitOffsetPagination):
    limit_query_param = 'starts'

    def get_paginated_response(self, data, request):
        return Response(OrderedDict([
            ("draw", int(request.POST.get("draw"))),
            ('recordsTotal', self.count),
            ('recordsFiltered', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_limit(self, request):
        start = int(request.POST.get('length'))
        if self.limit_query_param:
            try:
                return _positive_int(
                    start,
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

    def get_offset(self, request):
        try:
            return _positive_int(
                int(request.POST.get('start')),
            )
        except (KeyError, ValueError):
            return 0
