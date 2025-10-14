from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from functools import wraps

# "Tabla" de usuarios en sesión (demo sin BD)
def _users(session):
    return session.setdefault('users', [])

def _current(session):
    return session.get('user')

def login_required(view):
    @wraps(view)
    def wrapper(request, *a, **kw):
        if not _current(request.session):
            return redirect('login')
        return view(request, *a, **kw)
    return wrapper

def home(request):
    # Opción A: las plantillas están directamente en calcuapp/templates/
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            users = _users(request.session)
            # impedir correos duplicados
            if any(u['email'] == form.cleaned_data['email'] for u in users):
                form.add_error('email', 'Ya existe una cuenta con este correo')
            else:
                u = {
                    'nombre': form.cleaned_data['nombre'],
                    'apellido': form.cleaned_data['apellido'],
                    'email': form.cleaned_data['email'],
                    'password': form.cleaned_data['password'],  # solo demo
                }
                users.append(u)
                request.session['user'] = {k: u[k] for k in ('nombre', 'apellido', 'email')}
                request.session.modified = True
                return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            user = next((u for u in _users(request.session)
                         if u['email'] == email and u['password'] == pwd), None)
            if user:
                request.session['user'] = {k: user[k] for k in ('nombre', 'apellido', 'email')}
                return redirect('dashboard')
            form.add_error(None, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': _current(request.session)})

def logout_view(request):
    request.session.pop('user', None)
    return redirect('home')
