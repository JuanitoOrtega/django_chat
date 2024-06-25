from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=120, unique=True, verbose_name="Nombre del grupo")

    class Meta:
        verbose_name = "Grupo de Chat"
        verbose_name_plural = "Grupos de Chat"

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