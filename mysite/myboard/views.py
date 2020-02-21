from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models
from . import apps

def page(request):
    datas = [{"id":1, "name":"홍길동1"},
             {"id":2, "name":"홍길동2"},
             {"id":3, "name":"홍길동3"},
             {"id":4, "name":"홍길동4"},
             {"id":5, "name":"홍길동5"},
             {"id":6, "name":"홍길동6"},
             {"id":7, "name":"홍길동7"},
             ]  

    page = request.GET.get("page", 1)    
    #(page-1)*3:page*3

    #첫번째 파라미터는 데이터, 두번째 파라미터는 한페이지에 보여줄 데이터의 개수
    p = Paginator(datas, 3)

    #전체 데이터 중 일부 데이터만 subs에 저장, p.page(1)은 123만, p.page(2)는 456만 보여주는것을 확인할 수 있다.    
    subs = p.page(page)

    #return render(request, "myboard/page.html", {"datas":datas})
    return render(request, "myboard/page.html", {"datas":subs})

def ajaxdel(request):
    pk = request.GET.get("pk")
#pk가 pk인 object를 찾는다.
    models.Board.objects.get(pk=pk)
    #board.delete()
    
    return JsonResponse({'error':'0'})

#모듈단위 검증은 shell이 좋다.
def ajaxget(request):
    page = request.GET.get("page", 1)
    datas = models.Board.objects.all().filter(category='common')
    page = int(page)
    subs = datas[(page-1)*3:(page)*3]
    
    #p = Paginator(datas, 3)
    #subs = p.page(page)

    datas = {'datas': [ {"pk":data.pk, "title":data.title, "cnt":data.cnt} for data in subs]}
    print(datas)

    return JsonResponse(datas)

class BoardView(View) :
    def get(self, request, category, pk, mode, page):
        if  mode == 'add' :
            form = forms.BoardForm()
        elif mode == 'list' :
            username = request.session["username"]
            user = User.objects.get(username=username)
            data = models.Board.objects.all().filter(category=category)
            #print(reverse('myboard', args=('common', 0, 'list')))

            page = request.GET.get("page", 1)    
            #(page-1)*3:page*3

            #첫번째 파라미터는 데이터, 두번째 파라미터는 한페이지에 보여줄 데이터의 개수
            p = Paginator(data, 3)

            #전체 데이터 중 일부 데이터만 subs에 저장, p.page(1)은 123만, p.page(2)는 456만 보여주는것을 확인할 수 있다.    
            subs = p.page(page)
            
            context = {"datas": subs, "username": username, "category": category}

            return render(request, apps.APP + "/list2.html", context)

        elif mode ==  "detail" :
            p = get_object_or_404(models.Board, pk=pk)
            p.cnt += 1
            p.save()
            return render(request, apps.APP +"/detail.html", {"d": p,"category":category})
        elif mode == "edit" :
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(instance=post)
        else :
            return HttpResponse("error page")

        return render(request, apps.APP +"/edit.html", {"form":form})

    def post(self, request, category, pk, mode):

        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
                post.category = category
            post.save()
            return redirect("myboard", category, 0, 'list')
        return render(request, apps.APP + "/edit.html", {"form": form})
'''
    def photolist(request):
        username = 'lee'
        sql = f"""select filename from myboard_image where username'{username}'"""

        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        context = dictfetchall(result)

        return render(request, 'myboard/photolist.html', context)

'''
########################################################################


                        #----제출할것----#


###########################이미지 업로드##############################

def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('myboard/photolist.html'))

