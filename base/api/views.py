from rest_framework.decorators import api_view
from rest_framework.response import Response
from .. import models

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = models.Room.objects.all()
    rooms_names = []
    for room in rooms:
        rooms_names.append(room.name)
    return Response(rooms_names)
