from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm
from django.template import loader
from cloudinary.forms import cl_init_js_callbacks
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            # If yes save it
            form.save()
            # Redirect Home
            return HttpResponseRedirect('/')
        else:

            #If NO show error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all()[:20]
    # Show
    return render(request, 'posts.html',
                {'posts': posts}
    )


def delete (request,post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect('/')    

def edit (request,post_id):
        post = Post.objects.get(id=post_id)
        if request.method == 'POST':
          form=PostForm(request.POST,request.FILES,instance = post)
          
          if form.is_valid():
             post.save()
             return HttpResponseRedirect('/')
          else:
            form=PostForm(PostForm)
        return render(request,'update_post.html',{'post':post})

def like(request, post_id):
    post = Post.objects.get(id=post_id)
    post.like += 1
    post.save()
    return HttpResponseRedirect('/')