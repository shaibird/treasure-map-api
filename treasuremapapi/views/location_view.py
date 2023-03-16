from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from treasuremapapi.models import Location

class LocationView(ViewSet):
    """Locations View"""
    def retrieve(self, request, pk):
        """Handle GET requests for single location
        
        Returns:
            Response -- JSON serialized location
        """

        location = Location.objects.get(pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all blogs
        
        Returns:
            Response -- JSON serialized list of locations
        """

        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def create(self, request):

        location = Location()
        location.name = request.data['name']
        location.latitude = request.data['latitude']
        location.longitude = request.data['longitude']
        location.private = request.data['private']
        location.date = request.data['date']
        location.user = request.auth.user
        location.save()

        serialized = LocationSerializer(location, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for Location
        
        Returns:
            nothing
        """

        location = Location.objects.get(pk=pk)
        location.name = request.data['name']
        location.latitude = request.data['latitude']
        location.longitude = request.data['longitude']
        location.private = request.data['private']
        location.date = request.data['date']
        location.user = request.auth.user
    
    def destroy(self, request, pk=None):
        """Handle PUT requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        location = Location.objects.get(pk=pk)
        location.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude', 'private', 'date', 'user')