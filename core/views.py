from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Paciente, Vacina, UF, Municipio, Estabelecimento, Profissional, Agenda, HorarioAgenda, PacienteVacina, Estoque

# Create your views here.
def index(request):
    template_name='core/index.html'
    return render(request, template_name)

def cadastro(request):
    template_name='core/cadastro.html'
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        if campo_vazio(nome):
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'E-mail não pode ficar em branco')
            return redirect('cadastro')
        if senha1 != senha2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este usuário já existe')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este usuário já existe')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha1)
        user.save()
        paciente = Paciente(nome=nome, user=user)
        paciente.save()
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')
    else:
        return render(request, template_name)
        
def login(request):
    template_name='core/login.html'
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == "" or senha == "":
            messages.error(request, 'Os campos não podem ficar em branco')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado c/ sucesso')
                if hasattr(user, 'paciente'): 
                    return redirect('dashboard_paciente')
                if hasattr(user, 'profissional'):
                    return redirect('dashboard_profissional')
                if user.username=='coordenadorSUS':
                    return redirect('dashboard_coord')
    return render(request, 'core/login.html')

def dashboard_coord(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.username=="coordenadorSUS":
            id = request.user.id
        estabelecimentos = Estabelecimento.objects.all().order_by('nomeFantasia')
        context = {
            'estabelecimentos': estabelecimentos,
        }
        template_name='core/dashboard-coord.html'
        return render(request, template_name, context)
    if request.method == 'POST':
        template_name='core/dashboard-coord.html'
        nome = request.POST['nome']
        email = request.POST['email']
        estabelecimento_id = request.POST['estabelecimento_id']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']
        if campo_vazio(nome):
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('dashboard_coord')
        if campo_vazio(email):
            messages.error(request, 'E-mail não pode ficar em branco')
            return redirect('dashboard_coord')
        if campo_vazio(estabelecimento_id):
            messages.error(request, 'Estabelecimento não pode ficar em branco')
            return redirect('dashboard_coord')
        if senha1 != senha2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('dashboard_coord')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este usuário já existe')
            return redirect('dashboard_coord')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Este usuário já existe')
            return redirect('dashboard_coord')
        user = User.objects.create_user(username=nome, email=email, password=senha1)
        user.save()
        estabelecimento = Estabelecimento.objects.get(pk=estabelecimento_id)
        profissional = Profissional(nome=nome, user=user, estabelecimento=estabelecimento)
        profissional.save()
        messages.success(request, 'Cadastro do profissional realizado com sucesso!')
        return redirect('login')
    else:
        return render(request, template_name)


def dashboard_paciente(request):
    if request.user.is_authenticated and hasattr(request.user, 'paciente'):
        id = request.user.id
        paciente = Paciente.objects.get(user=request.user)
        horarios = HorarioAgenda.objects.filter(paciente=paciente, hora_chamada__isnull=True).order_by('-agenda')
        vacinas = PacienteVacina.objects.filter(paciente=paciente).order_by('data')
        context = {
            'horarios': horarios,
            'vacinas': vacinas,
        }
        return render(request, 'core/dashboard-paciente.html', context)
    else:
        return redirect('index')
        
@login_required
def dashboard_profissional(request):
    if request.method == 'GET':
        if request.user.is_authenticated and hasattr(request.user, 'profissional'):
            template_name = 'core/dashboard-profissional.html'
            id = request.user.id
            agendaDia = ()
            horarioAgendas = ()
            msg = True
            agenda = Agenda.objects.filter(data=date.today())
            if len(agenda) != 0:
                msg = False
                agendaDia = agenda[0]
                horarioAgendas = HorarioAgenda.objects.filter(agenda=agendaDia)
            profissional = Profissional.objects.get(user=request.user)
            estabelecimento = Estabelecimento.objects.get(profissional=profissional)
            context = {
                'msg' : msg,
                'agenda': agendaDia,
                'horarioAgendas': horarioAgendas,
                'estabelecimento' : estabelecimento,
            }
            return render(request, template_name, context)
        else:
            return redirect('index')
    if request.method == 'POST':
        if 'chamar_paciente' in request.POST:
            agenda = Agenda.objects.get(data=date.today())
            fila_chamada = agenda.fila_chamada
            fila_chamada = fila_chamada + 1
            agenda.fila_chamada = fila_chamada
            horarioAgenda = HorarioAgenda.objects.get(agenda=agenda, fila=fila_chamada)
            horarioAgenda.hora_chamada = datetime.now()
            agenda.save()
            horarioAgenda.save()
        if 'registro_chegada' in request.POST:
            agenda = Agenda.objects.get(data=date.today())
            fila = agenda.fila
            fila = fila + 1
            agenda.fila = fila
            horarioAgenda = HorarioAgenda.objects.get(pk=request.POST['registro_chegada'])
            horarioAgenda.hora_chegada = datetime.now()
            horarioAgenda.fila = fila
            agenda.save()
            horarioAgenda.save()
        if 'registro_aplicacao' in request.POST:
            horarioAgenda = HorarioAgenda.objects.get(pk=request.POST['registro_aplicacao'])
            horarioAgenda.hora_atendimento = datetime.now()
            horarioAgenda.confirmacao = True
            horarioAgenda.save()
            pacienteVacina = PacienteVacina(paciente=horarioAgenda.paciente, vacina=horarioAgenda.vacina, data=datetime.now())
            pacienteVacina.save()
            profissional = Profissional.objects.get(user=request.user)
            estabelecimento = Estabelecimento.objects.get(profissional=profissional)
            estoque = Estoque.objects.get(vacina=horarioAgenda.vacina, estabelecimento=estabelecimento)
            estoque.quantidade = estoque.quantidade - 1
            estoque.save()
        return redirect('dashboard_profissional') 

def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required
def selecionar_municipio(request):
    if request.method == 'GET':
        template_name = 'core/selecao-municipio.html'
        municipios = Municipio.objects.all().order_by('nome')
        context = {
            'municipios': municipios
        }
        return render(request, template_name, context)
    if request.method == 'POST':
        municipio = request.POST['municipio_id']
        return HttpResponseRedirect(reverse('selecionar_estabelecimento', args=(municipio,)))
        #return HttpResponseRedirect(reverse('agendar_vacinacao', args=(municipio,)))
        #return redirect('agendar_vacinacao', args=(1))

@login_required
def selecionar_estabelecimento(request, id):
    if request.method == 'GET':
        template_name = 'core/selecao-estabelecimento.html'
        municipio = Municipio.objects.get(pk=id)
        estabelecimentos = Estabelecimento.objects.filter(municipio=municipio).order_by('nomeFantasia')
        context = {
            'id': id,
            'estabelecimentos': estabelecimentos,
        }
        return render(request, template_name, context)
    if request.method == 'POST':
        estabelecimento = request.POST['estabelecimento_id']
        return HttpResponseRedirect(reverse('agendar_vacinacao', args=(estabelecimento,)))
        #return redirect('agendar_vacinacao', args=(1))

@login_required
def agendar_vacinacao(request, id):
    if request.method == 'GET':
        template_name='core/agendar-vacinacao.html'
        vacinas = Vacina.objects.all().order_by('nome')
        estabelecimento = Estabelecimento.objects.get(pk=id)
        horarios = HorarioAgenda.objects.filter(agenda__estabelecimento=estabelecimento, paciente__isnull=True)
        #horarios = HorarioAgenda.objects.filter(estabelecimento=estabelecimento).order_by('horario')
        context = {
            'vacinas': vacinas,
            'horarios': horarios,
            'estabelecimento': estabelecimento,
        }
        return render(request, template_name, context)
    if request.method == 'POST':
        vacina_id = request.POST['vacina_id']
        vacina = Vacina.objects.get(pk=vacina_id)
        #paciente_id = request.user.paciente.id
        #user = User.objects.get(pk=request.user.id)
        paciente = Paciente.objects.get(user=request.user)
        horario_id = request.POST['horario_id']
        horarioAgenda = HorarioAgenda.objects.get(pk=horario_id)
        horarioAgenda.vacina = vacina
        horarioAgenda.paciente = paciente
        horarioAgenda.save()
        messages.success(request, 'Agendamento realizado com sucesso')
        return redirect('dashboard_paciente')

@login_required
def registrar_vacina(request):
    if request.method == 'GET':
        template_name='core/registro-vacina-privada.html'
        vacinas = Vacina.objects.all().order_by('nome')
        context = {
            'vacinas': vacinas,
        }
        return render(request, template_name, context)
    if request.method == 'POST':
        vacina_id = request.POST['vacina_id']
        vacina = Vacina.objects.get(pk=vacina_id)
        data = request.POST['data']
        paciente = Paciente.objects.get(user=request.user)
        pacienteVacina = PacienteVacina(paciente=paciente, vacina=vacina, data=data)
        pacienteVacina.save()
        messages.success(request, 'Registro realizado com sucesso')
        return redirect('dashboard_paciente')

@login_required
def profissional_registro_data(request):
    if request.method == 'GET':
        template_name='core/profissional-registro-data.html'
        profissional = Profissional.objects.get(user=request.user)
        context = {
            'profissional': profissional,
        }
        return render(request, template_name, context)
    if request.method == 'POST':
        data = request.POST['data_estabelecimento']
        fila = 0
        fila_chamada = 0
        profissional = Profissional.objects.get(user=request.user)
        estabelecimento = Estabelecimento.objects.get(profissional=profissional)
        agenda = Agenda(data=data, fila=fila, fila_chamada=fila_chamada, estabelecimento=estabelecimento)
        agenda.save()
        hs = ('08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30')
        for horario in hs:
            horarioAgenda = HorarioAgenda(agenda=agenda,horario=horario, fila=0)
            horarioAgenda.save()
        messages.success(request, 'Data registrada com sucesso')
        return redirect('dashboard_profissional')

@login_required
def estoque(request):
    if request.method == 'GET':
        template_name = 'core/estoque.html'
        profissional = Profissional.objects.get(user=request.user)
        estabelecimento = Estabelecimento.objects.get(profissional=profissional)
        estoques = Estoque.objects.filter(estabelecimento=estabelecimento)
        context = {
            'estabelecimento': estabelecimento,
            'estoques': estoques,
        }
        return render(request, template_name, context)


def campo_vazio(campo):
    return not campo.strip()