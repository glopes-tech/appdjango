from django.contrib import admin
from .models import Enquete, Opcao, Pergunta, Aluno, AreaInteresse, Resposta, MultiplaEscolhaResposta, AreaInteresse, AlunoInteresse

admin.site.register(Enquete)
admin.site.register(Pergunta)
admin.site.register(Opcao)
admin.site.register(Aluno)
admin.site.register(Resposta)
admin.site.register(MultiplaEscolhaResposta)
admin.site.register(AreaInteresse)
admin.site.register(AlunoInteresse)