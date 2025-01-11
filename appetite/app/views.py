from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import logout as logouts
from django.shortcuts import render, redirect
from .models import register, surplus_food_supplier, supplier_surplus_food, delivery_agent, surplus_requests, \
    complaints, feedbacks
from .forms import registerform, Loginform, addDeliveryAgentForm, Editadminprofileform, Edituserform, editsurplusform, \
    Addsurplusform, supplierregform, Editsupplierregform, replyComplaintForm, createComplaintForm,replyfeedbackForm,givefeedbackForm
from django.contrib import messages
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta,date
from datetime import datetime




def index(request):
    return render(request, "main/index.html")


def register_func(request,uid):
    if request.method == 'POST':
        form = registerform(request.POST,request.FILES)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            if User.objects.filter(email=post_email).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/register/%s' % uid)
            else:
                form.save()
                uname = register.objects.get(email=post_email)
                User.objects.create_user(username=uname, email=post_email)
                length_of_string = 10
                sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$^&*/!"
                pswd = ''.join(random.choices(sample_str, k=length_of_string))
                register.objects.filter(email=post_email).update(password=pswd)
                # name=uname.name
                # subject = 'Welcome to Appetite'
                # message = f'Hi {name}, Thank you for accepting our invitaion to join Appetite.\n' \
                #           f'Your Email Id and Password has been provided below :\n' \
                #           f'Email Id : {post_email} \n' \
                #           f'Password : {pswd} \n' \
                #           f'Thank you..'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['', ]
                # send_mail(subject, message, email_from, recipient_list)

                messages.warning(request, "Registration Successful")
                return redirect('/register/%s' % uid)

    else:
        form_value = registerform()
        return render(request, "admin/register.html", {'form_key': form_value,'login_id':uid})


def supplier_reg(request):
    if request.method == 'POST':
        form = supplierregform(request.POST, request.FILES)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            if User.objects.filter(email=post_email).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/supplier_reg/')
            else:
                form.save()
                uname = surplus_food_supplier.objects.get(email=post_email)
                User.objects.create_user(username=uname, email=post_email)
                messages.warning(request, "Registration Successful")
                return redirect('/supplier_reg/')

    else:
        form_value = supplierregform()
        return render(request, "main/supplier_register.html", {'form_key': form_value})


