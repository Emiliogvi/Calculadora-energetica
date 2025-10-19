from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm, ElectrodomesticoForm
from django.contrib.auth.decorators import login_required
from .models import Electrodomestico, TarifaEnergia
from functools import wraps
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout

# def _users(session):
#     return session.setdefault('users', [])

# def _current(session):
#     return session.get('user')

# def login_required(view):
#     @wraps(view)
#     def wrapper(request, *a, **kw):
#         if not _current(request.session):
#             return redirect('login')
#         return view(request, *a, **kw)
#     return wrapper

def home(request):

    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Verificar si ya existe
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Ya existe una cuenta con este correo')
            else:
                # Crear usuario en la base de datos
                usuario = User.objects.create_user(
                    username=email,                 # Django necesita username
                    email=email,
                    first_name=form.cleaned_data['nombre'],
                    last_name=form.cleaned_data['apellido'],
                    password=form.cleaned_data['password']
                )
                login(request, usuario)  # Iniciar sesión automáticamente
                return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Credenciales inválidas. Verifica tu correo y contraseña.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def ingresar_electrodomestico(request):
    if request.method == 'POST':
        form = ElectrodomesticoForm(request.POST)
        if form.is_valid():
            electro = form.save(commit=False)
            electro.usuario = request.user
            electro.save()
            return redirect('dashboard') 
    else:
        form = ElectrodomesticoForm()
    return render(request, 'ingresar_electrodomestico.html', {'form': form})

@login_required
def listar_electrodomesticos(request):
    electrodomesticos = Electrodomestico.objects.all()
    return render(request, 'listar_electrodomesticos.html', {'electrodomesticos': electrodomesticos})

@login_required
def editar_electrodomestico(request, id):
    # Buscar el electrodoméstico o mostrar error 404 si no existe
    electrodomestico = get_object_or_404(Electrodomestico, id=id)
    
    # Si el formulario fue enviado (POST)
    if request.method == 'POST':
        form = ElectrodomesticoForm(request.POST, instance=electrodomestico)
        if form.is_valid():
            form.save()
            return redirect('listar_electrodomesticos')  # Asegúrate de que este nombre coincida con tu URL
    else:
        form = ElectrodomesticoForm(instance=electrodomestico)

    # Renderizar el template
    return render(request, 'electrodomesticos/editar_electrodomesticos.html', {
        'form': form,
        'electrodomestico': electrodomestico
    })

@login_required
def eliminar_electrodomestico(request, id):
    electro = get_object_or_404(Electrodomestico, id=id)
    electro.delete()
    return redirect('listar_electrodomesticos')

@login_required
def calcular_consumos(request):
    electrodomesticos = Electrodomestico.objects.filter(usuario=request.user)
    resultados = []
    tarifa_usuario = TarifaEnergia.objects.filter(usuario=request.user).last()
    
    if request.method == 'POST':
        valor_kwh = float(request.POST.get('tarifa'))
        if not tarifa_usuario or tarifa_usuario.valor_kwh != valor_kwh:
            TarifaEnergia.objects.create(usuario=request.user, valor_kwh=valor_kwh)
        tarifa = valor_kwh
    else:
        tarifa = tarifa_usuario.valor_kwh if tarifa_usuario else 0.0

    for e in electrodomesticos:
        consumo_diario_kwh = (e.potencia_w * e.horas_uso_diario) / 1000
        consumo_mensual = consumo_diario_kwh * 30
        consumo_anual = consumo_diario_kwh * 365
        costo_mensual = consumo_mensual * tarifa
        costo_anual = consumo_anual * tarifa
        huella_mensual = consumo_mensual * 0.43
        huella_anual = consumo_anual * 0.43

        resultados.append({
            'nombre': e.nombre,
            'consumo_mensual': round(consumo_mensual, 2),
            'consumo_anual': round(consumo_anual, 2),
            'costo_mensual': round(costo_mensual, 2),
            'costo_anual': round(costo_anual, 2),
            'huella_mensual': round(huella_mensual, 2),
            'huella_anual': round(huella_anual, 2),
        })

    return render(request, 'calcular_consumos.html', {'resultados': resultados, 'tarifa': tarifa})

@login_required
def comparar_electrodomesticos(request):
    tarifa = float(request.GET.get('tarifa', 0))
    
    # Traer todos los electrodomésticos para el formulario
    electrodomesticos = Electrodomestico.objects.all()

    # Por ahora seleccionamos los primeros de cada tipo para los cálculos
    electro_conv = Electrodomestico.objects.filter(tipo='convencional').first()
    electro_efic = Electrodomestico.objects.filter(tipo='eficiente').first()

    if not electro_conv or not electro_efic:
        mensaje = "No hay electrodomésticos suficientes para comparar."
        return render(request, "comparar_electrodomesticos.html", {
            'mensaje': mensaje,
            'electrodomesticos': electrodomesticos
        })

    # Calculos
    consumo_mensual_conv = electro_conv.potencia_w * electro_conv.horas_uso_diario * 30 / 1000
    consumo_mensual_efic = electro_efic.potencia_w * electro_efic.horas_uso_diario * 30 / 1000

    resultado = {
        'tarifa': tarifa,
        'conv': {
            'nombre': electro_conv.nombre,
            'consumo_mensual': consumo_mensual_conv,
            'costo_mensual': consumo_mensual_conv * tarifa,
        },
        'efic': {
            'nombre': electro_efic.nombre,
            'consumo_mensual': consumo_mensual_efic,
            'costo_mensual': consumo_mensual_efic * tarifa,
        },
        'ahorro_costo_mensual': (consumo_mensual_conv - consumo_mensual_efic) * tarifa,
        'ahorro_kwh_mensual': consumo_mensual_conv - consumo_mensual_efic,
        'ahorro_co2_mensual': (consumo_mensual_conv - consumo_mensual_efic) * 0.43,
    }

    return render(request, "comparar_electrodomesticos.html", {
        'resultado': resultado,
        'electrodomesticos': electrodomesticos
    })
