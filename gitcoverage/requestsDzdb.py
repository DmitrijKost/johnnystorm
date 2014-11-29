__author__ = 'oleg'

#TODO метод добавления репозитория,комита,блоба,строки в репозиторий
from models import *

def putRep(URL):
    repo=Repository(url=URL)
    repo.save()
    return repo

def putBranch(name,URL):
    repo=Repository.objects.get(url=URL)
    branch=Branch(id_repo=repo,name=name)
    branch.save()
    return branch

def putCommit(ssh,nameBrench):
    branch=Branch.objects.get(name=nameBrench)
    commit=Commit(id_branch=branch,ssh=ssh)
    commit.save()
    return commit

def putBlob(path,sshCom):
    com=Commit.objects.get(ssh=sshCom)
    blob=Blob(id_commit=com,path_to_file=path)
    blob.save()
    return blob

def putLine(pathBlob,sshCom,number,autor):
    com=Commit.objects.get(ssh=sshCom)
    blob=Blob.objects.get(id=com,path_to_file=pathBlob)
    line=Line(id_blob=blob,number=number,owner=autor)
    line.save()
    return putLine




