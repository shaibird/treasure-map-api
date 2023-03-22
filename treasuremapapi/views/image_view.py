from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers, status
from treasuremapapi.models import Image, Location, UserDetail
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
import base64
from django.core.files.base import ContentFile

class ImageSerializer(serializers.ModelSerializer):
    """JSON serializer for Images"""

    class Meta:
        model = Image
        fields = ('id', 'image', 'user', 'location', 'private')


class ImageView(viewsets.ModelViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single image
        
        Returns:
            Response -- JSON serialized image
        """

        try:
            image = Image.objects.get(pk=pk)
            serializer = ImageSerializer(image)
            return Response(serializer.data)
        except Image.DoesNotExist as ex:
            return Response({'message:': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all images
        
        Returns:
            Response -- JSON serialized list of images
        """
        location_id = request.query_params.get('location', None)

        if location_id is not None:
            try:
                images = Image.objects.filter(location=location_id)
            except Image.DoesNotExist:
                return Response({'error': 'Location ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST requests to /images
        Returns the created instance of image and a 201 status code
        """
        
        image = Image()
        image.user = request.auth.user
        image.location = Location.objects.get(pk=request.data['location'])
        image.private = request.data.get('private', False)
        image.date = request.data.get('date')

        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{image.id}-{uuid.uuid4()}.{ext}')
        image.image = data
        image.save()

        serialized = ImageSerializer(
            image, many=False, context={'request': request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)

