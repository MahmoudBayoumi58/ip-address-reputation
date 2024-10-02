from rest_framework import serializers


class IPListSerializer(serializers.Serializer):
    ips = serializers.ListField(
        child=serializers.IPAddressField(protocol='both', required=True),
        allow_empty=False,
        required=True
    )
