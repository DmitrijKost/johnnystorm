from django.db import models
from django.contrib.auth.models import *


class Repository (models.Model):
    url = models.CharField(max_length=256)
    work_dir = models.CharField(max_length=256)


class Actor(models.Model):
    repository = models.ForeignKey(Repository)
    actor_name = models.CharField(max_length=128)
    actor_email = models.CharField(max_length=128)


class Branch(models.Model):
    repository = models.ForeignKey(Repository)
    name = models.CharField(max_length=64)


class Commit(models.Model):
    branch = models.ForeignKey(Branch)
    actor = models.ForeignKey(Actor)
    committed_date = models.DateField()
    sha = models.CharField(max_length=64)
    processed = models.BooleanField(default=0)


class File(models.Model):
    commit = models.ForeignKey(Commit)
    path_to_file = models.CharField(max_length=256)


class Line(models.Model):
    file = models.ForeignKey(File)
    actor = models.ForeignKey(Actor)
    num = models.IntegerField()
    coverage = models.BooleanField(default=0)