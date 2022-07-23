from email import message
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project,Tag
from .forms import Project, ProjectForm,ReviewForm
from django.db.models import Q
from .utils import  searchProjects, paginateProjects



'''def project(request,pk):
    return HttpResponse("helloooo"+' '+str(pk)) '''  

'''projectList = [
    {
        'id':"1",
        'title':"Ecommerce website",
        'description':'Fully functional ecommerce website'
    },
    {
        'id':"2",
        'title':"Portfolio website",
        'description':'Fully functional portfolio website'
    },
    {
        'id':"3",
        'title':"Social website",
        'description':'Fully functional social website'
    }
]'''

def projects(request):
    projects,search_query = searchProjects(request)
    custom_range,projects = paginateProjects(request,projects,3)
    

    return render(request,'projects/projects.html',{'projects':projects,'search_query':search_query,'custom_range':custom_range})

def project(request, pk):
    
    projectObj= Project.objects.get(id=pk)
    
    form=ReviewForm()
    if request.method == 'POST':
        form= ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount
        #update project votecount
        messages.success(request,'Your review has been successfully submitted')
        return redirect('project',pk=projectObj.id)
    
    tags = projectObj.tags.all()
    '''for i in projectList:
        if i['id']== pk:
            projectObj=i'''

    return render(request,'projects/single-project.html',{'project':projectObj,'tags':tags,'form':form} )
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        form= ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project= form.save(commit=False)
            project.owner= profile
            project.save()
            return redirect('account')

    context ={'form': form,'project':project}
    return render (request,"projects/project_form.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
         
        form= ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project=form.save()
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)   
                project.tags.add(tag)
            return redirect('account')

    context ={'form': form,'project':project} 
    return render (request,"projects/project_form.html",context)    

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request,'projects/delete.template.html',context)