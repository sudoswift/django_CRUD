from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

nextId = 4

topics = [
    {'id': 1, 'title': 'Routing', 'body':'Routing is ...'},
    {'id': 2, 'title': 'View', 'body':'View is ...'},
    {'id': 3, 'title': 'Model', 'body':'Model is ...'},
]

def htmltemplate(articletag, id = None):
    global topics
    contextui =''
    if id != None:
        contextui = f'''
        <li>
        <form action ="/delete/" method = "POST">
            <input type="hidden" name ="id" value={id}>
            <input type ="submit" value ="DELETE">
        </form>
        </li>
        <li><a href ="/update/{id}">update</a></li>
        '''
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
    {contextui}
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
    return HttpResponse(htmltemplate(article, id))

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
    
@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newtopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newtopics.append(topic)
        topics = newtopics
        return redirect('/')
    

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectTitle= {
                    "title" : topic['title'],
                    "body" : topic['body']
                }
        article = f'''
        <form action ="/update/{id}/" method ="POST">
        <p><input type="text" name ="title" placeholder = "Title" value = {selectTitle["title"]}></p>
        <p><textarea name ="body" placeholder ="body">{selectTitle['body']}</textarea></p>
        <p><input type ="submit"></p>
        </form>
        '''
        return HttpResponse(htmltemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')
