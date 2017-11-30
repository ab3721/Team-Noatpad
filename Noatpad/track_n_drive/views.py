from django.shortcuts import render
from .models import Car, Profile, Technician, FutureRepair, PhoneTimings, EmailTimings, Notifications, Repair, \
    TechAddedInfo, Phone, Email, ProfileAddedInfo

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from .forms import AddTechnicianForm, AddTechAddedInfoForm, AddCarForm, AddFutureRepairForm, AddRepairForm, \
    AddPhoneForm, AddEmailForm, AddUserAddedInfoForm, EditCarForm

import datetime


# Create your views here.
def index(request):
    if not request.user.is_anonymous():
        profile = Profile.objects.get(id=request.user.profile.id)
        cars = Car.objects.all()
        user_cars = list(c for c in cars if c.profile == profile)
        techs = Technician.objects.all()
        # future_repairs = FutureRepair.objects.all()
        # user_added_info = User.info.all()
        return render(
            request,
            'index.html',
            context={
                'profile': profile, 'cars': user_cars, 'techs': techs,
                # 'future_repairs': future_repairs,
            },
        )
    else:
        return render(request, 'registration/login.html')


def car_prof(request, unique_id):
    num_users = Profile.objects.all().count()
    profile = Profile.objects.get(id=request.user.profile.id)
    cars = Car.objects.all()
    user_cars = list(c for c in cars if c.profile == profile)
    car = Car.objects.get(unique_id=unique_id)
    techs = Technician.objects.all()
    future_repairs = FutureRepair.objects.all()
    return render(
        request,
        'car.html',
        context={
            'num_users': num_users, 'cars': user_cars, 'techs': techs,
            'future_repairs': future_repairs, 'car': car,
        },
    )


def tech_prof(request, unique_id):
    num_users = Profile.objects.all().count()
    cars = Car.objects.all()
    tech = Technician.objects.get(unique_id=unique_id)
    reps = Repair.objects.filter(technician=tech)
    car_set = list(set((c, rep) for c in cars for rep in reps if c.unique_id == rep.car.unique_id))
    car_tech = dict()
    for c, r in car_set:
        if c in car_tech and r not in car_tech[c]:
            car_tech[c].append(r)
        else:
            car_tech[c] = [r]
    techs = Technician.objects.all()
    future_repairs = FutureRepair.objects.all()
    return render(
        request,
        'tech.html',
        context={
            'num_users': num_users, 'cars': cars, 'techs': techs,
            'future_repairs': future_repairs, 'tech': tech,
            'reps': reps, 'car_tech': car_tech,
        },
    )


def stats(request, unique_id):
    num_users = Profile.objects.all().count()
    cars = Car.objects.all()
    car = Car.objects.get(unique_id=unique_id)
    reps = Repair.objects.all()
    techs = Technician.objects.all()
    future_repairs = FutureRepair.objects.all()
    return render(
        request,
        'stat.html',
        context={
            'num_users': num_users, 'cars': cars, 'techs': techs,
            'future_repairs': future_repairs, 'car': car,
            'reps': reps,
        },
    )


def setting(request):
    cars = Car.objects.all()
    techs = Technician.objects.all()
    phone_timings = PhoneTimings.objects.all()
    email_timings = EmailTimings.objects.all()
    notifications = Notifications.objects.all()
    # note_phone = [(note, pt.phone) for pt in phone_timings for note in pt.notification]
    return render(
        request,
        'settings.html',
        context={
            'cars': cars, 'techs': techs,
            'phone_timings': phone_timings, 'email_timings': email_timings,
            'notifications': notifications,
        }
    )


