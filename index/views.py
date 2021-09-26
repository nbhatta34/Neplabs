from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from numpy import add, dot
from .forms import LoginForm, UserAdminCreationForm, SearchForm
from .auth import unauthenticated_user
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .models import AddToCart, LabResult, Order, Profile, UserProfile, Test, VaccineBooking
from django.contrib.auth import get_user_model
from .models import Document, Hospital
from django.http import HttpResponse, response, JsonResponse
from math import cos, asin, sqrt, pi
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
User = get_user_model()


# Create your views here.
def index_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_obj = User.objects.filter(email=email).first()

            profile_obj = Profile.objects.filter(user=user_obj).first()

            if not profile_obj.is_verified:
                messages.warning(
                    request, 'Account is not verified. Please check your email.')
                return redirect('/')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/userDash')

            else:
                messages.add_message(
                    request, messages.ERROR, 'Invalid username or password')
                return render(request, 'index/index.html', {'form': form})
    context = {
        'form': LoginForm,
        "activate_login": 'active'
    }
    return render(request, 'index/index.html', context)


@login_required
def user_dashboard(request):
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    context = {
        'cart_item_quantity': cart_item_quantity
    }
    return render(request, 'index/userDash.html', context)


def user_sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        form = UserAdminCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            us_id = user.id
            user_id = User.objects.get(id=us_id)
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_id, auth_token=auth_token)

            UserProfile.objects.create(user=user, username=user.username, firstname=user.first_name,
                                       lastname=user.last_name, phone=user.phone, email=user.email)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error in registering User')
            return render(request, 'accounts/userSignUp.html', {'form': form})
    context = {
        'form': UserAdminCreationForm,
        'activate_signup': 'active'
    }
    return render(request, 'index/userSignUp.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def token_send(request):
    return render(request, 'index/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.info(
                    request, 'Your account is already been verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(
                request, 'Congratulations your account has been verified.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


@csrf_exempt
@login_required
def add_documents(request):
    documents = Document.objects.filter(user_id=request.user.id)
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    if request.method == 'POST':
        document_type = request.POST.get('document_type')
        description = request.POST.get('description')
        upload = request.FILES.get('file')
        user = request.user.id

        file_obj = Document(document_type=document_type,
                            upload=upload, description=description, user_id=user)
        file_obj.save()

        if file_obj:
            file = Document.objects.values().filter(user_id=request.user.id)
            list_file = list(file)
            return JsonResponse({'data': list_file})

        else:
            return HttpResponse("File cannot be added")

    context = {
        'documents': documents,
        'cart_item_quantity': cart_item_quantity
    }

    return render(request, 'index/documents.html', context)


@login_required
def delete_document(request):
    id1 = request.GET.get('id', None)
    Document.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


@login_required
def distance_ajax(request):
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    format_distance = 0
    nearby_distance = []
    nearby_address = []

    if request.method == 'POST':
        lat1 = request.POST.get('latitude')
        lon1 = request.POST.get('longitude')

        db_lat_lon = Hospital.objects.values_list(
            'latitude',
            'longitude',
            'address'
        )

        nearby_distance = []
        nearby_address = []

        for lat_lon in db_lat_lon:
            if not lat_lon[0] == None and not lat_lon[1] == None:
                if not lat_lon[2] in nearby_address:
                    latitude = float(lat_lon[0])
                    longitude = float(lat_lon[1])
                    address = lat_lon[2]
                    p = pi / 180
                    a = 0.5 - cos((latitude - float(lat1)) * p) / 2 + cos(float(lat1) * p) * \
                        cos(latitude * p) * \
                        (1 - cos((longitude - float(lon1)) * p)) / 2
                    distance = 12742 * asin(sqrt(a))
                    format_distance = "{:.2f}".format(distance)

                    if float(format_distance) < 5:
                        nearby_distance.append(format_distance)
                        nearby_address.append(address)

        return response.JsonResponse({"data": nearby_distance, "data1": nearby_address})

    context = {
        'distance': format_distance,
        'nearby_distance': nearby_distance,
        'nearby_address': nearby_address,
        'cart_item_quantity': cart_item_quantity
    }

    return render(request, 'index/distance_ajax.html', context)


@login_required
def diagnostics(request):
    context = {
    }
    return render(request, 'index/diagnostics.html', context)


@login_required
def profile(request):
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    profile = request.user.userprofile
    email = request.user.email
    lab_result = LabResult.objects.filter(user_email=email)
    context = {
        'test_history': lab_result,
        'cart_item_quantity': cart_item_quantity
    }
    return render(request, 'index/profile.html', context)


@csrf_exempt
def edit_profile(request):
    current_user = request.user.id
    profile = UserProfile.objects.get(user_id=current_user)
    if request.method == "POST":
        profile.firstname = request.POST['first_name']
        profile.lastname = request.POST['last_name']
        profile.phone = request.POST['phone']
        profile.gender = request.POST['gender']
        profile.age = request.POST['age']
        profile.nationality = request.POST['nationality']
        profile.dob = request.POST['dob']
        print(request.POST['dob'])
        profile.address = request.POST['address']
        profile.save()

    return response.JsonResponse({
        "fname": request.POST['first_name'],
        "lname": request.POST['last_name'],
        "phone": request.POST['phone'],
        "gender": request.POST['gender'],
        "nationality": request.POST['nationality'],
        "dob": request.POST['dob'],
        "address": request.POST['address']
    })


@csrf_exempt
def update_image(request):
    current_user = request.user.id
    profile = UserProfile.objects.get(user_id=current_user)
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        profile.profile_pic = profile_pic
        profile.save()
        image = UserProfile.objects.values().filter(user_id=current_user)

        list_image = list(image)

    return JsonResponse({'image': list_image})


@login_required
def laboratory_test(request):
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    cart_items = AddToCart.objects.filter(
        user_id=request.user.id).order_by('-id')
    tests = Test.objects.all().order_by('-id')

    price = AddToCart.objects.filter(
        user_id=request.user.id).values_list('price')
    total = 0
    total_price = 0
    list_price = list(price)
    numbers1 = []
    for i in list_price:
        total = i[0]
        for word in total.split():
            if word.isdigit():
                numbers1.append(int(word))
    for j in numbers1:
        total_price += j
    context = {
        'tests': tests,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_quantity': cart_item_quantity
    }
    return render(request, 'index/laboratory_tests.html', context)


@login_required
def lab_result(request):
    email = request.user.email
    cart_item_quantity = AddToCart.objects.filter(
            user_id=request.user.id).count()
    if LabResult.objects.filter(user_email=email):
        lab_result = LabResult.objects.filter(user_email=email)
    else:
        return redirect('/no_content')
    context = {
        "lab_result": lab_result,
        'cart_item_quantity': cart_item_quantity
    }
    return render(request, 'index/lab_result.html', context)


def no_content(request):
    context = {}
    return render(request, 'index/no_content.html', context)


def delete_lab_result(request):
    id1 = request.GET.get('id', None)
    LabResult.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)


@csrf_exempt
def add_to_cart(request):
    user_id = request.user.id
    if request.method == 'POST':
        test_name = request.POST['test_name']
        test_price = request.POST['test_price']
        quantity = 1
        test_id = request.POST['test_id']
        if not AddToCart.objects.filter(user_id=user_id, test_id=test_id).exists():
            cart_obj = AddToCart.objects.create(
                test_name=test_name, price=test_price, quantity=quantity, user_id=user_id, test_id=test_id)
            file = AddToCart.objects.values().filter(
                user_id=request.user.id).order_by('-id')
            list_file = list(file)
            price = AddToCart.objects.filter(
                user_id=user_id).values_list('price')
            total = 0
            total_price = 0
            list_price = list(price)
            numbers = []
            for i in list_price:
                total = i[0]
                for word in total.split():
                    if word.isdigit():
                        numbers.append(int(word))
            for j in numbers:
                total_price += j
            cart_item_quantity = AddToCart.objects.filter(
                user_id=request.user.id).count()
            return JsonResponse({'data': list_file, 'total': total_price, 'quantity': cart_item_quantity})
        else:
            cart_items = AddToCart.objects.filter(
                user_id=request.user.id).order_by('-id')
            list_file = list(cart_items)
            return JsonResponse({'data': list_file})
    return JsonResponse({})


def delete_cart_item(request):

    item_id = request.GET['item_id']

    AddToCart.objects.get(id=item_id).delete()
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    # Getting the grand total from database

    price = AddToCart.objects.filter(
        user_id=request.user.id).values_list('price')
    total = 0
    total_price = 0
    list_price = list(price)
    numbers1 = []
    for i in list_price:
        total = i[0]
        for word in total.split():
            if word.isdigit():
                numbers1.append(int(word))
    for j in numbers1:
        total_price += j

    data = {
        'deleted': True,
        'total_price': total_price,
        'cart_item_quantity': cart_item_quantity
    }
    return JsonResponse(data)


@login_required
def Checkout(request):
    item_number = AddToCart.objects.filter(user_id=request.user.id).count()
    test_items = AddToCart.objects.filter(user_id=request.user.id)

    price = AddToCart.objects.filter(
        user_id=request.user.id).values_list('price')
    total = 0
    total_price = 0
    list_price = list(price)
    numbers1 = []
    for i in list_price:
        total = i[0]
        for word in total.split():
            if word.isdigit():
                numbers1.append(int(word))
    for j in numbers1:
        total_price += j

    unique_order_id = AddToCart.objects.filter(
        user_id=request.user.id).values_list('id')

    unique_order_id_merge = ''
    for i in unique_order_id:
        unique_order_id_merge += str(i[0])

    if item_number == 0:
        return redirect('/laboratoryTest')
    else:
        if request.method == 'POST':
            payment_method = request.POST['payment_method']
            test_date = request.POST['test_date']
            if request.POST['payment_method'] == 'Esewa':
                return redirect('/esewa-request')
            else:
                Order.objects.create(
                    user_id=request.user.id,
                    order_id='cash' + unique_order_id_merge,
                    payment_method=payment_method,
                    test_date=test_date,
                    total_amount=total_price
                )
                AddToCart.objects.filter(user_id=request.user.id).delete()
                return redirect('/laboratoryTest')

    context = {
        'test_items': test_items,
        'total_price': total_price
    }
    return render(request, 'index/checkout.html', context)


def esewa_request(request):
    price = AddToCart.objects.filter(
        user_id=request.user.id).values_list('price')
    total = 0
    total_price = 0
    list_price = list(price)
    numbers1 = []
    for i in list_price:
        total = i[0]
        for word in total.split():
            if word.isdigit():
                numbers1.append(int(word))
    for j in numbers1:
        total_price += j

    unique_order_id = AddToCart.objects.filter(
        user_id=request.user.id).values_list('id')

    unique_order_id_merge = ''
    for i in unique_order_id:
        unique_order_id_merge += str(i[0])

    context = {
        'total_price': total_price,
        'unique_order_id': unique_order_id_merge
    }
    return render(request, 'index/esewarequest.html', context)


def esewa_verify(request):
    unique_order_id = request.GET.get("oid")
    amount = request.GET.get("amt")
    ref_id = request.GET.get("refId")

    Order.objects.create(order_id=unique_order_id,
                         total_amount=amount, ref_id=ref_id, payment_method="Esewa", user_id=request.user.id)
    AddToCart.objects.filter(user_id=request.user.id).delete()
    messages.success(
        request, 'Your order was successfully placed.')

    if Order.objects.filter(user_id=request.user.id).values_list('order_id') == None:
        Order.objects.filter(user_id=request.user.id, order_id=None).delete()
    return redirect('/laboratoryTest')


@login_required
def vaccine_booking(request):
    cart_item_quantity = AddToCart.objects.filter(
        user_id=request.user.id).count()
    format_distance = 0
    nearby_distance = []
    nearby_address = []

    if request.method == 'POST':
        if request.POST.get("form_type") != 'formOne':
            lat1 = request.POST.get('latitude')
            lon1 = request.POST.get('longitude')

            db_lat_lon = Hospital.objects.values_list(
                'latitude',
                'longitude',
                'address'
            )

            nearby_distance = []
            nearby_address = []

            for lat_lon in db_lat_lon:
                if not lat_lon[0] == None and not lat_lon[1] == None:
                    if not lat_lon[2] in nearby_address:
                        latitude = float(lat_lon[0])
                        longitude = float(lat_lon[1])
                        address = lat_lon[2]
                        p = pi / 180
                        a = 0.5 - cos((latitude - float(lat1)) * p) / 2 + cos(float(lat1) * p) * \
                            cos(latitude * p) * \
                            (1 - cos((longitude - float(lon1)) * p)) / 2
                        distance = 12742 * asin(sqrt(a))
                        format_distance = "{:.2f}".format(distance)

                        if float(format_distance) < 5:
                            nearby_distance.append(format_distance)
                            nearby_address.append(address)

            return response.JsonResponse({"data": nearby_distance, "data1": nearby_address})

    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            try:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                ethnicity = request.POST.get('ethnicity')
                gender = request.POST.get('gender')
                dob = request.POST.get('dob')
                age = request.POST.get('age')
                province = request.POST.get('province')
                district = request.POST.get('district')
                local = request.POST.get('local')
                ward_no = request.POST.get('ward_no')
                nationality = request.POST.get('nationality')
                identity_type = request.POST.get('identity_type')
                id_no = request.POST.get('id_no')
                issue_office = request.POST.get('issue_office')
                occupation = request.POST.get('occupation')
                mobile = request.POST.get('mobile')
                medical_condition = request.POST.get('checkbox_value')
                disability = request.POST.get('disability')
                vaccination_center = request.POST.get('vaccination_center')

                VaccineBooking.objects.create(
                    user_id=request.user.id,
                    first_name=first_name,
                    last_name=last_name,
                    ethnicity=ethnicity,
                    gender=gender,
                    dob=dob,
                    age=age,
                    province=province,
                    district=district,
                    local_level_government=local,
                    ward_no=ward_no,
                    nationality=nationality,
                    identity_type=identity_type,
                    id_number=id_no,
                    issue_office=issue_office,
                    occupation=occupation,
                    mobile=mobile,
                    medical_condition=medical_condition,
                    vaccination_center=vaccination_center
                )
                messages.success(
                    request, 'Your vaccination has been booked succesfully. You will be sent an email for your vaccination card.')
            except Exception as e:
                messages.warning(
                    request, 'Your Vaciination Has Already Been Booked.')
    context = {
        'vaccination_center': nearby_address,
        'cart_item_quantity': cart_item_quantity
    }
    return render(request, 'index/vaccineBooking.html', context)
