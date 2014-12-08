from django.contrib import admin
from bars.models import *


class RepoAdmin(admin.ModelAdmin):
    list_display = ('url',)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'repo')

class CommitAdmin(admin.ModelAdmin):
    list_display = ('ssh', 'branch')

class RawAdmin(admin.ModelAdmin):
    list_display = ('owner', 'coverage', 'commit')

admin.site.register(Repo, RepoAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Raw, RawAdmin)
admin.site.register(Commit,CommitAdmin)