from django.shortcuts import render,redirect
from client.models import client_data,client_info,clientdocument
import qrcode
import datetime
from io import BytesIO
from django.core.files import File
from client.utils import render_to_pdf

def index(request):
    return render(request,"index.html")

# Create your views here.
def base(request):
    
    return render(request,'base.html')
def signup(request): 
    return render(request,'signup.html')
def clientregister(request):
    if request.method == "POST":
       

        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        photo=request.FILES['photo']
        client_obj=client_data(username=username,email=email,password=password,photo=photo)
        error_msg=validateclient(client_obj)
        if not error_msg:
             client_obj.save()
             return redirect("adminchk")
        else:
             return render(request,"signup.html",{'error1':error_msg})
        
             
        
    return render(request,"signup.html")
def validateclient(client_obj):
     error_msg=None
     email=client_data.objects.filter(email=client_obj.email)

     if email:
          error_msg="Email Already exist"
     return error_msg    
def adminchk(request):
        return render(request,"adminchk.html") 
def clientlogin(request):
        if request.method=="POST":
            email=request.POST.get("email")
            password=request.POST.get("pswd")
            try:
                 client_obj=client_data.objects.get(email=email)
            except:
                 error_msg="THIS IS WRANGG!!!!!"
                 return render(request,'signup.html',{'error':error_msg})
            data={'client_obj':client_obj}
            if client_obj and client_obj.status == 1:
                      if(password==client_obj.password):
                           request.session['id']=client_obj.id
                           request.session['name']=client_obj.username
                           return render(request,"clienthome.html",data)
        return render(request,"signup.html") 
def clienthome(request):
     return render(request,"clienthome.html")
def clientdata(request):
         if request.method=="GET":
                  
            return render(request,"registration.html")
            
         else:
            name=request.POST.get("name")
            email=request.POST.get("email")
            address=request.POST.get("address")
            district=request.POST.get("district")
            phone=request.POST.get("phone")
            city=request.POST.get("city")
            aadhar=request.POST.get("aadhar")
            dob=request.POST.get("dob")
            obj=client_info(address=address,phone=phone,district=district,city=city,aadhar=aadhar,dob=dob,client=client_data(request.session['id']))
            obj.save()
            #qrcode
            document=clientdocument(client=client_info(obj.id))
            clientobj=client_data.objects.get(id=request.session['id']) 
            today_date=datetime.date.today()
            name=clientobj.username
            email=clientobj.email
            img=qrcode.make("QR Code Created Date:%s \n\n Name:'%s' \n\n Email Address:'%s' \n\n Contact NO:'%s' \n\n DOB:'%s' \n\n Address:'%s'  \n\n City:'%s'  \n\n AAdhar No:'%s' "
                            %(str(today_date),str(name),str(email),str(phone),str(dob),str(address),str(city),str(aadhar)))
           
            
            imgfile="img%s.jpg"%(obj.id)
            img.save(imgfile)
            buffer=BytesIO()
            img.save(buffer,'PNG')
            document.qrdata.save(imgfile,File(buffer))
            global pdf
            pdf=render_to_pdf(obj.id,'certificate.html',{'clientobj':clientobj,'obj':obj})
          #document=clientdocument(Client=clientinfo(obj.id))
            global filename
            filename="doc%s.pdf"%(obj.id)
            document.pdfdata.save(filename,File(BytesIO(pdf.content)))
            document.save()

            return render(request,"result.html",{'document':document})
def logoutclient(request):
     request.session.clear()
     return redirect('/')

    