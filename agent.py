import random
import os

ARQUIVO_MEMORIA = "intelligentAgent/conhecimento.txt"

class AgenteForca:

    # Construtor da classe, e é onde nosso agente inteligente "nasce".
    # Quando se refere com self.(função), ele diz que essa variável pertence a esse agente
    # específico que tá jogando o jogo. Com isso, conseguimos atender ao requisito de ser autônomo e não
    # dependemos tanto mais de variáveis globais.

    def __init__(self):
        self.conhecimento = self.carregar_memoria()
        self.letras_erradas = set()
        self.letras_certas = set()
        self.tentativas_restantes = 6
        self.mascara = []

    def carregar_memoria(self):

        # Roda a leitura do conhecimento.txt e, caso não houver esse arquivo, ele vai criar uma lista
        # com zero itens e vai começar a armazenar lá os valores aprendidos (ver função aprender_palavra, que
        # "casa" com esse requisito). Com isso, remove as quebras de linhas que colocamos ao armazenar as palavras,
        # e transforma tudo em minúsculo (IMPORTANTE!!, trata muitas excessões.)

        if not os.path.exists(ARQUIVO_MEMORIA):
            return []
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return [linha.strip().lower() for linha in f.readlines()]

    def aprender_palavra(self, nova_palavra):

        # Função pra aprender as palavras, no caso, escrever lá no txt. Faz parte do tratamento de exceções
        # e, dado o tratamento, começa: ele olha na sua memória, ve se tá lá, se não tá, inclui. depois, adiciona
        # a nova linha com o conhecimento novo pra que o aprendizado seja contínuo (cumprindo mais um requisito).

        nova_palavra = nova_palavra.strip().lower()
        if nova_palavra not in self.conhecimento:
            self.conhecimento.append(nova_palavra)
            with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as f:
                f.write(f"\n{nova_palavra}")
            print(f"-> O agente aprendeu uma nova palavra: {nova_palavra}")
        else:
            print("-> O agente já conhecia essa palavra.")

    def filtrar_candidatas(self):

        # Percebe o ambiente, e filtra o dicionario baseado no que enxerga. Criamos um array vazio que guarda as palavras que,
        # dados os testes, vão sobrevivendo e se tornando nossos candidatos a escolha. Temos algumas condições:
        # I. Se a palavra que o usuário pensou tiver 5 letras, e a palavra do conhecimento tiver mais ou menos letras,
        # o agente entende que não é ela e prossegue.
        # II. Aqui, MUITO IMPORTANTE pq, se a posição não é um "buraco" e a letra da máscara for diferente da letra
        # na mesma posição na palavra candidata, a gente seta o booleano como False e prossegue novamente.
        # III. Finalmente, verifica se a palavra candidata tem alguma letra que o agente já chutou e errou antes (o que não
        # verificamos ainda anteriormente). Novamente, mudamos o booleano que é CRUCIAL nessa verificação
        # De forma geral, simula a percepção do ambiente em uma forma de "funil", e, o que cai em candidatas ao final,
        # é justamente tudo aquilo que é logicamente possível até o momento e cabe ao agente prosseguir com elas.

        candidatas = []
        for palavra in self.conhecimento:
            # I. Filtra por tamanho
            if len(palavra) != len(self.mascara):
                continue
            
            # II. Filtra por letras já reveladas
            bateu = True
            for i, letra in enumerate(self.mascara):
                if letra != '_' and letra != palavra[i]:
                    bateu = False
                    break
            
            # III. Filtra se a palavra tem letras que sabemos que NÃO existem
            if any(letra in palavra for letra in self.letras_erradas):
                bateu = False
            
            if bateu:
                candidatas.append(palavra)

        return candidatas

    def tomar_decisao(self, candidatas):

        # Aqui, é baseado na autonomia e na independência pra tomar decisões, de tentar uma
        # letra ou a palavra inteira de vez. Assim, temos uma lógica pra quando ele vai tentar
        # a letra, ou a palavra inteira. Tentamos implementar as decisões mentais que temos ao
        # jogar o jogo da forca com base na lógica humana.
        
        # Lógica de chutar caso no array candidatas só sobrar um valor, após passar pelo funil
        # da etapa anterior.
        if len(candidatas) == 1:
            return "CHUTE", candidatas[0]

        # LÓGICA IMPORTANTE DEMAIS PRO AGENTE "PENSAR":

        # Por meio de um dicionário, percorre as candidatas e temos mais uma lógica, em que só conta
        # uma letra se ele ainda não tentou ela, evitando chutar as mesmas letras se já tiver tentado,
        # implementando um laço aninhado com uma condicional, temos o seguinte fluxo:

        # Olha para as candidatas, pega letra por letra, se não chutamos tal palavra, adiciona no dic.
        # Depois de percorrer as candidatas, faça uma lógica de verificação se está no dicionário ou não,
        # e depois, pega aquela com maior quantidade dentro do dicionário e chuta essa letra. Assim, garantimos
        # um chute mais "seguro", e não aleatório.

        contagem = {}
        for palavra in candidatas:
            for letra in palavra:
                if letra not in self.letras_certas and letra not in self.letras_erradas:
                    contagem[letra] = contagem.get(letra, 0) + 1
        
        # Aqui, é um plano B: se contagem está vazio, vamos ter um plano B de como agir.
        # Peguei as letras mais frequentes na língua portuguesa, em que as vogais vem primeiro e depois
        # as consoantes, já que as vogais são bem mais frequentes. A variável alfabeto previne do agente
        # ficar perdido e não chutar qualquer coisa aleatória.

        # Se percorrer todas essas comuns e perceber que já usou todas, ele assume que não tem mais chances de ganhar
        # e joga a toalha retornando "DESISTO".

        # De forma geral, o bloco de código é a heurística humana de "chutar o obvio" quando não se sabe a resposta exata.

        if not contagem:
            alfabeto = "aeiosrntdmulc"
            for l in alfabeto:
                if l not in self.letras_certas and l not in self.letras_erradas:
                    return "LETRA", l
            return "DESISTO", None

        # O agente identifica qual letra teve mais votos anteriormente e traz essa decisão pra que
        # o jogo possa executar ela.

        melhor_letra = max(contagem, key=contagem.get)
        return "LETRA", melhor_letra

    def jogar(self):

        # Aqui, eh a função que conecta o nosso "cérebro" ao jogo mesmo, e vai chamando as funções
        # declaradas acima. Investimos um bom tempo na progressão visual que o Sr. solicitou para acompanhar
        # o processo do agente. Com ele, também fizemos alguns tratamentos de entrada, caso o usuário
        # que for jogar digitar de forma estúpida (infelizmente faz parte da vida).

        print("\n--- INICIANDO JOGO DA FORCA ---")
        print("Pense em uma palavra, o Agente tentará adivinhar.")
        
        try:
            tamanho = int(input("Quantas letras tem a sua palavra? "))
        except ValueError:
            print("Digite um número.")
            return

        # Cria o tabuleiro vazio
        self.mascara = ['_'] * tamanho

        # O loop do jogo começa aqui e só para quando o número de tentativas restantes for 0, ou seja, após a última tentativa
        # do jogador.
        while self.tentativas_restantes > 0:
            print(f"\nEstado: {' '.join(self.mascara)}")
            print(f"Vidas: {self.tentativas_restantes} | Erros: {list(self.letras_erradas)}")
            
            candidatas = self.filtrar_candidatas()
            print(f"(O agente pensou em {len(candidatas)} palavras possíveis)")

            tipo, palpite = self.tomar_decisao(candidatas)

            if tipo == "DESISTO":
                print("O agente não sabe mais o que chutar.")
                break
            
            if tipo == "CHUTE":
                print(f"-> O agente decidiu arriscar a palavra: '{palpite}'")
                resposta = input("Ele acertou? (s/n): ").lower()
                if resposta == 's':
                    print("O AGENTE VENCEU!")
                    return
                else:
                    print("O agente errou o chute e perdeu o jogo. Nice try! (NT)")
                    self.letras_erradas.add(palpite)
                    self.tentativas_restantes = 0
                    break

            elif tipo == "LETRA":
                print(f"-> O agente chutou a letra: '{palpite.upper()}'")
                resposta = input("Essa letra existe na palavra? (s/n): ").lower()

                if resposta == 's':
                    self.letras_certas.add(palpite)
                    print("Onde está a letra? (digite as posições separadas por espaço, começando em 1)")
                    print("Exemplo: se a palavra é BOLA e ele chutou A, digite: 4")
                    posicoes = input("Posições: ").split()
                    
                    # Mais um tratamento de entrada, mas agora para a resposta de "posição", caso
                    # o jogador for novamente estúpido.
                    try:
                        for pos in posicoes:
                            idx = int(pos) - 1
                            if 0 <= idx < len(self.mascara):
                                self.mascara[idx] = palpite
                    except:
                        print("Erro ao ler posições. O agente ficou confuso.")
                    
                    if '_' not in self.mascara:
                        print(f"O AGENTE VENCEU! A palavra era {''.join(self.mascara)}")
                        return
                else:
                    self.letras_erradas.add(palpite)
                    self.tentativas_restantes -= 1

        # FIM DO JOGO, PERDEU
        print("\n--- FIM DE JOGO ---")
        print("O agente não conseguiu adivinhar.")
        palavra_real = input("Qual era a palavra correta? ").strip().lower()
        self.aprender_palavra(palavra_real)

if __name__ == "__main__":
    jogo = AgenteForca()
    jogo.jogar()