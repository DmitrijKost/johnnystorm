from django.utils import timezone
from time import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
from models import *
from models import Commit as DBCommit, Actor as DBActor, File as DBFile
from forms import *
from git import *
import subprocess
from xml.etree import ElementTree
import os
import re

def index(request):
    template = 'code_coverage/index.html'
    context = {}
    return render(request, template, context)

#def selectorReps(request):


class IndexView(View, TemplateResponseMixin, FormMixin):
    template_name = "code_coverage/index.html"
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class DownloaderView(View, TemplateResponseMixin, FormMixin):
    template_name = "code_coverage/downloader.html"
    form_class = RepositoryForm

    def get_context_data(self, message, **kwargs):
        context = super(DownloaderView, self).get_context_data(**kwargs)
        context["message"] = message
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(message=None), **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        print('user')
        message = ''
        url = form.cleaned_data["url"]
        try:
            if Repository.objects.filter(url=url):
                r = Repository.objects.get(url=url)
                path = r.work_dir
                g = Git(path)
                g.execute('git push %s master' % r.url) #!!!IMPORTANT
                message = "Updated"
            else:
                path = "cache/%s" % "_".join(url.split('/')[2:])
                Repo.clone_from(url, path)
                r = Repository(url=url, work_dir=path)
                r.save()
            g = Git(path)
            repo = Repo(path)
            i=1
            for head in repo.heads:
                head.checkout()
                head_commit = head.commit
                branch_commits = []
                branch_commits.append(head_commit)
                for c in head_commit.iter_parents():
                    branch_commits.append(c)
                if not Branch.objects.filter(repository=r, name=head.name):
                    b = Branch(repository=r, name=head.name)
                    b.save()
                else:
                    b = Branch.objects.get(name=head.name,repository=r)
                for commit in branch_commits:
                    g.execute('git checkout %s' % commit.hexsha)
                    if not DBCommit.objects.filter(branch=b, sha=commit.hexsha):
                        if not DBActor.objects.filter(repository=r, actor_name=commit.author.name, actor_email=commit.author.email):
                            a = DBActor(repository=r, actor_name=commit.author.name, actor_email=commit.author.email)
                            a.save()
                        else:
                            a = DBActor.objects.get(repository=r, actor_name=commit.author.name, actor_email=commit.author.email)
                        c = DBCommit(branch=b, actor=a, committed_date=datetime.datetime.fromtimestamp(commit.committed_date).date(), sha=commit.hexsha, processed=False)
                        c.save()
                    else:
                        c = DBCommit.objects.get(branch=b, sha=commit.hexsha)
                        i += 1
                    message += str(commit)+'\n'+' commit '+str(i)
                    files = self.walk(g, commit)
                    if(files is None):
                        print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nfiles is None!!')
                        return self.render_to_response(self.get_context_data(message=message), **kwargs)
                    for file in files:
                        if not DBFile.objects.filter(commit=c, path_to_file=file):
                            f = DBFile(commit=c, path_to_file=file)
                            f.save()
                        else:
                            f = DBFile.objects.get(commit=c, path_to_file=file)
                        count = 0
                        cur_sha = ''
                        cur_num = ''
                        white_regex = re.compile('^\s*$')
                        for line in g.execute('git blame --line-porcelain %s' % file).split('\n'):
                            count = count + 1
                            if count == 1:
                                print line
                                cur_sha = line.split(' ')[0]
                                cur_num = line.split(' ')[2]
                            elif count == 13:
                                count = 0
                                if white_regex.match(line) is None:
                                    cur_com = DBCommit.objects.get(branch=b, sha=cur_sha)
                                    if not Line.objects.filter(file=f, actor=cur_com.actor, num=cur_num):
                                        l = Line(file=f, actor=cur_com.actor, num=cur_num)
                                        l.save()
            return HttpResponseRedirect('/coverage/selector/%s' % r.id)
        except GitCommandError:
            message = "Repository does not exist"
        except InvalidGitRepositoryError:
            message = "Invalid repository"
        return self.render_to_response(self.get_context_data(message=message), **kwargs)

    def form_invalid(self, form, **kwargs):
        return self.render_to_response(self.get_context_data(message="Wrong url!"), **kwargs)

    def walk(self, g, commit):
        try:
            pyfile = re.compile('.*\.py$')
            files = []
            for t in commit.tree.trees:
                self.walk(g, t)
            for b in commit.tree.blobs:
                if pyfile.match(str(b.abspath)):
                    files.append(b.abspath)
        except AttributeError:
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return None
        return files




