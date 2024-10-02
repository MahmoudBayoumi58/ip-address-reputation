from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from services.reputation_service import IPInfoAdapter


@shared_task
def get_ip_info(ip_address):
    ip_info_adapter = IPInfoAdapter()
    success, result = ip_info_adapter.get_ip_address_reputation(ip_address, 1)

    # Send result to the WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'ip_check_group',
        {
            'type': 'ip_scan_result',
            'message': {
                'info': f'Result for IP {ip_address}',
                'success': success,
                'result': result
            }
        }
    )

    return result
