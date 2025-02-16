from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Tag, Quote
from .forms import TagForm, AuthorForm, QuoteForm


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})


def quote(request):
    tags = Tag.objects.all()
    author = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            choice_authors = author.filter(name__in=request.POST.getlist('author')).first()
            new_quote.author=choice_authors.id
            new_quote.save()

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, 'author': author, 'form': form})

    return render(request, 'quotesapp/quote.html', {"tags": tags, 'author': author, 'form': QuoteForm()})

def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote})
