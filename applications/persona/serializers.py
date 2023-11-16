#
from rest_framework import serializers, pagination
#
from .models import Person, Reunion, Hobby


class PersonSerializer(serializers.ModelSerializer):

    def create(self, validated_data): #Este es un create personalizado, en este caso puede funcionar sin el.
        print('Create', 'Personalizado')
        hobbies = validated_data['hobbies']
        print('Hobby', hobbies)

        person = Person.objects.create(
            full_name=validated_data['full_name'],
            job=validated_data['job'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )
        person.hobbies.set(hobbies)
        return person
    class Meta:
        model = Person
        fields = ('__all__')


class PersonaSerializer(serializers.Serializer): #Serializador Geneeruci.
    full_name = serializers.CharField()
    id = serializers.IntegerField()
    job = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    #
    activo = serializers.BooleanField(default=False)
    #activo = serializers.BooleanField(required=False)


class PersonaSerializer2(serializers.ModelSerializer):

    activo = serializers.BooleanField(default=False) #Sera un campo nuevo

    class Meta:
        model = Person
        fields = ('__all__')



class ReunionSerializer(serializers.ModelSerializer):

    persona = PersonSerializer()

    class Meta:
        model = Reunion
        fields = ( #Campos que quiero serializar
            'id', #literal solo apareceran estos campos
            'fecha',
            'hora',
            'asunto',
            'persona', #persona es un campo foraneo
        )


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('__all__')


class PersonaSerializer3(serializers.ModelSerializer):

    #hobbies = HobbySerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'id',
            'full_name',
            'job',
            'email',
            'phone',
            'hobbies',
            'created',
        )


class ReunionSerializer2(serializers.ModelSerializer):

    fecha_hora = serializers.SerializerMethodField()

    class Meta:
        model = Reunion
        fields = (
            'id',
            'fecha',
            'hora',
            'asunto',
            'persona',
            'fecha_hora',
        )
    
    def get_fecha_hora(self, obj):
        return str(obj.fecha) + ' - ' + str(obj.hora)



class ReunionSerializerLink(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reunion
        fields = (
            'id',
            'fecha',
            'hora',
            'asunto',
            'persona',
        )
        extra_kwargs = { #Variable del HyperlinkedModelSerializer
            'persona': {'view_name': 'persona_app:detalle', 'lookup_field': 'pk'}
        }


class PersonPagination(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 100


class CountReunionSerializer(serializers.Serializer):
    persona__job = serializers.CharField()
    cantidad = serializers.IntegerField()