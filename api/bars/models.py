from django.db import models


class Repo(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=20)
    repo = models.ForeignKey(Repo, related_name='branchs')

    def __unicode__(self):
        return self.name


class Commit(models.Model):
    ssh = models.CharField(max_length=8)
    branch = models.ForeignKey(Branch, related_name='commits')
    def __unicode__(self):
        return self.ssh


class Raw(models.Model):
    owner = models.CharField(max_length=20)
    coverage = models.BooleanField()
    commit = models.ForeignKey(Commit, related_name='raws')
    def __unicode__(self):
        return self.id