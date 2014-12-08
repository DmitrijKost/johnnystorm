from bars.models import *
from rest_framework import serializers


class RawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raw
        fields = ('id', 'owner', 'coverage')


class CommitSerializer(serializers.ModelSerializer):
    raws = RawSerializer(many=True)
    class Meta:
        model = Commit
        fields = ('id', 'ssh', 'raws')




class BranchSerializer(serializers.ModelSerializer):
    commits = CommitSerializer(many=True)
    class Meta:
        model = Branch
        fields = ('id', 'name', 'commits')


class RepoSerializer(serializers.ModelSerializer):
    branchs = BranchSerializer(many=True)
    class Meta:
        model = Repo
        fields = ('id', 'url','branchs')


