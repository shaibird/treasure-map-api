from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from treasuremapapi.models import LayerName, LayerPin, Location
from treasuremapapi.views import LocationSerializer

class LayerPinView(ViewSet):
    """View for retrieving LayerPin instances associated with a specific LayerName"""

class LayerPinView(ViewSet):
    """View for retrieving LayerPin instances associated with a specific LayerName"""

    def list(self, request):
        """Handle GET requests to get all LayerPin instances associated with a specific LayerName"""
        layer_name = request.query_params.get('layername', None)
        if layer_name is not None:
            try:
                layer = LayerName.objects.get(name=layer_name)
            except LayerName.DoesNotExist:
                return Response(f"No layer with name {layer_name} exists.", status=status.HTTP_404_NOT_FOUND)

            layer_pins = LayerPin.objects.filter(layer=layer)
            serializer = LayerPinSerializer(layer_pins, many=True)
            return Response(serializer.data)
        else:
            layer_pins = LayerPin.objects.all()
            serializer = LayerPinSerializer(layer_pins, many=True)
            return Response(serializer.data)


    def create(self, request):
        layer_pin = LayerPin()
        layer_pin.layer = LayerName.objects.get(pk=request.data['layer'])
        layer_pin.location = Location.objects.get(pk=request.data['location'])
        layer_pin.save()

        serialized = LayerPinSerializer(layer_pin, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle PUT requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        layer_pin = LayerPin.objects.get(pk=pk)
        layer_pin.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """Handle GET requests for single location notes
        
        Returns:
            Response -- JSON serialized location notes"""

        layer_pin = LayerPin.objects.get(pk=pk)
        serializer = LayerPinSerializer(layer_pin)
        return Response(serializer.data)

class LayerPinSerializer(serializers.ModelSerializer):
    location = LocationSerializer
     
    class Meta:
        model = LayerPin
        fields = ('id', 'layer', 'location')
        