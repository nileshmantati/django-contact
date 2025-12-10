from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib import messages
from .models import Contact ,Registration

# Create your views here.
def login(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Registration.objects.get(email=email, password=password)
            # Here SessionStore 
            request.session['email'] = user.email    
            messages.success(request, "Login Successful")
            return redirect('home') 
        except Registration.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login') 
    return render(request,'loginpage.html')

def registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
        if Registration.objects.filter(email=email).exists():
            print("error:exits")
            messages.error(request, "Email Already Registered!")
            return render(request, 'registrationpage.html')
        
        if password != confirm_password:
            print("error:password")
            messages.error(request, "Passwords do not match!!")
            return render(request,'registrationpage.html')
            
        Registration.objects.create(
            name=name,
            email=email,
            phone=phone,
            password = password,
        )
        messages.success(request, "Registration Successfully!")
        return redirect('login')
    return render(request,'registrationpage.html')

def home(request,pk=None):
    if 'email' not in request.session:
        return redirect('login')
    
    user = Registration.objects.get(email=request.session['email'])
    contact = None
    if pk:
        contact = get_object_or_404(Contact, pk=pk)
        
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        image = request.FILES.get('image')

        # Update Contact if exits
        if contact:
            contact.name = name
            contact.email = email
            contact.phone = phone
            contact.address = address

            if image:
                contact.image = image

            contact.save()
            messages.success(request, "Contact Updated!")
            return redirect('contact')

        # Create new contact if does not exits
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            user = user
        )
        messages.success(request, "Contact Added!")
        return redirect('contact')

    return render(request, 'home.html', {
        "data": contact,
        "title": "Edit Contact" if pk else "Add Contact",
        "btn": "Update Contact" if pk else "Save Contact"
    })


def contact(request):
    if 'email' not in request.session:
        return redirect('login')
    user = Registration.objects.get(email=request.session['email'])
    alldata = Contact.objects.filter(user=user)
    context = {
        'alldata':alldata
    }
    return render(request, 'contactall.html',context)

def getsingledata(request,pk):
    data = get_object_or_404(Contact,pk=pk)
    context={
        'data':data
    }
    return render(request,'contactsingle.html',context)

def delete_contact(request,pk):
    if 'email' not in request.session:
        return redirect('login')
    contact = get_object_or_404(Contact,pk=pk)
    contact.delete()
    messages.success(request, "Contact deleted!")
    return redirect('contact')

def edit_contact(request,pk):
    if 'email' not in request.session:
        return redirect('login')
    contact = get_object_or_404(Contact, pk=pk)

    return render(request,'home.html',{
        "title": "Edit Contact",
        "btn" : "Update Contact",
        "data" : contact,
    })
    
def update_status(request,pk):
    if 'email' not in request.session:
        return redirect('login')
    contact =  get_object_or_404(Contact,pk=pk)
    if contact.status == True:
        contact.status = False
    else:
        contact.status = True
    contact.save()
    messages.success(request, "Contact Status Updated!")
    return redirect('contact')

def logout(request):
    # del request.session['email']
    messages.success(request, "Logout Successfully!")
    request.session.flush()  # ye sare session ko delete kar deta hai
    return redirect('login')