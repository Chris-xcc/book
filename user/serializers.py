from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone'
        ]


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名', help_text='用户名', max_length=10,
                                     )

    password = serializers.CharField(
        label='密码', help_text='密码', write_only=True,
    )

    # 创建用户设置密码
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", 'password')