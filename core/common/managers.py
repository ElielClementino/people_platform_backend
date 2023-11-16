from django.db import models


class BaseModelManager(models.Manager):
    # Toda vez que um modelo que estiver usando esse manager for chamado, ele irá retornar apenas os dados conforme a query, no caso, que estão ativos
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)

    # Manager que retorna apenas dados que estão ativos
    objects = BaseModelManager()
    # Manager que retorna todos os dados, ativos ou inativos
    all_objects = models.Manager()

    # Faz com que o django não crie uma migração para esse modelo
    class Meta:
        abstract = True

    def _snake_case(self, name):
        return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

    def _get_related_models(self):
        related_models = []
        for field in self._meta.get_fields():
            if field.one_to_many and field.auto_created and isinstance(field, models.ManyToOneRel):
                related_models.append(field.related_model)
        return related_models


    def _soft_delete_cascading_models(self, related_models):
        if not related_models:
            return

        for model in related_models:
            field_name = self._snake_case(self._meta.model.__name__)

            filter_args = {f"{field_name}_id": self.pk, 'is_active': True}
            related_objects = model.objects.filter(**filter_args)

            for obj in related_objects:
                obj.is_active = False
                obj.save()

    def delete(self):
        related_models = self._get_related_models()
        self.is_active = False
        self.save()
        self._soft_delete_cascading_models(related_models=related_models)
