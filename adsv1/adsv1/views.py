from django.db.models import fields
from django.http import HttpResponse
from django.http import request
from django.views import generic
from .models import Comment, Pic
from django.views import View
from django.urls import reverse_lazy
from .forms import CommentForm, CreateForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('all')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class PicListView(generic.ListView):
    model = Pic
    context_object_name = 'pics'

    
class PicCreateView(View):
    template_name = 'adsv1/pic_form.html'
    success_url = reverse_lazy('ads_all')

    def get(self, req, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(req, self.template_name, ctx)

    def post(self, req, pk=None):
        form = CreateForm(req.POST, req.FILES or None)
        
        if not form.is_valid():
            ctx = {'form': form}
            return render(req, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)


class AdDetailView(generic.DetailView):
    model = Pic
    context_object = 'pic'
    template_name = 'adsv1/pic_detail.html'

    def get(self, request, pk):
        pic = get_object_or_404(Pic, id=pk)
        comments = Comment.objects.filter(ad_id=pk).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'pic': pic, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)


class CommentCreateView(View):

    def post(self, request, pk):
        ad = get_object_or_404(Pic, id=pk)
        form = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        form.save()
        return redirect('ad_detail', pk)
        

class CommentDeleteView(generic.edit.DeleteView):
    model = Comment

    def get_success_url(self):
        ad = self.object.ad
        return reverse_lazy('ad_detail', kwargs={'pk': ad.id})


class AdUpdateView(generic.edit.UpdateView):
    model = Pic
    fields = ['title', 'text', 'price', 'picture']
    template_name = 'adsv1/pic_form.html'

    def get(self, request, pk):
        pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form':form}
        return render(request, self.template_name,  ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        pic = form.save(commit=False)
        pic.save()

        return redirect('ads_all')



class AdDeleteView(generic.edit.DeleteView):
    model = Pic
    success_url = reverse_lazy('ads_all')


def stream_file(req, pk):
    pic = get_object_or_404(Pic, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response