class SelectorView(View, TemplateResponseMixin, FormMixin):
    template_name = 'code_coverage/selector.html'

    def get_context_data(self, **kwargs):
        context = super(SelectorView, self).get_context_data(**kwargs)
        context = kwargs
        return context

    def get(self, request, repo_id, *args, **kwargs):
        r = Repository.objects.get(id=repo_id)
        repo = Repo(r.work_dir)
        commits = []
        for head in repo.heads:
            commits.append({'commit': head.commit, 'head': head})
            for c in head.commit.iter_parents():
                commits.append({'commit': c, 'head': head})
        context = {'commits': commits, 'repo_id': repo_id}
        return self.render_to_response(self.get_context_data(**context), **kwargs)

    def post(self, request, repo_id, *args, **kwargs):
        r = Repository.objects.get(id=request.POST['repo_id'])
        path = r.work_dir
        repo = Repo(path)
        g = Git(path)
        files = []
        prev_test_file = ""
        for branch in repo.heads:
            b = Branch.objects.get(name=branch.name, repository=r)
            branch.checkout()
            head_commit = branch.commit
            branch_commits = []
            branch_commits.append(head_commit)
            for c in head_commit.iter_parents():
                branch_commits.append(c)
            for c in branch_commits:
                com = DBCommit.objects.get(branch=b, sha=c.hexsha)
                if c.hexsha in request.POST and request.POST[c.hexsha] != "":
                    test_file = request.POST[c.hexsha]
                    prev_test_file = test_file
                else:
                    test_file = prev_test_file
                g.execute('git checkout %s' % c.hexsha)
                try:
                    subprocess.call(['coverage', 'run', '{0}/{1}'.format(path, test_file)])
                    subprocess.call(['coverage', 'xml', '-o', '%s/coverage.xml' % path])
                    t = ElementTree.parse('%s/coverage.xml' % path)
                    cov = t.getroot()
                    for child in cov[0][0][0]:
                        files.append(c.hexsha + " : " + child.attrib["filename"] + " : " + child.attrib["line-rate"])
                        f = DBFile.objects.get(commit=com, path_to_file="C:\Users\Timur\PycharmProjects\code_analysis\%s" % "\\".join(child.attrib["filename"].split('/')))
                        for line in child[1]:
                            print str(f.id) + " : " + line.attrib["number"]
                            l = Line.objects.get(file=f, num=line.attrib["number"])
                            if line.attrib["hits"] == '1':
                                l.coverage = True
                                l.save()
                except Exception as ex:
                    files.append(c.hexsha + " : " + str(ex))
                subprocess.call(['coverage', 'erase'])
            try:
                os.remove('%s/coverage.xml' % path)
            except:
                pass
        context = {'files': files}
        return self.render_to_response(self.get_context_data(**context), **kwargs)


class RegisterView(View,TemplateResponseMixin,FormMixin):
    template_name = "code_coverage/register.html"
    def get_context_data(self,error,**kwargs):
        context = super(RegisterView,self).get_context_data(**kwargs)
        context["error_message"] = error
        return context
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return render(request, "code_coverage/register.html")
        else:
            return HttpResponseRedirect(reverse('index'))
    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        u = User.objects.filter(username=username)
        if u:
            return self.render_to_response(self.get_context_data(error="Choose another username"),**kwargs)
        u = User.objects.filter(email=email)
        if u:
            return self.render_to_response(self.get_context_data(error="Choose another email"),**kwargs)
        if (password != password2):
            return self.render_to_response(self.get_context_data(error="Passwords do not match"),**kwargs)
        u = User.objects.create_user(username=username, email=email, password=password)
        u.save()
        log = LoginView()
        return log.post(request=self.request)

class LoginView(View,TemplateResponseMixin,FormMixin):
    template_name = "code_coverage/login.html"
    def get_context_data(self,error,**kwargs):
        context = super(RegisterView,self).get_context_data(**kwargs)
        context["error_message"] = error
        return context
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            if request.GET.has_key("next"):
                print request.GET["next"]
                context = {'next': request.GET["next"]}
            else:
                context = {}
            return render(request, 'code_coverage/login.html', context)
        else:
            return HttpResponseRedirect(reverse('index'))
    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.has_key("next"):
                redirect_path = request.GET["next"]
            else:
                redirect_path = reverse('index')
            return HttpResponseRedirect(redirect_path)
        else:
            return HttpResponseRedirect(reverse('login'))

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('login'))
"""

def no_auth_please(v):
    def wrapper(request, *a, **k):
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        else:
            return v(request, *a, **k)
    return wrapper

@login_required(login_url=reverse_lazy("sign_in"))
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("sign_in"))


@login_required(login_url=reverse_lazy("sign_in"))
def q(request):
    return HttpResponse("CLASSIFIED")

@no_auth_please
def sign_in(request):
    if request.POST:
        f = LoginForm(request.POST)
        if f.is_valid():
            user = authenticate(
                                username=f.cleaned_data["username"],
                                password=f.cleaned_data["password"]
            )
            if user:
                login(request, user)
                if request.GET.has_key("next"):
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('sign_in'))
    else:
        f = LoginForm()
        context = {"f": f}
        if request.GET.has_key("next"):
            context["next"] = request.GET["next"]
        return render(request, "code_coverage/sign_in.html", context)
"""