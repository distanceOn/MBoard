from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, AdvertisementForm, ResponseFilterForm, ResponseForm, VerificationCodeForm
from .models import Advertisement, CustomUser, Response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
import string
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохраняем, но пока не активируем пользователя
            user.is_active = False
            user.save()
            send_verification_email(user)  # Отправляем код для подтверждения
            return redirect('email_sent')  # Перенаправляем на страницу с сообщением о том, что письмо отправлено
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)  # Добавьте request.FILES
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('home')
    else:
        form = AdvertisementForm()
    return render(request, 'create_advertisement.html', {'form': form})


@login_required
def create_response(request, ad_id):
    advertisement = Advertisement.objects.get(id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()
            # Отправить e-mail уведомление владельцу объявления
            send_notification_email(
                'Новый отклик на ваше объявление',
                f'Пользователь {request.user.username} оставил отклик на ваше объявление {advertisement.title}.',
                [advertisement.user.email]
            )
            return redirect('home')
    else:
        form = ResponseForm()
    return render(request, 'create_response.html', {'form': form, 'advertisement': advertisement})


from django.core.mail import send_mail

def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'from@example.com',
        recipient_list,
        fail_silently=False,
    )
    
    
@login_required
def view_advertisement(request, ad_id):
    advertisement = get_object_or_404(Advertisement, id=ad_id)
    file_ext = advertisement.attached_file.name.split('.')[-1] if advertisement.attached_file else None

    if file_ext in ['jpg', 'jpeg', 'png']:
        file_type = 'image'
    elif file_ext == 'pdf':
        file_type = 'pdf'
    elif file_ext in ['mp4', 'avi']:
        file_type = 'video'
    else:
        file_type = 'unknown'

    # Обработка отправки формы ResponseForm
    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            # Создайте объект Response и сохраните его в базе данных
            response = response_form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()
          

    else:
        response_form = ResponseForm()

    return render(request, 'view_advertisement.html', {'advertisement': advertisement, 'file_type': file_type, 'response_form': response_form})

@login_required
def edit_advertisement(request, ad_id):
    advertisement = Advertisement.objects.get(id=ad_id)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'edit_advertisement.html', {'form': form})

@login_required
def view_responses(request):
    responses = Response.objects.filter(advertisement__user=request.user, is_hidden=False)  # Добавляем is_hidden=False

    # Обработка фильтрации
    category_filter = request.POST.get('category')
    if category_filter:
        responses = responses.filter(advertisement__category=category_filter)

    filter_form = ResponseFilterForm(initial={'category': category_filter})

    return render(request, 'view_responses.html', {'responses': responses, 'filter_form': filter_form})

def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_verification_email(user):
    code = generate_verification_code()
    user.email_verification_code = code
    user.save()
    send_mail(
        'Подтверждение регистрации',
        f'Ваш код подтверждения: {code}',
        'no-reply@yourwebsite.com',
        [user.email],
        fail_silently=False,
    )


def email_sent(request):
    return render(request, 'email_sent.html')


def confirm_email_page(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                user = CustomUser.objects.get(email_verification_code=code)
                user.is_active = True
                user.email_verification_code = None  # очищаем код, так как он уже использован
                user.save()
                
                return redirect('home')  # перенаправляем на главную страницу
            except CustomUser.DoesNotExist:
                # код не найден
                form.add_error('code', 'Неверный код подтверждения')
    else:
        form = VerificationCodeForm()
    return render(request, 'confirm_email_page.html', {'form': form})

@login_required
def home(request):
    advertisements = Advertisement.objects.all()  # Получаем все объявления
    return render(request, 'home.html', {'advertisements': advertisements})


def manage_response(request, response_id, action):
    try:
        response = Response.objects.get(id=response_id)
        
        # В зависимости от значения параметра 'action' выполняем разные действия
        if action == 'approve':
            response.is_accepted = True
            response.is_hidden = True  # Скрываем отклик после одобрения
            response.save()
            messages.success(request, 'Отклик одобрен успешно.')
        elif action == 'reject':
            response.is_accepted = False
            response.is_hidden = True  # Скрываем отклик после отклонения
            response.save()
            messages.success(request, 'Отклик отклонен успешно.')
        else:
            messages.error(request, 'Недопустимое действие для управления откликами.')
    except Response.DoesNotExist:
        messages.error(request, 'Отклик не найден.')
    
    return redirect('view_responses')  # Перенаправляем пользователя на страницу с откликами
