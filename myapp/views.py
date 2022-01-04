from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

nextId = 4

topics = [
    {'id': 1, 'title': 'Routing', 'body':'Routing is ...'},
    {'id': 2, 'title': 'View', 'body':'View is ...'},
    {'id': 3, 'title': 'Model', 'body':'Model is ...'},
]

def htmltemplate(articletag):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return (f'''
<html>
<body>
<h1><a href="/">Django<a/></h1>
<ul>
    {ol}
</ul>
    {articletag}
    <ul>
    <li><a href="/create/">CREATE</a></li>
    </ul>
</body>
</html>
''')

def index(request):
    article = '''
    <h2>Welcom</h2>
    Hello Django!
    '''
    return HttpResponse(htmltemplate(article))
    
def read(request, id):
    global topics
    article =''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(htmltemplate(article))

@csrf_exempt
def create(request):
    global nextId
    if request.method == 'GET':
        article = '''
        <form action ="/create/" method ="POST">
        <p><input type="text" name ="title" placeholder = "Title"></p>
        <p><textarea name ="body" placeholder ="body"></textarea></p>
        <p><input type ="submit"></p>
        </form>
        '''
        return HttpResponse(htmltemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newtopic = {"id": nextId, "title": title, "body": body}
        topics.append(newtopic)
        url = '/read/' + str(nextId)
        nextId += 1
        return redirect(url)
    

