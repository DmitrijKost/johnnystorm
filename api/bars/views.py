from django.shortcuts import render
from rest_framework import generics
from bars.serializers import *


def home(request):
    return render(request, "index.html")

class RepoList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = Repo
    serializer_class = RepoSerializer

class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = Repo
    serializer_class = RepoSerializer


class BranchList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Branch
    serializer_class = BranchSerializer

class BranchDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Branch
    serializer_class = BranchSerializer


class CommitList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Commit
    serializer_class = CommitSerializer

class CommitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Commit
    serializer_class = CommitSerializer


class RawList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of groups.
    """
    model = Raw
    serializer_class = RawSerializer


class RawDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single group.
    """
    model = Raw
    serializer_class = RawSerializer