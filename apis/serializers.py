from store.models import Product, Category
from rest_framework import serializers
from accounts.models import Account

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'name', 'slug', 'created_at']
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class RegistertionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password'],
            country=validated_data.get('country', 'Egypt'),
            phone_number=validated_data.get('phone_number', None)
        )
        return user
        