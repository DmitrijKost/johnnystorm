import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from bars.serializers import *


def home(request):
    return render(request, "index.html")

def branch(request):
    example = {"commits": [{"date": "2014.12.13.21.43", "branch": "master", "coverage": 69},
                {"date": "2014.12.14.21.50", "branch": "master", "coverage": 77},
                {"date": "2014.12.15.11.50", "branch": "api", "coverage": 40},
                {"date": "2014.12.15.21.50", "branch": "test", "coverage": 90},
                {"date": "2014.12.16.21.50", "branch": "master", "coverage": 73}]}
    return HttpResponse(json.dumps(example), content_type="application/json")


class Example(View):
    def index(request):
        return render(request, 'index.html')


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