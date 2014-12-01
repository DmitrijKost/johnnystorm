# coding: utf8
__author__ = 'oleg'

#TODO метод добавления репозитория,комита,блоба,строки в репозиторий
from models import *

def putRep(URL):
    repo=Repository(url=URL)
    repo.save()
    return repo

def putBranch(name,URL,repo=None):
    if(repo==None):
        repo=Repository.objects.get(url=URL)
    if(repo!=None&name!=None):
        branch=Branch(id_repo=repo,name=name)
        branch.save()
        return branch
    return None

def putCommit(ssh,nameBrench,branch=None):
    if(branch==None):
        #branch=Branch.objects.get(name=nameBrench)
        branch='head'
    if(ssh!=None&branch!=None):
        commit=Commit(id_branch=branch,ssh=ssh)
        commit.save()
        return commit
    return None

def putBlob(path,sshCom,commit=None):
    if(commit==None):
        commit=Commit.objects.get(ssh=sshCom)
    if(commit!=None&path!=None):
        blob=Blob(id_commit=commit,path_to_file=path)
        blob.save()
        return blob
    return None

def putLine(number,autor,pathBlob,sshCom,blob=None):
    if(blob==None):
        com=Commit.objects.get(ssh=sshCom)
        blob=Blob.objects.get(id=com,path_to_file=pathBlob)
    if(blob!=None&number!=None):
        if(autor==None):
            autor="Unknown programmer"
    line=Line(id_blob=blob,number=number,owner=autor)
    line.save()
    return putLine




