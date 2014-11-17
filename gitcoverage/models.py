from django.db import models

class User(models.Model):
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Repository(models.Model):
    url = models.CharField(max_length=140)

class Branch(models.Model):
    id_repo = models.ForeignKey(Repository)
    name = models.CharField(max_length=40)
    
class Commit(models.Model):
    id_branch = models.ForeignKey(Branch)
    ssh = models.CharField(max_length=40)

class Blob(models.Model):
    id_commit = models.ForeignKey(Commit)
    path_to_file = models.CharField(max_length=120)
    
class Line(models.Model):
    id_blob = models.ForeignKey(Blob)
    owner = models.CharField(max_length=60)
    coverage = models.BooleanField()
