from rest_framework import serializers

from ads.models import Users, Locations, Ads, Compilation, Category


class AdsUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='username',
    )
    category = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Ads
        exclude = ['id']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class AdsDeDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['id']


class AdsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='username',
    )
    category = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Ads
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        exclude = ['id']

    def is_valid(self, *, raise_exception=False):
        qd = self.initial_data.copy()
        self._locations = qd.pop('location')
        self.initial_data = qd
        valid_result = super().is_valid(raise_exception=raise_exception)
        qd.update({'location': self._locations})
        self.initial_data = qd
        return valid_result

    def create(self, validated_data):
        user = Users(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            role=validated_data['role'],
            age=validated_data['age']
        )
        user.set_password(validated_data["password"])
        user.save()
        for location in self._locations:
            user_loc, _ = Locations.objects.get_or_create(name=location)
            user.location.add(user_loc)
            user.save()
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Locations.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Users
        exclude = ['id']

    def is_valid(self, *, raise_exception=False):
        qd = self.initial_data.copy()
        self._locations = qd.pop('location') if qd['location'] else None
        self.initial_data = qd
        valid_result = super().is_valid(raise_exception=raise_exception)
        qd.update({'location': self._locations})
        self.initial_data = qd
        return valid_result

    def save(self):
        user = super().save()

        for location in self._locations:
            user_loc, _ = Locations.objects.get_or_create(name=location)
            user.location.add(user_loc)
        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id"]


class CompilationListSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Compilation
        fields = "__all__"


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class CompilationDetailSerializer(serializers.ModelSerializer):
    items = AdsDetailSerializer(many=True)

    class Meta:
        model = Compilation
        fields = "__all__"


class CompilationCreateSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Ads.objects.all(),
        slug_field='id',
    )

    class Meta:
        model = Compilation
        fields = ['owner', 'name', 'items']

    def create(self, validated_data):
        compilation = Compilation(
            name=validated_data['name'],
            owner=validated_data['owner'])

        compilation.save()
        for item in validated_data['items']:
            print(item.pk)
            item_ad = Ads.objects.get(pk=item.pk).pk
            compilation.items.add(item_ad)
            compilation.save()
        compilation.save()
        return compilation


class CompilationUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ['name', 'items']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        for item in validated_data.get('items', instance.name):
            item_ad = Ads.objects.get(pk=item.pk).pk
            instance.items.add(item_ad)
            instance.save()
        instance.save()
        return instance


class CompilationDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id"]
