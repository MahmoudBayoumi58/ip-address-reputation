from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import IPListSerializer
from .tasks import get_ip_info
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class IPCheckView(APIView):
    def post(self, request):
        ip_list_serializer = IPListSerializer(data=request.data)
        if ip_list_serializer.is_valid():
            ips = ip_list_serializer.validated_data.get('ips', [])

            channel_layer = get_channel_layer()

            # Process each IP one by one as separate task and sent to Celery for scanning
            for ip in ips:
                get_ip_info.delay(ip)
                async_to_sync(channel_layer.group_send)(
                    'ip_check_group', {'type': 'ip_check', 'message': f'Checking IP: {ip}'}
                )
            return Response({'message': 'IPs are being processed'}, status=status.HTTP_202_ACCEPTED)

        return Response(ip_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
