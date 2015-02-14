from django.db import models


# describes change in a table: table[rowId, columnName] = value

class Transaction(models.Model):
    author = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=256)

    module = models.CharField(max_length=256)
    model = models.CharField(max_length=256)

    rowId = models.CharField(max_length=256)
    column = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    originalValue = models.CharField(max_length=256)