from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from django.core.paginator import Paginator
from .forms import BlogPost

def home(request) :
    blogs = Blog.objects
    # 블로그 객체 세 개를 한 페이지로 자르기
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    # request 된 페이지가 뭔지를 알아내고
    page = request.GET.get('page')
    # request 된 페이지를 얻어온 뒤 return 해준다.
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs' : blogs, 'posts' : posts})

def detail(request, blog_id) : 
    details = get_object_or_404(Blog, pk = blog_id)
    return render(request, "detail.html", {'detail' : details})

#new.html을 띄워주기만 함
def new(request) :
    return render(request, 'new.html')

#입력받은 내용을 DB에 넣어줌
def create(request) :
    blog = Blog() #블로그 객체 생성
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id)) #redirect : 위의 내용을 처리한 후 넘길 URL 페이지

def blogpost(request):
    #1. 입력된 내용 처리 -> request.POST
    #2. 빈페이지 -> request.GET

    if request.method == 'POST' :
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form' : form})


