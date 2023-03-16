from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from treasuremapapi.models import LayerName, LayerPin


class LayerView(ViewSet):
    """Location notes view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single location notes
        
        Returns:
            Response -- JSON serialized location notes"""

        layer_name = LayerName.objects.get(pk=pk)
        serializer = LayerNameSerializer(layer_name)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all blogs
        
        Returns:
            Response -- JSON serialized list of locations
        """

        layer_names = LayerName.objects.all()
        serializer = LayerNameSerializer(layer_names, many=True)
        return Response(serializer.data)

    def create(self, request):

        layer_names = LayerName()
        layer_names.user = request.auth.user
        layer_names.name = request.data['name']
        layer_names.save()

        serialized = LayerNameSerializer(layer_names, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     """Handle Put request for Notes
    #         Returns nothing"""


    #     layer_names = LayerName()
    #     layer_names.user = request.auth.user
    #     layer_names.name = request.data['name']
    #     layer_names.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle PUT requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        layer_names = LayerName.objects.get(pk=pk)
        layer_names.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class LayerNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayerName
        fields = ('name', 'user')