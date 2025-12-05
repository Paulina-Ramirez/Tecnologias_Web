from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

# Serializer de Administrador 
class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

# Serializer de Alumnos 
class AlumnoSerializer(serializers.ModelSerializer): 
    user=UserSerializer(read_only=True)
    class Meta: 
        model = Alumnos 
        fields = '__all__'

# Serializer de Maestros 
class MaestroSerializer(serializers.ModelSerializer): 
    user=UserSerializer(read_only=True)
    class Meta: 
        model = Maestros 
        fields = '__all__'

# Serializer de Materias
# En serializers.py, actualiza MateriaSerializer
class MateriaSerializer(serializers.ModelSerializer):
    profesor_nombre = serializers.SerializerMethodField()
    profesor_id = serializers.SerializerMethodField()
    dias_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Materias
        fields = ['id', 'nrc', 'nombre', 'seccion', 'dias', 'hora_inicio', 'hora_fin', 
                  'salon', 'programa_educativo', 'profesor', 'creditos', 'creation', 
                  'update', 'profesor_nombre', 'profesor_id', 'dias_list']
    
    def get_profesor_nombre(self, obj):
        if obj.profesor and obj.profesor.user:
            return f"{obj.profesor.user.first_name} {obj.profesor.user.last_name}"
        return None
    
    def get_profesor_id(self, obj):
        if obj.profesor:
            return obj.profesor.id
        return None
    
    def get_dias_list(self, obj):
        if obj.dias:
            try:
                import json
                return json.loads(obj.dias)
            except:
                return obj.dias.split(',') if obj.dias else []
        return []