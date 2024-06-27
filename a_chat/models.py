from django.db import models
from django.contrib.auth.models import User
import shortuuid


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=120, unique=True, verbose_name="Nombre del grupo")
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
    body = models.CharField(max_length=300, verbose_name="Mensaje")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Mensaje de Grupo"
        verbose_name_plural = "Mensajes de Grupo"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author.username} : {self.body}"