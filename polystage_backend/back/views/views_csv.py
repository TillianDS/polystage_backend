from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from ..serializers import FileSerializer

class CsvEtudiant(APIView) :
    #parser_classes = [FileUploadParser]

    def post (self, request):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
           # once validated, grab the file from the request itself
        file = request.FILES['file']
        return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
