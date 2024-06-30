from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import shortuuid
import os


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=120, unique=True, default=shortuuid.uuid, verbose_name="Nombre del grupo")
    groupchat_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Nombre del grupo")
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Administrador")
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True, verbose_name="Usuarios en línea")
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True, verbose_name="Miembros")
    is_private = models.BooleanField(default=False, verbose_name="Privado")

    class Meta:
        verbose_name = "Grupo de Chat"
        verbose_name_plural = "Grupos de Chat"

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = shortuuid.uuid()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="chat_messages", verbose_name="Grupo")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    body = models.CharField(max_length=300, blank=True, null=True, verbose_name="Mensaje")
    file = models.FileField(upload_to="files/", blank=True, null=True, verbose_name="Archivo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Mensaje de Grupo"
        verbose_name_plural = "Mensajes de Grupo"
        ordering = ["-created"]
    
    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None
    
    # @property
    # def is_image(self):
    #     if self.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
    #         return True
    #     else:
    #         return False

    @property
    def is_image(self):
        try:
            image = Image.open(self.file)
            image.verify()
            return True
        except:
            return False

    def __str__(self):
        if self.body:
            return f"{self.author.username} : {self.body}"
        elif self.file:
            return f"{self.author.username} : {self.filename}"