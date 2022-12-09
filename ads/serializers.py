from datetime import date

from rest_framework import serializers

from ads.models import Users, Locations, Ads, Compilation, Category


class BirthDateValidator:
    date_today = date.today()

    def __init__(self, min_age):
        self.min_age = min_age[0]

    def __call__(self, value):
        if int(str(self.date_today - value).split()[0]) < self.min_age * 364:
            raise serializers.ValidationError(
                f'Минимальный возраст пользователя не должна быть меньше {self.min_age[0]} годам')


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
    birth_date = serializers.DateField(validators=[BirthDateValidator([9])])
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
            age=validated_data['age'],
            email=validated_data['email'],
            birth_date=validated_data['birth_date']
        )
        user.set_password(validated_data["password"])
        user.save()
        for location in self._locations:
            user_loc, _ = Locations.objects.get_or_create(name=location)
            user.location.add(user_loc)
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


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class CategoryDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']


class AdsListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='first_name',
    )
    category = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Ads
        exclude = ['logo']


class AdsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='first_name',
    )
    category = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Ads
        exclude = ['logo']


class AdsCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='first_name',
    )
    category = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Ads
        exclude = ['id', 'logo']

    def create(self, validated_data):
        ads = Ads(
            name=validated_data['name'],
            price=validated_data['price'],
            author=validated_data["author"],
            description=validated_data['description'],
            is_published=validated_data['is_published'],
            category=validated_data['category'])
        ads.save()
        return ads


class AdsUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        many=False,
        queryset=Users.objects.all(),
        slug_field='first_name',
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


class AdsDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']


class CompilationDetailSerializer(serializers.ModelSerializer):
    items = AdsDetailSerializer(many=True)

    class Meta:
        model = Compilation
        fields = "__all__"
