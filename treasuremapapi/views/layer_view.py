from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from treasuremapapi.models import LayerName, LayerPin
from treasuremapapi.views import LocationSerializer


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
        layer_name = request.query_params.get('layername')
        user_id = request.query_params.get('user')
        
        if layer_name is not None:
            try:
                layer = LayerName.objects.get(name=layer_name)
            except LayerName.DoesNotExist:
                return Response({'error': 'Layer not found'}, status=status.HTTP_404_NOT_FOUND)

            pins = None
            if user_id is not None:
                pins = LayerPin.objects.filter(layer=layer, user=user_id)
            else:
                pins = LayerPin.objects.filter(layer=layer)
            
            serializer = LayerPinSerializer(pins, many=True)
            return Response(serializer.data)
        
        elif user_id is not None:
            pins = LayerName.objects.filter(user=user_id)
            serializer = LayerNameSerializer(pins, many=True)
            return Response(serializer.data)
        
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
class LayerPinSerializer(serializers.ModelSerializer):
    location = LocationSerializer
     
    class Meta:
        model = LayerPin
        fields = ('id', 'layer', 'location')
        
class LayerNameSerializer(serializers.ModelSerializer):
    pins = LayerPinSerializer(many=True, read_only=True)

    class Meta:
        model = LayerName
        fields = ('id', 'name', 'user', 'pins')