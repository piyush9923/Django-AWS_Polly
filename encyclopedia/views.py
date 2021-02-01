import random

from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import recordings
from . import util
import markdown2
from bs4 import BeautifulSoup


class NewPage(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='Description', widget=forms.Textarea(attrs={'cols': '60', 'style': 'height: 350px;'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def info(request, title):
    if title in util.list_entries():
        # try polly
        try:
            raw_html = markdown2.markdown(util.get_entry(title))
            query = recordings.objects.get(blog_name=title)
            print("no new model created")
        except:
            raw_html = markdown2.markdown(util.get_entry(title))
            new_str = "".join(BeautifulSoup(raw_html).findAll(text=True))
            path = util.generate_speech(title,new_str)
            print("new model created")
            query = recordings(blog_name=title)
            query.blog_audio.name = 'recordings/' + path['record_path'].split('/')[-1]
            query.save()
        return render(request, "encyclopedia/main.html", {
            "title": title,
            "text": raw_html,
            "file": query.blog_audio
        })
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        entry_list = util.list_entries()
        if query in entry_list:
            return render(request, "encyclopedia/search.html", {
                "content": markdown2.markdown(util.get_entry(query)),
            })
        else:
            final_list = [a for a in entry_list if query.lower() in a.lower()]
            return render(request, "encyclopedia/index.html", {
                "entries": final_list
            })

def create(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title in util.list_entries():
                raise Http404("Unable to Save! "+title+" already exists") #HttpResponse("Unable to Save! "+title+" already exists")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wikipedia:title", args=(title,)))

    return render(request, "encyclopedia/create.html", {
        "form": NewPage()
    })

def random_page(request):
    title = random.choice(util.list_entries())
    raw_html = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/main.html", {
        "title": title,
        "text": raw_html
    })


def edit(request, title):
    entry = util.get_entry(title)
    if entry:
        if request.method == 'POST':
            entry = request.POST.get('body').strip()
            if len(entry) > 10:
                util.save_entry(title, entry)
                return HttpResponseRedirect(reverse("wikipedia:title", args=(title,)))
            else:
                messages.error(request, f'New Entry Don\'t have enough characters!')
        return render(request, 'encyclopedia/edit.html', {'body': entry.strip(), 'title': title})
    else:
        raise Http404("Entry does not exist")
