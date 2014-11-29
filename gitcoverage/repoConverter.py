# coding: utf8
import requestsDzdb

__author__ = 'oleg'

from git import *

import os

pathToAllRepositories="D:/develop/python/cod/testgit/"


TestRepo=Repo.clone(Repo("D:/develop/python/cod/testgit/clonefnts"),"D:/develop/python/cod/testgit/clonefnts2")

#метод получения всех файлов в репозитории определенного коммита в входных данных полный путь до репозитория
def dowloadRep(url,nameRep,dirReps=pathToAllRepositories):
    if(nameRep in os.listdir(dirReps)):
        nameRep=createNewName(dirReps,nameRep)
    repo = Repo.clone_from(url,dirReps+nameRep)
    modRep=requestsDzdb.putRep(nameRep,url)
    return repo

#Вспомагательный метод для dowloadRepAndUse запускается, когда в проекте уже лежит репозиторий с таким именем
#Предположительно будет использоваться при многопоточном обработке репозиториев или если возникла
#ошибка выполнения транзакции и скачанный репозитори не был удален
def createNewName(dir,name):
    i=2
    name=name+'('+i+')'
    while(name in os.listdir(dir)):
        name=name[:-2]
        i+=1
        name=name+i+')'
    return name

#Данный метод будет запускать обработку репозитория по переданным ему именам(хеш) коммитов:
#TODO атрибут repo
def obrRepByCommit(dir,listCommits,repo=TestRepo):
    #Какая-нибудь валидация listCommits
    for commit in listCommits:
        #TODO добавить commit в бд
        dirCom=makeDirCommit(dir,commit)
        #TODO метод который будет воссоздавать репозиторий на момент когда в репозитории данный коммит являлся хедом
        #TODO пока вместо верхнего делаем так. затем метод убрать, когда верхний будет готов
        Repo.clone(repo,dirCom)

        walk(dirCom,commit)

    #TODO все ли коммиты из листа были обработаны и соотвествующие действия при отрицательном ответе

#Создание рабочей области(папки) для обработки определенного коммита
def makeDirCommit(dir,commit):
    dirCom=dir+"/workplace/"+commit
    os.makedirs(dirCom)
    return dirCom

#метод который обходит репозиторий, который находится в том состояние в котором он был,
#при коммите переданным ему в аргументах.
def walk(dir,commit="Unknown"):
    if(commit=="Unknown"):
        return "Exception: Unknown commit in atribytes"
    #TODO проверка на наличие коммита в бд
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            print path
            #TODO cложить файл в бд
            #TODO запустить метод обработки данного файла
        else:
            walk(path)


#прочий код для теста модуля. Если за этим комментарием окажется код в рабочем варианте, поощряется надавать по голове
#разработчик(у\ам) этого модуля,руки желательно не трогать им ещё это исправлять.
walk("D:/develop/python/cod/testgit/fnts")
dowloadRep("https://bitbucket.org/thegoodguysteam/mister-fantastic/get/435fceb5611f.zip","mistrer fantastic")