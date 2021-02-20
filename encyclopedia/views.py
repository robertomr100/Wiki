from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from markdown2 import Markdown
import logging
import random
logger = logging.getLogger("mylogger")

class NewSearchForm(forms.Form):
    query = forms.CharField(label="query")

class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    textvalue = forms.CharField(label="textvalue",widget=forms.Textarea)

markdowner = Markdown()


def index(request):
    entries = util.list_entries()
    upperEntries = [x.upper() for x in entries]
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query.upper() in upperEntries:
                logger.info(upperEntries)
                return render(request,"encyclopedia/entry.html",{
                    "entryName":query,
                    "entry": markdowner.convert(util.get_entry(query))
                 })
            else:
                result = [i for i in upperEntries if query.upper() in i] 
                logger.info(result)
                return render(request, "encyclopedia/index.html", {
                    "entries": result
                })

            return render(request, "encyclopedia/index.html", {
                "entries": query
            })
           
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })

def entry(request,entryName):
    entryRequest= util.get_entry(entryName)
    if entryRequest is None:
        return render(request,"encyclopedia/error.html",{
        "error": "<h1>ERROR</h1> <h3>"+entryName+" page not found</h3>"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
        "entryName":entryName,
        "entry": markdowner.convert(entryRequest)
        })

def add(request):
    entries = util.list_entries()
    upperEntries = [x.upper() for x in entries]
    if request.method == "POST":
        form= NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textvalue = form.cleaned_data["textvalue"]
            if title.upper() in upperEntries:
                return render(request,"encyclopedia/adderror.html")
            util.save_entry(title,textvalue)
            print(title)
            print(textvalue)
            return HttpResponseRedirect(reverse("entry",args=[title]))
    return render(request,"encyclopedia/add.html",{
        "form":NewPageForm()
    })

def randomPage(request):
    entries = util.list_entries()
    randEntry = random.choice(entries)
    entryRequest= util.get_entry(randEntry)
    return render(request,"encyclopedia/entry.html",{
        "entryName":randEntry,
        "entry": markdowner.convert(entryRequest)
     })

def edit(request,entryName):
    if request.method == "POST":
        print("POOOOOST")
        form= NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textvalue = form.cleaned_data["textvalue"]
            print(textvalue)
            util.save_entry(title,textvalue)
            return HttpResponseRedirect(reverse("entry",args=[title]))

    entryRequest= util.get_entry(entryName)
    return render(request,"encyclopedia/edit.html",{
        "entryName":entryName,
        "form":NewPageForm(initial={'title':entryName, 'textvalue':entryRequest})
    })
