from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    nivelAcceso = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='personas/')
    def __str__(self):
        return self.nombre
    
    def Validar_acceso(encoding):
        personas=Persona.objects.filter(autotizado=True)
        for persona in personas:
            if persona.encoding==encoding:
                return True
        return False
    
    def crear_persona(nombre, nivelAcceso, imagen):
        persona = Persona(nombre=nombre, nivelAcceso=nivelAcceso, imagen=imagen)
        persona.save()
        return persona  
    
    def eliminar_persona(id):
        try:
            persona = Persona.objects.get(id=id)
            persona.delete()
            return True
        except Persona.DoesNotExist:
            return False
        
    def actualizar_persona(id, nombre=None, nivelAcceso=None, imagen=None):
        try:
            persona = Persona.objects.get(id=id)
            if nombre is not None:
                persona.nombre = nombre
            if nivelAcceso is not None:
                persona.nivelAcceso = nivelAcceso
            if imagen is not None:
                persona.imagen = imagen
            persona.save()
            return persona
        except Persona.DoesNotExist:
            return None