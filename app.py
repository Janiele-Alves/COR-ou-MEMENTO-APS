from flask import Flask, render_template
app = Flask(__name__, template_folder="template")

class Memento:
    def __init__(self, validadores):
        self._state = validadores

    def get_state(self):
        return self._state

class ValidadorInscricao:
    def __init__(self):
        self.proximo = None
        self._memento = None

    def definir_proximo(self, proximo):
        self.proximo = proximo

    def validar(self, aluno):
        pass

    def salvar_estado(self):
        self._memento = Memento(self)

    def restaurar_estado(self):
        if self._memento:
            self.__dict__ = self._memento.get_state().__dict__

class ValidadorIdade(ValidadorInscricao):
    def validar(self, aluno):
        if aluno.idade < 18:
            return False
        if self.proximo:
            return self.proximo.validar(aluno)
        return True

class ValidadorPagamento(ValidadorInscricao):
    def validar(self, aluno):
        if not aluno.pagamento_em_dia:
            return False
        if self.proximo:
            return self.proximo.validar(aluno)
        return True

class ValidadorAluno(ValidadorInscricao):
    def validar(self, aluno):
        if aluno.idade >= 18 and aluno.pagamento_em_dia:
            return True
        if self.proximo:
            return self.proximo.validar(aluno)
        return True

class Aluno:
    def __init__(self, nome, idade, pagamento_em_dia):
        self.nome = nome
        self.idade = idade
        self.pagamento_em_dia = pagamento_em_dia

@app.route('/')
def index():
    aluno1 = Aluno("Maria", 14, True)
    aluno2 = Aluno("Janiele", 30, False)
    aluno3 = Aluno("Janiel", 30, True)

    validador_idade = ValidadorIdade()
    validador_pagamento = ValidadorPagamento()
    validador_aluno = ValidadorAluno()

    validador_idade.definir_proximo(validador_pagamento)

    validador_idade.salvar_estado()
    validador_pagamento.salvar_estado()
    validador_aluno.salvar_estado()

    validador_idade.restaurar_estado()
    validador_pagamento.restaurar_estado()


    resultado_validacao3 = "O aluno está apto para a academia." if validador_aluno.validar(aluno3) else "O aluno não está apto para a academia."
    resultado_validacao1 = "O aluno está apto para a academia." if validador_idade.validar(aluno1) else "O aluno é menor de idade."
    resultado_validacao2 = "O aluno está apto para a academia." if validador_pagamento.validar(aluno2) else "O aluno está com a mensalidade atrasada."
    return render_template('index.html', resultado_validacao1=resultado_validacao1, resultado_validacao2=resultado_validacao2, resultado_validacao3=resultado_validacao3)

if __name__ == '__main__':
    app.run(debug=True)