def login(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email_val = form.cleaned_data['email']
            pswd = form.cleaned_data['password']
            try:
                user = register.objects.get(email=email_val)
                if user:
                    try:
                        user1 = register.objects.get(Q(reg_id=user.reg_id) & Q(password=pswd))
                        if user1:
                            request.session['session_id'] = user.reg_id
                            if user.usertype == 1:
                                return redirect('/admin_home/%s' % user.reg_id)
                            else:
                                    return redirect('/user_home/%s' % user.reg_id)

                    except register.DoesNotExist:
                        user1 = None
                        messages.warning(request, "Incorrect Password")
                        return redirect('/login/')
            except register.DoesNotExist:
                try:
                    user = surplus_food_supplier.objects.get(email=email_val)
                    if user:
                        try:
                            user1 = surplus_food_supplier.objects.get(Q(supplier_id=user.supplier_id) & Q(password=pswd))
                            if user1:
                                if user.status == True:
                                    request.session['session_id'] = user.supplier_id
                                    return redirect('/supplier_home/%s' % user.supplier_id)
                                else:
                                    messages.warning(request, "You are not yet approved")
                                    return redirect('/login/')
                        except surplus_food_supplier.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/login/')
                except surplus_food_supplier.DoesNotExist:
                    try:
                        user = delivery_agent.objects.get(email=email_val)
                        if user:
                            try:
                                user1 = delivery_agent.objects.get(Q(agent_id=user.agent_id) & Q(password=pswd))
                                if user1:
                                    request.session['session_id'] = user.agent_id
                                    return redirect('/delivery_agent_home/%s' % user.agent_id)
                            except delivery_agent.DoesNotExist:
                                user1 = None
                                messages.warning(request, "Incorrect Password")
                                return redirect('/login/')
                    except delivery_agent.DoesNotExist:
                                user = None
                                messages.warning(request, "Invalid Email Id")
                                return redirect('/login/')
    else:
        form1 = Loginform()
        return render(request, "main/login.html", {'form': form1})


def delivery_agent_reg(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = addDeliveryAgentForm(request.POST,request.FILES)
            length_of_string = 10
            sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$^&*/!"
            pswd = ''.join(random.choices(sample_str, k=length_of_string))
            if form.is_valid():
                name = form.cleaned_data['name']
                post_email = form.cleaned_data['email']
                id_proof = form.files['id_proof']
                profile_pic = form.files['profile_pic']
                if User.objects.filter(email=post_email).exists():
                    messages.warning(request, "Email Id Already Exist")
                    return redirect('/delivery_agent_reg/%s' % uid)
                else:
                    delivery_agent.objects.create(name=name, email=post_email, password=pswd,id_proof=id_proof,profile_pic=profile_pic)
                    uname = delivery_agent.objects.get(email=post_email)
                    User.objects.create_user(username=uname, email=post_email)
                    name = form.cleaned_data['name']
                    # subject = 'Welcome to Appetite'
                    # message = f'Hi {name}, Thank you for accepting our invitaion to join Appetite.\n' \
                    #           f'Your Email Id and Password has been provided below :\n' \
                    #           f'Email Id : {post_email} \n' \
                    #           f'Password : {pswd} \n' \
                    #           f'Thank you..'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = ['', ]
                    # send_mail(subject, message, email_from, recipient_list)
                    messages.warning(request, "Delivery Agent Added Successfully")
                    return redirect('/delivery_agent_reg/%s' % uid)
        else:
            form_value = addDeliveryAgentForm()
            return render(request, "admin/add_delivery_agent.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def user_list(request, uid):
    if request.session.get('session_id'):
        user = register.objects.filter(Q(usertype=2))

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/user_list.html",
                      {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delete_user(request, uid, id):
    if request.session.get('session_id'):
        cust = register.objects.get(reg_id=id)
        user = User.objects.get(email=cust.email)
        user.delete()
        register.objects.filter(reg_id=id).delete()
        return redirect('/user_list/%s' % uid)
    else:
        return redirect('/login/')


def approvesuppliers(request, uid):
    if request.session.get('session_id'):
        suppliers = surplus_food_supplier.objects.filter(status=False)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(suppliers, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/approve_suppliers.html",
                      {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def approve_supplier(request, uid, id):
    if request.session.get('session_id'):
        surplus_food_supplier.objects.filter(supplier_id=id).update(status=True)
        return redirect('/approvesuppliers/%s' % uid)
    else:
        return redirect('/login/')


def reject_supplier(request, uid, id):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.get(supplier_id=id)
        user = User.objects.get(email=supplier.email)
        user.delete()
        surplus_food_supplier.objects.get(supplier_id=id).delete()
        return redirect('/approvesuppliers/%s' % uid)
    else:
        return redirect('/login/')


def supplier_list(request, uid):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.filter(status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(supplier, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/supplier_list.html",
                      {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delete_supplier(request, uid, id):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.get(supplier_id=id)
        user = User.objects.get(email=supplier.email)
        user.delete()
        surplus_food_supplier.objects.get(supplier_id=id).delete()
        return redirect('/supplier_list/%s' % uid)
    else:
        return redirect('/login/')


def delivery_agent_list(request, uid):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(agent, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "admin/delivery_agent_list.html",
                      {'agents': agent, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delete_delivery_agent(request, uid, id):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.get(agent_id=id)
        user = User.objects.get(email=agent.email)
        user.delete()
        delivery_agent.objects.get(agent_id=id).delete()
        return redirect('/delivery_agent_list/%s' % uid)
    else:
        return redirect('/login/')



def admin_profile(request, uid):
    if request.session.get('session_id'):
        admin = register.objects.get(reg_id=uid)
        return render(request, "admin/admin_profile.html", {'admin': admin, 'login_id': uid})
    else:
        return redirect('/login/')


def edit_admin_profile(request, uid):
    if request.session.get('session_id'):
        admin = register.objects.get(reg_id=uid)
        if request.method == 'POST':
            form = Editadminprofileform(request.POST, instance=admin)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/admin_profile/%s' % uid)

        else:
            form_value = Editadminprofileform(instance=admin)
            return render(request, "admin/edit_admin_profile.html",
                          {'form_key': form_value, 'admin': admin, 'login_id': uid})
    else:
        return redirect('/login/')


def user_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "user/user_home.html", {'login_id': uid})
    else:
        return redirect('/login/')


def admin_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "admin/admin_home.html", {'login_id': uid})
    else:
        return redirect('/login/')


def supplier_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "supplier/supplier_home.html", {'login_id': uid})
    else:
        return redirect('/login/')



def delivery_agent_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "delivery/delivery_agent_home.html", {'login_id': uid})
    else:
        return redirect('/login/')


def user_profile(request, uid):
    if request.session.get('session_id'):
        users = register.objects.get(reg_id=uid)
        return render(request, "user/user_profile.html", {'users': users,'login_id': uid})
    else:
        return redirect('/login/')


def edit_user_profile(request, uid):
    if request.session.get('session_id'):
        users = register.objects.get(reg_id=uid)
        if request.method == 'POST':
            form = Edituserform(request.POST, request.FILES, instance=users)

            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/user_profile/%s' % uid)

        else:
            form_value = Edituserform(instance=users)
            return render(request, "user/edit_user_profile.html",
                          {'form_key': form_value, 'users': users, 'login_id': uid})
    else:
        return redirect('/login/')



def supplier_profile(request, uid):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.get(supplier_id=uid)
        return render(request, "supplier/supplier_profile.html", {'supplier': supplier,'login_id': uid})
    else:
        return redirect('/login/')


def edit_supplier_profile(request, uid):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.get(supplier_id=uid)
        if request.method == 'POST':
            form = Editsupplierregform(request.POST,request.FILES, instance=supplier)

            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/supplier_profile/%s' % uid)

        else:
            form_value = Editsupplierregform(instance=supplier)
            return render(request, "supplier/edit_supplier_profile.html",
                          {'form_key': form_value, 'supplier': supplier, 'login_id': uid})
    else:
        return redirect('/login/')


def add_supplier_surplus(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = Addsurplusform(request.POST, request.FILES)
            if form.is_valid():
                details = form.cleaned_data['details']
                image = form.files['image']
                supplier_id = surplus_food_supplier.objects.get(supplier_id=uid)
                uploaded_on = datetime.now().date()
                uploaded_time= timezone.localtime(timezone.now())
                five_hours_later = uploaded_time + timedelta(hours=5)
                time_expire = five_hours_later.replace(second=0, microsecond=0)
                time_exp = time_expire.strftime("%I:%M %p")
                uploaded_tm = uploaded_time.strftime("%I:%M %p")
                supplier_surplus_food.objects.create(uploaded_time=uploaded_tm,time_expire=time_exp,uploaded_on=uploaded_on,details=details,image=image,supplier_id=supplier_id,)
                messages.warning(request, "Surplus Food Details Added")
                return redirect('/add_supplier_surplus/%s' % uid)
        else:
            form_value = Addsurplusform()
            return render(request, "supplier/add_surplus_food.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def edit_supplier_surplus(request, uid, id):
    if request.session.get('session_id'):
        surplus = supplier_surplus_food.objects.get(surplus_id=id)
        if request.method == 'POST':
            form = editsurplusform(request.POST, request.FILES, instance=surplus)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/supplier_surplus_list/%s' % uid)
        else:
            form_value = editsurplusform(instance=surplus)
            return render(request, "supplier/edit_surplus_food.html",
                          {'form_key': form_value, 'surplus': surplus, 'login_id': uid})
    else:
        return redirect('/login/')


def supplier_surplus_list(request, uid):
    if request.session.get('session_id'):
        surplus = supplier_surplus_food.objects.filter(Q(supplier_id=uid) & Q(status=True))
        for i in surplus:
            timeexp = datetime.strptime(i.time_expire, "%I:%M %p")
            time_expire = timeexp.time()
            current_time=timezone.localtime(timezone.now()).time()
            if current_time <= time_expire:
                pass
            else:
                supplier_surplus_food.objects.filter(surplus_id=i.surplus_id).update(status=False,supply_status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(surplus, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "supplier/surplus_list.html",
                      {'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/login/')


def delete_supplier_surplus(request, uid, id):
    if request.session.get('session_id'):
        supplier_surplus_food.objects.get(surplus_id=id).delete()
        return redirect('/supplier_surplus_list/%s' % uid)
    else:
        return redirect('/login/')

def supplier_list(request, uid):
    if request.session.get('session_id'):
        supplier = surplus_food_supplier.objects.filter(status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(supplier, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/supplier_list.html",
                      {'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def user_surplus_list(request, uid):
    if request.session.get('session_id'):
        user=register.objects.get(reg_id=uid)
        surplus = supplier_surplus_food.objects.filter(Q(status=True) & Q(supplier_id__city=user.city))
        for i in surplus:
            timeexp = datetime.strptime(i.time_expire, "%I:%M %p")
            time_expire = timeexp.time()
            current_time=timezone.localtime(timezone.now()).time()
            if current_time <= time_expire:
                pass
            else:
                supplier_surplus_food.objects.filter(surplus_id=i.surplus_id).update(status=False,supply_status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(surplus, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/surplus_food.html",
                      {'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/login/')

def user_surplus_request(request,uid,id):
    if request.session.get('session_id'):
        surplus_id= supplier_surplus_food.objects.get(surplus_id=id)
        user_id=register.objects.get(reg_id=uid)
        agent = delivery_agent.objects.filter(available=True).first()
        current_time = timezone.localtime(timezone.now())
        one_hour_later = current_time + timedelta(hours=1)
        pickupat = one_hour_later.replace(second=0, microsecond=0)
        pickup_at= pickupat.strftime("%I:%M %p")
        surplus_requests.objects.create(surplus_id=surplus_id,user_id=user_id,agent_id=agent,pickup_at=pickup_at)
        supplier_surplus_food.objects.filter(surplus_id=id).update(status=False)
        delivery_agent.objects.filter(agent_id=agent.agent_id).update(available=False)
        return redirect('/user_surplus_list/%s' % uid)
    else:
        return redirect('/login/')

def surplus_accepted_users(request, uid):
    if request.session.get('session_id'):
        surplus = surplus_requests.objects.filter(Q(surplus_id__supplier_id=uid) & Q(surplus_id__status=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(surplus, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "supplier/surplus_accepted_users.html",
                      {'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/login/')


def accepted_surplus_food(request, uid):
    if request.session.get('session_id'):
        surplus = surplus_requests.objects.filter(Q(user_id=uid) & Q(surplus_id__status=False))
        page_num = request.GET.get('page', 1)
        paginator = Paginator(surplus, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/accepted_surplus_food.html",
                      {'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/login/')

def delivery_agent_orders(request,uid):
    if request.session.get('session_id'):
        order_list = surplus_requests.objects.filter(Q(agent_id=uid) & Q(deliver_status=False)).order_by('accepted_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "delivery/my_orders.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')

def pickup_order(request, uid, id):
    if request.session.get('session_id'):
        current_time = timezone.localtime(timezone.now())
        pickup_at = current_time.strftime("%I:%M %p")
        surplus_requests.objects.filter(req_id=id).update(pickup_status=True,pickup_at=pickup_at)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/login/')

def deliver_order(request, uid, id):
    if request.session.get('session_id'):
        current_time = timezone.localtime(timezone.now())
        delivered_at = current_time.strftime("%I:%M %p")
        surplus_requests.objects.filter(req_id=id).update(deliver_status=True,delivered_at=delivered_at)
        delivery_agent.objects.filter(agent_id=uid).update(available=True)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/login/')


def delivery_completed_tasks(request,uid):
    if request.session.get('session_id'):
        order_list = surplus_requests.objects.filter(Q(agent_id=uid) & Q(deliver_status=True)).order_by('-accepted_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "delivery/completed_tasks.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')



def surplus_food_information(request,uid):
    if request.session.get('session_id'):
        order_list = surplus_requests.objects.all().order_by('-accepted_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/surplus_food_information.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')


def all_surplus_food_information(request,uid):
    if request.session.get('session_id'):
        order_list = supplier_surplus_food.objects.all().order_by('-uploaded_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/all_surplus_food.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')

def all_surplus_information(request,uid):
    if request.session.get('session_id'):
        order_list = supplier_surplus_food.objects.filter(supplier_id=uid).order_by('-uploaded_on')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "supplier/all_surplus_food.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')



def create_complaint(request, uid,id):
    if request.session.get('session_id'):
        try:
            complaint=complaints.objects.get(req_id=id)
            messages.warning(request, "Complaint Already Raised")
            return redirect('/accepted_surplus_food/%s' % uid)
        except:
            req = surplus_requests.objects.get(req_id=id)
            if request.method == 'POST':
                form = createComplaintForm(request.POST)
                if form.is_valid():
                    complaint=form.cleaned_data['complaint']
                    complaints.objects.create(complaint=complaint,req_id=req)
                    messages.warning(request, "Complaint Raised Successfully")
                    return redirect('/accepted_surplus_food/%s' % uid)
            else:
                form_value = createComplaintForm()
                return render(request, "user/create_complaint.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def give_reply(request, uid,id):
    if request.session.get('session_id'):
            complaint=complaints.objects.get(complaint_id=id)
            if complaint.reply_status == 0:
                messages.warning(request, "You have Already Replied")
                return redirect('/view_complaints_list/%s' % uid)
            else:
                if request.method == 'POST':
                    form = replyComplaintForm(request.POST)
                    if form.is_valid():
                        reply=form.cleaned_data['reply']
                        complaints.objects.filter(complaint_id=id).update(reply=reply,reply_status=False)
                        messages.warning(request, "Reply Sent Successfully")
                        return redirect('/view_complaints_list/%s' % uid)
                else:
                    form_value = replyComplaintForm()
                    return render(request, "admin/give_reply.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def complaints_list(request, uid):
    if request.session.get('session_id'):
        complaint = complaints.objects.filter(req_id__user_id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(complaint, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/complaints_list.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')

def view_complaints_list(request, uid):
    if request.session.get('session_id'):
        complaint = complaints.objects.all().order_by('-complaint_id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(complaint, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/view_complaints_list.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')



def give_feedback(request, uid,id):
    if request.session.get('session_id'):
        try:
            feedback=feedbacks.objects.get(req_id=id)
            messages.warning(request, "Feedback Already Given")
            return redirect('/accepted_surplus_food/%s' % uid)
        except:
            req = surplus_requests.objects.get(req_id=id)
            if request.method == 'POST':
                form = givefeedbackForm(request.POST)
                if form.is_valid():
                    feedback=form.cleaned_data['feedback']
                    feedbacks.objects.create(feedback=feedback,req_id=req)
                    messages.warning(request, "Feedback Given Successfully")
                    return redirect('/accepted_surplus_food/%s' % uid)
            else:
                form_value = givefeedbackForm()
                return render(request, "user/give_feedback.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def give_feedback_reply(request, uid,id):
    if request.session.get('session_id'):
            feedback=feedbacks.objects.get(feedback_id=id)
            if feedback.reply_status == 0:
                messages.warning(request, "You have Already Replied")
                return redirect('/view_feedback_list/%s' % uid)
            else:
                if request.method == 'POST':
                    form = replyfeedbackForm(request.POST)
                    if form.is_valid():
                        reply=form.cleaned_data['reply']
                        feedbacks.objects.filter(feedback_id=id).update(reply=reply,reply_status=False)
                        messages.warning(request, "Reply Sent Successfully")
                        return redirect('/view_feedback_list/%s' % uid)
                else:
                    form_value = replyfeedbackForm()
                    return render(request, "supplier/give_feedback_reply.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def feedback_list(request, uid):
    if request.session.get('session_id'):
        feedback = feedbacks.objects.filter(req_id__user_id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(feedback, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "user/feedback_list.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')

def admin_view_feedback_list(request, uid):
    if request.session.get('session_id'):
        feedback = feedbacks.objects.all().order_by('-feedback_id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(feedback, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/view_feedback_list.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')

def view_feedback_list(request, uid):
    if request.session.get('session_id'):
        feedback = feedbacks.objects.filter(req_id__surplus_id__supplier_id=uid).order_by('-feedback_id')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(feedback, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "supplier/view_feedback_list.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def logout(request):
    del request.session['session_id']
    logouts(request)
    return redirect('/')