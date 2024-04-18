from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from apps.chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from apps.chat.models import ChatRoom, ChatMessage
from rest_framework.permissions import *
from django.db.models import Q,F, Count


class HandleUnexpectedCall(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomView(APIView):
    
	# authentication_classes = [JWTAuthentication]
	# permission_classes = [IsAuthenticated]
    
	def get(self, request, userId):
		chatRooms = ChatRoom.objects.filter(member=userId)
		# chatRooms = ChatRoom.objects.annotate(num_member=Count('member')).filter(Q(member=userId) & Q(num_member__gt=1))
		serializer = ChatRoomSerializer(
			chatRooms, many=True, context={"request": request}
		)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = ChatRoomSerializer(
			data=request.data, context={"request": request}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesView(ListAPIView):
	serializer_class = ChatMessageSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		roomId = self.kwargs['roomId']
		return ChatMessage.objects.\
			filter(chat__roomId=roomId).order_by('-timestamp')