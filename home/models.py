from django.db import models

# Create your models here.
# ML model store model
# name: name of the model
# description: description of the model
# model: the model file
# created_at: the time when the model is created
# updated_at: the time when the model is updated
# accuracy: the accuracy of the model

class MLModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    # model_file = models.FileField(upload_to='models/')
    accuracy = models.FloatField(default=0.0)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



# ML model input store model
# name: name of the model input
# attribute: the attribute of the input
# description: description of the model input
# input_type: the type of the input
# model: the model that the input belongs to
# created_at: the time when the model input is created
# updated_at: the time when the model input is updated

class MLModelInput(models.Model):
    INPUT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('file', 'File'),
        ('image', 'Image'),
    )
    name = models.CharField(max_length=100)
    attribute = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, null=True, blank=True)
    input_type = models.CharField(max_length=100)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name