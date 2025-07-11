from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import AreaInteresse, Enquete, Pergunta, Resposta, Aluno
from .forms import RespostaForm, CriarEnqueteForm, RegistrarAlunoForm, FiltrarEnquetesForm
from django.contrib import messages
from django.utils import timezone

def index(request):
    now = timezone.now()
    return render(request, 'perguntas/home.html', {'now': now})

class EnqueteCreateView(CreateView):
    model = Enquete
    form_class = CriarEnqueteForm  # Use o form para a criação
    template_name_suffix = '_criar'  # Nome do template para criar
    success_url = reverse_lazy('listar_enquetes')  # Redireciona para a lista após criar

# 2.2 Classe Editar
class EnqueteUpdateView(UpdateView):
    model = Enquete
    form_class = CriarEnqueteForm  # Use o mesmo form para edição
    template_name_suffix = '_editar'  # Nome do template para editar
    success_url = reverse_lazy('listar_enquetes')  # Redireciona para a lista após editar

# 2.3 Classe Detalhar
class EnqueteDetailView(DetailView):
    model = Enquete
    template_name_suffix = '_detalhe'  # Nome do template para detalhar

# 2.4 Classe Listar
class EnqueteListView(ListView):
    model = Enquete
    context_object_name = 'enquetes'  # Nome para usar a lista no template
    template_name = 'perguntas/listar_enquetes.html'  # Caminho para o template

# 2.5 Classe Deletar
class EnqueteDeleteView(DeleteView):
    model = Enquete
    success_url = reverse_lazy('listar_enquetes')  # Redireciona para a lista após deletar
    template_name_suffix = '_deletar'  # Nome do template para deletar

#def gerenciar_enquetes(request):
#    filtro_form = FiltrarEnquetesForm(request.GET)
#    enquetes = Enquete.objects.all().order_by('-data_criacao')

#    if filtro_form.is_valid():
#        titulo = filtro_form.cleaned_data.get('titulo')
#        status = filtro_form.cleaned_data.get('status')

#        if titulo:
#            enquetes = enquetes.filter(titulo__icontains=titulo)
#        if status == 'ativa':
#            enquetes = enquetes.filter(ativa=True)
#        elif status == 'encerrada':
#            enquetes = enquetes.filter(ativa=False)

#    enquete_id = request.GET.get('enquete_id')
#    responder_form = None
#    enquete_responder = None
#    resultados = None
#    enquete_resultados = None

#    if enquete_id:
#        enquete_responder = get_object_or_404(Enquete, pk=enquete_id, ativa=True)
#        perguntas = #enquete_responder.pergunta_set.all().order_by('ordem')
#        responder_form = RespostaForm(perguntas)

#        if request.method == 'POST':
#            responder_form = RespostaForm(perguntas, request.POST)
#            if responder_form.is_valid():
#                aluno, created = Aluno.objects.get_or_create(nome="Aluno Teste", email="teste@example.com") # Adapte para autenticação real
#                for pergunta in perguntas:
#                    campo = f'pergunta_{pergunta.id}'
#                    if campo in responder_form.cleaned_data:
#                        resposta = Resposta.objects.create(aluno=aluno, pergunta=pergunta)
                        # ... (lógica para salvar diferentes tipos de respostas)
#                messages.success(request, 'Respostas enviadas com sucesso!')
#                return redirect(reverse('gerenciar_enquetes') + f'?enquete_id={enquete_id}')

#        if request.GET.get('resultados') == 'true':
#            enquete_resultados = get_object_or_404(Enquete, pk=enquete_id)
            # ... (lógica para obter os resultados da enquete)

#    return render(request, 'perguntas/enquetes/gerenciar_enquetes.html', {
#        'enquetes': enquetes,
#        'filtro_form': filtro_form,
#        'responder_form': responder_form,
#        'enquete_responder': enquete_responder,
#        'resultados': resultados,
#        'enquete_resultados': enquete_resultados,
#    })

def responder_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    perguntas = Pergunta.objects.filter(enquete=enquete)
    if request.method == 'POST':
        form = RespostaForm(perguntas, request.POST)
        if form.is_valid():
            for pergunta in perguntas:
                if pergunta.tipo == 'texto':
                    resposta_texto = form.cleaned_data[f'pergunta_{pergunta.id}']
                    Resposta.objects.create(
                        pergunta=pergunta,
                        resposta_texto=resposta_texto,
                    )
                elif pergunta.tipo in ['unica', 'multipla']:
                    opcoes_selecionadas = form.cleaned_data[f'pergunta_{pergunta.id}']
                    for opcao in opcoes_selecionadas:
                        Resposta.objects.create(
                            pergunta=pergunta,
                            opcao_selecionada=opcao,
                        )
            return redirect('enquete_respondida')
    else:
        form = RespostaForm(perguntas)
    return render(request, 'perguntas/responder_enquete.html', {'enquete': enquete, 'form': form})

def enquete_respondida(request):
    return render(request, 'perguntas/enquete_respondida.html')
    
def registrar_aluno(request):
    if request.method == 'POST':
        form = RegistrarAlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno registrado com sucesso!')
            return redirect('perguntas/usuarios/gerenciar')
    else:
        form = RegistrarAlunoForm()
    return render(request, 'perguntas/usuarios/gerenciar.html', {'registro_form': form})

def gerenciar_usuarios(request):
    alunos = Aluno.objects.all()
    registro_form = RegistrarAlunoForm()
    return render(request, 'perguntas/usuarios/gerenciar.html', {'alunos': alunos, 'registro_form': registro_form})

def criar_enquete(request):
    if request.method == 'POST':
        form = CriarEnqueteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enquete criada com sucesso!')
            return redirect(reverse('admin:perguntas_enquete_add'))
    else:
        form = CriarEnqueteForm()
    return render(request, 'perguntas/admin/criar_enquete.html', {'form': form})

def listar_areas_interesse(request):
    areas = AreaInteresse.objects.all().order_by('nome')
    return render(request, 'perguntas/areas/listar_areas_interesse.html', {'areas': areas})