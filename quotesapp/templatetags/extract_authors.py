from django import template

register = template.Library()

def authors(author):
    return str(author.fullname)

register.filter('authors', authors)