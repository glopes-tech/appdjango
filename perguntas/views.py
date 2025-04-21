from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Enquete, Pergunta, Opcao, Resposta, MultiplaEscolhaResposta
from django import forms

class RespostaForm(forms.Form):
    def __init__(self, perguntas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for pergunta in perguntas:
            if pergunta.tipo == 'unica':
                self.fields[f'pergunta_{pergunta.id}'] = forms.ModelChoiceField(
                    queryset=Opcao.objects.filter(pergunta=pergunta),
                    widget=forms.RadioSelect(),
                    label=pergunta.texto,
                    required=pergunta.obrigatoria
                )
            elif pergunta.tipo == 'multipla':
                self.fields[f'pergunta_{pergunta.id}'] = forms.ModelMultipleChoiceField(
                    queryset=Opcao.objects.filter(pergunta=pergunta),
                    widget=forms.CheckboxSelectMultiple(),
                    label=pergunta.texto,
                    required=pergunta.obrigatoria
                )
            elif pergunta.tipo == 'texto':
                self.fields[f'pergunta_{pergunta.id}'] = forms.CharField(
                    widget=forms.Textarea,
                    label=pergunta.texto,
                    required=pergunta.obrigatoria
                )

def listar_enquetes(request):
    enquetes = Enquete.objects.filter(ativa=True)
    return render(request, 'perguntas/listar_enquetes.html', {'enquetes': enquetes})

def responder_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id, ativa=True)
    perguntas = enquete.pergunta_set.all().order_by('ordem')

    if request.method == 'POST':
        form = RespostaForm(perguntas, request.POST)
        if form.is_valid():
            aluno_nome = "Aluno Teste"  # Em um cenário real, você teria a autenticação de usuários
            aluno_email = "teste@example.com"
            aluno, created = aluno.objects.get_or_create(nome=aluno_nome, email=aluno_email)

            for pergunta in perguntas:
                campo = f'pergunta_{pergunta.id}'
                if campo in form.cleaned_data:
                    resposta = Resposta.objects.create(aluno=aluno, pergunta=pergunta)
                    if pergunta.tipo == 'unica':
                        opcao = form.cleaned_data[campo]
                        resposta.opcao_unica = opcao
                        resposta.save()
                    elif pergunta.tipo == 'multipla':
                        opcoes = form.cleaned_data[campo]
                        for opcao in opcoes:
                            MultiplaEscolhaResposta.objects.create(resposta=resposta, opcao=opcao)
                    elif pergunta.tipo == 'texto':
                        resposta.texto_livre = form.cleaned_data[campo]
                        resposta.save()
            return redirect(reverse('enquete_respondida', args=[enquete_id]))
    else:
        form = RespostaForm(perguntas)

    return render(request, 'perguntas/responder_enquete.html', {'enquete': enquete, 'form': form})

def enquete_respondida(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id, ativa=True)
    return render(request, 'perguntas/enquete_respondida.html', {'enquete': enquete})

def exibir_resultados(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id, ativa=True)
    perguntas = enquete.pergunta_set.all()
    resultados = []

    for pergunta in perguntas:
        resultado_pergunta = {'pergunta': pergunta.texto, 'tipo': pergunta.tipo}
        if pergunta.tipo == 'unica' or pergunta.tipo == 'multipla':
            opcoes_com_contagem = []
            total_respostas = pergunta.resposta_set.count()
            for opcao in pergunta.opcao_set.all():
                contagem = 0
                if pergunta.tipo == 'unica':
                    contagem = Resposta.objects.filter(pergunta=pergunta, opcao_unica=opcao).count()
                elif pergunta.tipo == 'multipla':
                    contagem = MultiplaEscolhaResposta.objects.filter(opcao=opcao, resposta__pergunta=pergunta).count()

                porcentagem = (contagem / total_respostas * 100) if total_respostas > 0 else 0
                opcoes_com_contagem.append({'opcao': opcao.texto, 'contagem': contagem, 'porcentagem': f'{porcentagem:.2f}%'})
            resultado_pergunta['opcoes'] = opcoes_com_contagem
            resultado_pergunta['total_respostas'] = total_respostas
        elif pergunta.tipo == 'texto':
            respostas_texto = Resposta.objects.filter(pergunta=pergunta).values_list('texto_livre', flat=True).exclude(texto_livre__isnull=True).exclude(texto_livre__exact='')
            resultado_pergunta['respostas_texto'] = respostas_texto.order_by('-data_resposta')
            resultado_pergunta['total_respostas'] = respostas_texto.count()
        resultados.append(resultado_pergunta)

    context = {'enquete': enquete, 'resultados': resultados}
    return render(request, 'perguntas/exibir_resultados.html', context)