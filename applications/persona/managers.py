from django.db import models
#
from django.db.models import Count


class ReunionManager(models.Manager):

    def cantidad_reuniones_job(self):
        resultado = self.values('persona__job').annotate( #Annotate es para agregar un campo que es donde conte los IDs.
            cantidad=Count('id')
        ) #Cuanto  cuantas reuniones tiene un trabajo
        print('**************')
        print(resultado)
        return resultado