from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser,FileUploadParser,MultiPartParser
import io
from .serializers import UserSerializer,LoginuserSerializer,FileSerializer
from django.http import FileResponse
from random import randint
from FileSystem import settings
from django.core.mail import send_mail

def indexPage(Request):
    return render(Request,"index.html")

@login_required(login_url="/login/")
@csrf_exempt
def UploadFiles(Request):
    if Request.method=="POST":
        a=userDetail.objects.get(username=Request.user.username).staff
        if a :
            stream=io.BytesIO(Request.body)
            pythondata=FileUploadParser().parse(stream,parser_context={"request":Request})
            print(pythondata)
            serialize=FileSerializer(data=pythondata.files)
            print(pythondata.files)
            if serialize.is_valid():
                content_disposition = Request.headers.get('Content-Disposition', '')
                filename = content_disposition.split('filename=')[1].strip('"') if 'filename=' in content_disposition else None
                print(filename)
                b=filename[-4::]
                if b=="pptx" or b=="docx" or b=="xlsx":
                    serialize.save()
                    return HttpResponse(JSONRenderer().render({"Status":"Success","Result":"File Uploaded"}),content_type="application/json")
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"File IS Not Valid"}),content_type="application/json")
            else:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Data Is Not Valid"}),content_type="application/json")
        else:
            return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Acess Denied"}),content_type="application/json")
    else:
            return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Not Valid Request"}),content_type="application/json")

@csrf_exempt
def loginPage(Request):
    if Request.method=="POST":
        stream=io.BytesIO(Request.body)
        pythondata=JSONParser().parse(stream)
        serialize=LoginuserSerializer(data=pythondata)
        if(serialize.is_valid()):
            try:
                print("imran",pythondata)
                a=userDetail.objects.get(username=pythondata["username"])
            except:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Record Not Found"}),content_type="application/json")
            user=authenticate(username=pythondata["username"],password=pythondata["password"])
            if(user is not None):
                login(Request,user)
                return HttpResponse(JSONRenderer().render({"Status":"Success","Result":"Loged In"}),content_type="application/json")
            else:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Record Not Found"}),content_type="application/json")
    return HttpResponse(JSONRenderer().render({"Status":"Failed"}),content_type="application/json")

@login_required(login_url="/login/")
def listFile(Request):
    if Request.method=="GET":
        a=userDetail.objects.get(username=Request.user.username).staff
        if a is False:
            file=Files.objects.all()
            doc={}
            for i in file:
                doc[str(i.id)]=str(i.file)[8::]
            return HttpResponse(JSONRenderer().render(doc),content_type="application/json")
        else:
            return HttpResponse(JSONRenderer().render({"Status":"Failed"}),content_type="application/json")
    else:
        return HttpResponse(JSONRenderer().render({"Status":"Failed"}),content_type="application/json")
    
@login_required(login_url="/login/")
def logout1(Request):
    logout(Request)
    return HttpResponse(JSONRenderer().render({"Status":"Success","Result":"Logout "}),content_type="application/json")

@login_required(login_url="/login/")
def download(Request,id):
    if Request.method=="GET":
        a=userDetail.objects.get(username=Request.user.username).staff
        if a is False:
            try:
                files_obj=Files.objects.get(id=id)
                return HttpResponse(JSONRenderer().render({"Download-link":f"http://localhost:8000/downloading-file-request/{id}/","Message":"Sucesss"}),content_type="application/json")
            except:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"File Not Found"}),content_type="application/json")
    return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Acess Denied"}),content_type="application/json")
    
@login_required(login_url="/login/")
def downloadFile(Request,id):
    if Request.method=="GET":
        a=userDetail.objects.get(username=Request.user.username).staff
        if a is False:
            try:
                files_obj=Files.objects.get(id=id)
                name=str(files_obj.file)[8::]
            except:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"File Not Found"}),content_type="application/json")
            file_path=files_obj.file.path
            files=FileResponse(open(file_path,"rb"))
            files["Content-Disposittion"]=f'attachment; filename="{name}"'
            return files
        else:
            return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Acess Denied"}),content_type="application/json")
    else:
        return HttpResponse(JSONRenderer().render({"Status":"Failed"}),content_type="application/json")
    
@csrf_exempt
def verifyEmail(Request,code):
    try:
        pythondata=Request.session["data"]
    except:
         return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Not Valid"}),content_type="application/json")
    if code==pythondata["code"]:
        employeeSerializer=UserSerializer(data=pythondata)
        if employeeSerializer.is_valid():
            employeeSerializer.save()
            del Request.session["data"]
            return HttpResponse(JSONRenderer().render({"Status":"Success","Result":"validated"}),content_type="application/json")
    return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Not Authenticated"}),content_type="application/json") 

@csrf_exempt
def sigupPage(Request):
    if Request.method=="POST":
        stream=io.BytesIO(Request.body)
        pythondata=JSONParser().parse(stream)
        employeeSerializer=UserSerializer(data=pythondata)
        if employeeSerializer.is_valid():
            try:
                code=randint(100000,999999)
                pythondata["code"]=code
                Request.session["data"]=pythondata
                Request.session.set_expiry(60*60)
                url="http://localhost:8000/verify/"+str(code)+"/"
                subject = 'Email Verification'
                message ="""Hello """+ url +""",\n"""+""" CLick The Link to Validate The Account"""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [pythondata["email"]]
                send_mail( subject, message, email_from, recipient_list)
                return HttpResponse(JSONRenderer().render({"Status":"Success","Result":"Email Sended "}),content_type="application/json")
            except:
                return HttpResponse(JSONRenderer().render({"Status":"Failed","Result":"Username is Already Exits"}),content_type="application/json")
    return HttpResponse(JSONRenderer().render({"Status":"Failed"}),content_type="application/json")