from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from treasuremapapi.models import Location, LocationNote
from treasuremapapi.views import LocationSerializer

class LocationNoteView(ViewSet):
    """Location notes view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single location notes
        
        Returns:
            Response -- JSON serialized location notes"""

        location_notes = LocationNote.objects.get(pk=pk)
        serializer = LocationNotesSerializer(location_notes)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all location_notes
        
        Returns:
            Response -- JSON serialized list of location_notes"""
        try:
            user = request.auth.user
            location_id = request.query_params.get('location_id')
            if location_id:
                location_notes = LocationNote.objects.filter(location=location_id, user=user)
            else:
                location_notes = LocationNote.objects.filter(user=user)
            serialized = LocationNotesSerializer(location_notes, many=True)
            return Response(serialized.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):

        location_notes = LocationNote()
        location_notes.location = Location.objects.get(pk=request.data['location'])
        location_notes.user = request.auth.user
        location_notes.date = request.data['date']
        location_notes.note = request.data['note']
        location_notes.private = request.data['private']
        location_notes.save()

        serialized = LocationNotesSerializer(location_notes, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class LocationNotesSerializer(serializers.ModelSerializer):
    location = LocationSerializer

    class Meta:
        model = LocationNote
        fields = ('id', 'user', 'note', 'private', 'date', 'location')