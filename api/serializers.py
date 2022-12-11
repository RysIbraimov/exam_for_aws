from rest_framework import serializers

from .models import Category, Item


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=8)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.code = validated_data['code']
        instance.save()
        return instance


class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    price = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.category = validated_data['category']
        instance.save()
        return instance
