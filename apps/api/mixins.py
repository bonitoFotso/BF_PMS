from rest_framework import status
from rest_framework.response import Response


class HttpResponseMixin(object):
    @classmethod
    def success_response(self, status=status.HTTP_200_OK, message=None, data=None):
        return Response(
            headers={"status": status},
            data={
                "status": status,
                "message": message,
                "data": data if not data is None else {},
            },
            content_type="application/json",
        )

    @classmethod
    def error_response(
        self, status=status.HTTP_400_BAD_REQUEST, message=None, error=None
    ):
        return Response(
            status=status,
            data={
                "status": status,
                "message": message,
                "error": error if not error is None else {},
            },
            content_type="application/json",
        )
