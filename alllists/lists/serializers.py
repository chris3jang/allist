from rest_framework import serializers
from lists.models import Item

class ItemSerializer(serializers.ModelSerializer):
	#title = serializers.CharField(required=False, allow_blank=True, max_length=255)

	class Meta:
		model = Item
		fields = ('item_title', 'children', 'order_number')

	def create(self, validated_data):
		return Item.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.save()
		return instance