##### Views for Forms
def add_technician1(request):
    """
    View function for adding a Technician
    """
    tech_inst = Technician()

    if request.method == 'POST':

        form = AddTechnicianForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            tech_inst.fname = form.cleaned_data['fname']
            tech_inst.lname = form.cleaned_data['lname']
            tech_inst.street = form.cleaned_data['street']
            tech_inst.city = form.cleaned_data['city']
            tech_inst.company = form.cleaned_data['company']

            tech_inst.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('tech', args=[str(tech_inst.unique_id)]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddTechnicianForm()

    return render(request, 'add_technician.html', {'form': form, 'techinst': tech_inst})


def add_technician2(request, unique_id):
    """
    View function for adding a Technician
    """
    try:
        tech_inst = get_object_or_404(Technician, unique_id=unique_id)
    except:
        tech_inst = Technician()

    if request.method == 'POST':

        form = AddTechnicianForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            tech_inst.fname = form.cleaned_data['fname']
            tech_inst.lname = form.cleaned_data['lname']
            tech_inst.street = form.cleaned_data['street']
            tech_inst.city = form.cleaned_data['city']
            tech_inst.company = form.cleaned_data['company']

            tech_inst.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('tech', args=[str(unique_id)]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddTechnicianForm(initial={'fname': tech_inst.fname, 'lname': tech_inst.lname,
                                          'street': tech_inst.street, 'city': tech_inst.city,
                                          'company': tech_inst.company})

    return render(request, 'add_technician.html', {'form': form, 'techinst': tech_inst})


def add_technician_info(request, unique_id):
    """
    View function for adding technician info
    """
    try:
        techinfo_inst = get_object_or_404(TechAddedInfo, unique_id=unique_id)
    except:
        techinto_inst = TechAddedInfo()

    if request.method == 'POST':

        form = AddTechAddedInfoForm(request.POST)

        if form.is_valid():
            techinfo_inst.information_name = form.cleaned_data['information_name']
            techinfo_inst.information_contents = form.cleaned_data['information_contents']

            techinfo_inst.save()
            return HttpResponseRedirect(reverse('tech', args=[str(unique_id)]))
    else:
        form = AddTechAddedInfoForm()
    return render(request, 'add_technician_info.html', {'form': form, 'techinfo_inst': techinfo_inst})


# def add_car(request, unique_id):
#    """
#    View function for adding a Car
#    """
#    try:
#        car_inst=get_object_or_404(Car, unique_id = unique_id)
#    except:
#        car_inst = Car()
#
#
#    if request.method == 'POST':
#
#        form = AddCarForm(request.POST)
#        if form.is_valid():
#
#            car_inst.make = form.cleaned_data['make']
#            car_inst.year = form.cleaned_data['year']
#            car_inst.save()
#            return HttpResponseRedirect(reverse('car', args=[str(unique_id)]))
#
#    # If this is a GET (or any other method) create the default form.
#    else:
#        form = AddCarForm()
#    return render(request, 'add_car.html', {'form': form, 'car_inst':car_inst})
def add_car1(request):
    """
   View function for adding a Car
   """

    profile = Profile.objects.get(id=request.user.profile.id)
    cars = Car.objects.all()
    user_cars = list(c for c in cars if c.profile == profile)
    techs = Technician.objects.all()

    car_inst = Car()

    if request.method == 'POST':

        form = AddCarForm(request.POST)
        if form.is_valid():
            car_inst.make = form.cleaned_data['make']
            car_inst.model = form.cleaned_data['model']
            car_inst.profile = request.user.profile
            car_inst.year = form.cleaned_data['year']
            car_inst.profile = request.user.profile
            car_inst.engine_type = form.cleaned_data['engine_type']
            car_inst.mileage = form.cleaned_data['mileage']
            car_inst.oil_type = form.cleaned_data['oil_type']
            car_inst.color = form.cleaned_data['color']
            car_inst.registration = form.cleaned_data['registration']
            car_inst.vin_number = form.cleaned_data['vin_number']
            car_inst.save()
            return HttpResponseRedirect(reverse('car', args=[str(car_inst.unique_id)]))

            # If this is a GET (or any other method) create the default form.
    else:
        form = AddCarForm(initial={'make': car_inst.make, 'model': car_inst.model, 'year': car_inst.year,
                                   'engine_type': car_inst.engine_type, 'mileage': car_inst.mileage,
                                   'oil_type': car_inst.oil_type, 'color': car_inst.color,
                                   'registration': car_inst.registration, 'vin_number': car_inst.vin_number})
    return render(request, 'add_car.html', {'form': form, 'car_inst': car_inst, 'car': car_inst, 'cars': user_cars,
                    'techs': techs, 'profile': profile})


def add_car2(request, unique_id):
    """
   View function for adding a Car
   """
    try:
        car_inst = get_object_or_404(Car, unique_id=unique_id)
    except:
        car_inst = Car()

    if request.method == 'POST':

        form = AddCarForm(request.POST)
        if form.is_valid():
            car_inst.make = form.cleaned_data['make']
            car_inst.model = form.cleaned_data['model']
            car_inst.profile = request.user.profile
            car_inst.year = form.cleaned_data['year']
            car_inst.profile = request.user.profile
            car_inst.engine_type = form.cleaned_data['engine_type']
            car_inst.mileage = form.cleaned_data['mileage']
            car_inst.oil_type = form.cleaned_data['oil_type']
            car_inst.color = form.cleaned_data['color']
            car_inst.registration = form.cleaned_data['registration']
            car_inst.vin_number = form.cleaned_data['vin_number']
            car_inst.save()
            return HttpResponseRedirect(reverse('car', args=[str(unique_id)]))

            # If this is a GET (or any other method) create the default form.
    else:
        form = AddCarForm(initial={'make': car_inst.make, 'model': car_inst.model, 'year': car_inst.year,
                                   'engine_type': car_inst.engine_type, 'mileage': car_inst.mileage,
                                   'oil_type': car_inst.oil_type, 'color': car_inst.color,
                                   'registration': car_inst.registration, 'vin_number': car_inst.vin_number})
    return render(request, 'add_car.html', {'form': form, 'car_inst': car_inst, 'car': car_inst})


class UpdateCar(UpdateView):
    model = Car
    fields = ['make', 'model', 'year', 'engine_type', 'mileage', 'oil_type', 'color', 'registration', 'vin_number']
    template_name = 'edit_car'

# def add_future_repair(request, unique_id):
#     """
#     View function for adding Future Repairs
#     """
#     try:
#         future_repairs_inst = get_object_or_404(FutureRepair, unique_id=unique_id)
#     except:
#         future_repairs_inst = FutureRepair()
#
#     if request.method == 'POST':
#
#         form = AddFutureRepairForm(request.POST)
#         if form.is_valid():
#             future_repairs_inst.name = form.cleaned_data['name']
#             future_repairs_inst.date_of_repair = form.cleaned_data['date_of_repair']
#             # Add technician, car, and notification, ForeignKey
#             future_repairs_inst.save()
#
#             return HttpResponseRedirect(reverse('car', args=[str(unique_id)]))
#     else:
#         form = AddFutureRepairForm()
#
#     return render(request, 'add_future_repairs.html', {'form': form, 'future_repairs_inst': future_repairs_inst})
#
#
# def add_repair(request, unique_id):
#     """
#     View function for adding a repair
#     """
#     try:
#         repair_inst = get_object_or_404(Repair, unique_id=unique_id)
#     except:
#         tech_inst = Repair()
#
#     if request.method == 'POST':
#
#         form = AddRepairForm(request.POST)
#         if form.is_valid():
#             repair_inst.name = form.cleaned_data['name']
#             repair_inst.cost = form.cleaned_data['cost']
#             repair_inst.date_made = form.cleaned_data['date_made']
#             repair_inst.save()
#
#             return HttpResponseRedirect(reverse('car', args=[str(unique_id)]))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         form = AddRepairForm(initial={'renewal_date': proposed_renewal_date, })
#
#     return render(request, 'add_repair.html', {'form': form, 'repair_inst': repair_inst})
#
#
# def add_phone(request, unique_id):
#     """
#     View function for adding a phone number
#     """
#     try:
#         phone_inst = get_object_or_404(Phone, unique_id=unique_id)
#     except:
#         phone_inst = Phone()
#
#     if request.method == 'POST':
#
#         form = AddPhoneForm(request.POST)
#         if form.is_valid():
#             phone_inst.number = form.cleaned_data['number']
#             # add user, ForeignKey
#             phone_inst.save()
#
#             return HttpResponseRedirect(reverse('settings'))
#
#     else:
#
#         form = AddPhoneForm()
#
#     return render(request, 'add_phone.html', {'form': form, 'phone_inst': phone_inst})
#
#
# def add_email(request, unique_id):
#     """
#     View function for adding an email
#     """
#     try:
#         email_inst = get_object_or_404(Email, unique_id=unique_id)
#     except:
#         email_inst = Email()
#
#     if request.method == 'POST':
#
#         form = AddEmailForm(request.POST)
#
#         if form.is_valid():
#             email_inst.address = form.cleaned_data['address']
#             # add user, ForeignKey
#             email_inst.save()
#
#             return HttpResponseRedirect(reverse('settings'))
#
#     else:
#
#         form = AddEmailForm()
#
#     return render(request, 'add_email.html', {'form': form, 'email_inst': email_inst})
#
#
# def add_user_info(request, unique_id):
#     """
#     View function for adding User Info
#     """
#     try:
#         userinfo_inst = get_object_or_404(ProfileAddedInfo, unique_id=unique_id)
#     except:
#         userinfo_inst = ProfileAddedInfo()
#
#     if request.method == 'POST':
#
#         form = AddUserAddedInfoForm(request.POST)
#
#         if form.is_valid():
#             userinfo_inst.information_name = form.cleaned_data['information_name']
#             userinfo_inst.contents = form.cleaned_data['contents']
#             userinfo_inst.save()
#
#             return HttpResponseRedirect(reverse('settings'))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         form = AddUserAddedInfoForm()
#     return render(request, 'add_user_info', {'form': form, 'userinfo_inst': userinfo_inst})
