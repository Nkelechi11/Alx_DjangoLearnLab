from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by("is_read", "-timestamp")

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.filter(
            pk=pk,
            recipient=request.user
        ).first()

        if not notification:
            return Response(
                {"detail": "Notification not found."},
                status=404
            )

        notification.is_read = True
        notification.save()

        return Response({"detail": "Notification marked as read."})
    
