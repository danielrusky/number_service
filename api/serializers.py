from rest_framework import serializers

from users.models import User, Referrals


class ReferralSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    phone = serializers.CharField(source='user.phone')
    invite_code = serializers.CharField(source='user.invite_code')

    class Meta:
        model = Referrals
        fields = (
            'id',
            'phone',
            'invite_code',
        )


class UserSerializer(serializers.ModelSerializer):
    referrals = ReferralSerializer(source='referrals_author', many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'invite_code',
            'referrals',
        )
