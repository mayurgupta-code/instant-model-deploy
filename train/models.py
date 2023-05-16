from django.db import models

# Create your models here.

def user_rawdata_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/raw_data/{1}'.format(instance.user.id, filename)


class UploadedData(models.Model):
    name = models.CharField(max_length=100)
    data_file = models.FileField(upload_to=user_rawdata_directory_path, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)