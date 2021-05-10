from django.db import models
from django.conf import settings 

class Photo(models.Model):

    class Meta:
        db_table    = "photo"

    file        = models.ImageField(verbose_name="画像ファイル",upload_to="photo/",default="photo/default.png")
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)


class Document(models.Model):

    class Meta:
        db_table    = "document"

    file        = models.FileField(verbose_name="ファイル",upload_to="file/document/")
    mime        = models.TextField(verbose_name="MIMEタイプ")
    thumbnail   = models.ImageField(verbose_name="サムネイル",upload_to="file/thumbnail/",null=True)
