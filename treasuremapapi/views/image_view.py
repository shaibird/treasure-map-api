from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers, status
from treasuremapapi.models import Image, Location
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from django.core.files.uploadedfile import InMemoryUploadedFile

class ImageSerializer(serializers.ModelSerializer):
    """JSON serializer for Images"""

    class Meta:
        model = Image
        fields = ('id', 'image', 'user', 'location', 'private')


class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)


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

        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized photo instance"""

        # Check if an image file was included in the request
        if 'image' not in request.data:
            return Response({'error': 'Image file is missing from request'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the image file data from the request
        image_file = request.data['image']

        # Wrap the image file data in an InMemoryUploadedFile object
        image_data = InMemoryUploadedFile(image_file, None, image_file.name, 'image/jpeg', image_file.size, None)

        # Replace the 'image' value in the request data with the InMemoryUploadedFile object
        request.data['image'] = image_data

        # Create a new ImageSerializer with the updated request data
        Image_serializer = ImageSerializer(data=request.data)

        if Image_serializer.is_valid():
            Image_serializer.save()
            return Response(Image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', Image_serializer.errors)
            return Response(Image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

