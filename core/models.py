from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    id = None
    uuid = models.UUIDField(default=uuid4, primary_key=True, unique=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
