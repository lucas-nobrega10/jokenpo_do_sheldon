import pygame
import sys
import os
import time
from jogo import JogoJokenpo, itens
from typing import Tuple, Dict

class InterfaceJogo:
    def __init__(self) -> None:
        """Inicializa a interface do jogo Jokenpô."""
        pygame.init()
        pygame.mixer.init()
        
        self.LARGURA_TELA, self.ALTURA_TELA = 800, 600
        self.FUNDO = (240, 248, 255)  # Alice Blue

        # Definição de cores em formato RGB
        self.PRETO = (0, 0, 0)
        self.BRANCO = (255, 255, 255)
        self.VERDE = (34, 139, 34)
        self.VERMELHO = (178, 34, 34)
        self.AZUL = (0, 102, 204)
        self.CINZA = (169, 169, 169)

        self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption("JOKENPÔ DO SHELDON")
        self.fonte_grande = pygame.font.Font(None, 64)
        self.fonte_media = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 32)
        self.jogo = JogoJokenpo()
        self.imagens = self.carregar_imagens()
        self.sons = self.carregar_sons()

    def carregar_imagens(self) -> Dict[str, pygame.Surface]:
        """Carrega e redimensiona as imagens dos itens do jogo.

        Retorna:
            Dict[str, pygame.Surface]: Dicionário contendo as imagens dos itens do jogo.
        """
        caminho_imagens = "imagens"
        imagens = {}
        for item in itens:
            imagens[item] = pygame.image.load(os.path.join(caminho_imagens, f"{item.lower()}.png"))
            imagens[item] = pygame.transform.scale(imagens[item], (120, 120))
        imagens["vitoria"] = pygame.transform.scale(pygame.image.load(os.path.join(caminho_imagens, "sheldon_feliz.png")), (200, 200))
        imagens["derrota"] = pygame.transform.scale(pygame.image.load(os.path.join(caminho_imagens, "sheldon_decepcionado.png")), (200, 200))
        return imagens

    def carregar_sons(self) -> Dict[str, pygame.mixer.Sound]:
        """Carrega os efeitos sonoros do jogo.

        Retorna:
            Dict[str, pygame.mixer.Sound]: Dicionário contendo os sons utilizados no jogo.
        """
        return {
            "vitoria": pygame.mixer.Sound("sons/vitoria.wav"),
            "derrota": pygame.mixer.Sound("sons/derrota.wav"),
            "empate": pygame.mixer.Sound("sons/empate.wav"),
            "clique": pygame.mixer.Sound("sons/clique.wav"),
        }

    def tocar_som(self, som: pygame.mixer.Sound) -> None:
        """Reproduz um efeito sonoro específico.

        Parâmetros:
            som (pygame.mixer.Sound): O som a ser reproduzido.
        """
        som.play()

    def exibir_texto(self, texto: str, fonte: pygame.font.Font, cor: Tuple[int, int, int], x: int, y: int, alinhamento: str = 'centro') -> None:
        """Exibe um texto na tela com o alinhamento especificado.

        Parâmetros:
            texto (str): O texto a ser exibido.
            fonte (pygame.font.Font): A fonte a ser utilizada para o texto.
            cor (Tuple[int, int, int]): A cor do texto em formato RGB.
            x (int): A posição x na tela.
            y (int): A posição y na tela.
            alinhamento (str): O alinhamento do texto ('centro', 'esquerda', 'direita').
        """
        texto_renderizado: pygame.Surface = fonte.render(texto, True, cor)
        if alinhamento == 'esquerda':
            texto_rect = texto_renderizado.get_rect(midleft=(x, y))
        elif alinhamento == 'direita':
            texto_rect = texto_renderizado.get_rect(midright=(x, y))
        else:
            texto_rect = texto_renderizado.get_rect(center=(x, y))
        self.tela.blit(texto_renderizado, texto_rect)

    def desenhar_botao(self, texto: str, x: int, y: int, largura: int, altura: int, cor_inativa: Tuple[int, int, int], cor_ativa: Tuple[int, int, int]) -> bool:
        """Desenha um botão interativo na tela e gerencia sua interação.

        Parâmetros:
            texto (str): O texto a ser exibido no botão.
            x (int): A posição x do botão.
            y (int): A posição y do botão.
            largura (int): A largura do botão.
            altura (int): A altura do botão.
            cor_inativa (Tuple[int, int, int]): A cor do botão quando não está ativo.
            cor_ativa (Tuple[int, int, int]): A cor do botão quando está ativo.

        Retorna:
            bool: True se o botão foi clicado, False caso contrário.
        """
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()[0]
        
        if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
            pygame.draw.rect(self.tela, cor_ativa, (x, y, largura, altura), border_radius=15)
            if clique:
                self.tocar_som(self.sons["clique"])
                return True
        else:
            pygame.draw.rect(self.tela, cor_inativa, (x, y, largura, altura), border_radius=15)
        
        self.exibir_texto(texto, self.fonte_pequena, self.BRANCO, x + largura/2, y + altura/2)
        return False

    def inicializar_jogo(self) -> Tuple[str, str, str, bool, float, bool, int]:
        """Inicializa as variáveis do jogo.

        Retorna:
            Tuple[str, str, str, bool, float, bool, int]: Variáveis iniciais do jogo.
        """
        escolha_jogador = None
        escolha_computador = None
        resultado = None
        mostrando_resultado = False
        tempo_espera = 0
        pontuacao_atualizada = False
        jogada_numero = 1
        return escolha_jogador, escolha_computador, resultado, mostrando_resultado, tempo_espera, pontuacao_atualizada, jogada_numero

    def exibir_escolhas(self, escolha_jogador: str, escolha_computador: str, tempo_espera: float) -> None:
        """Exibe as escolhas do jogador e do computador na tela.

        Parâmetros:
            escolha_jogador (str): A escolha do jogador.
            escolha_computador (str): A escolha do computador.
            tempo_espera (float): O tempo de espera para exibir as escolhas.
        """
        self.exibir_texto("Sua escolha:", self.fonte_pequena, self.PRETO, self.LARGURA_TELA/4, 200)
        self.tela.blit(self.imagens[escolha_jogador], (self.LARGURA_TELA/4 - 60, 230))
        
        if escolha_computador and time.time() - tempo_espera > 1:
            self.exibir_texto("Escolha do computador:", self.fonte_pequena, self.PRETO, 3*self.LARGURA_TELA/4, 200)
            self.tela.blit(self.imagens[escolha_computador], (3*self.LARGURA_TELA/4 - 60, 230))

    def exibir_resultado(self, resultado: str, tempo_espera: float) -> None:
        """Exibe o resultado da jogada na tela.

        Parâmetros:
            resultado (str): O resultado da jogada.
            tempo_espera (float): O tempo de espera para exibir o resultado.
        """
        if resultado and time.time() - tempo_espera > 2:
            cor_resultado = self.VERMELHO if resultado == "Derrota" else self.VERDE
            self.exibir_texto(resultado, self.fonte_media, cor_resultado, self.LARGURA_TELA/2, 420)

    def atualizar_pontuacao(self, arquivo, jogada_numero: int, escolha_jogador: str, escolha_computador: str, resultado: str) -> int:
        """Atualiza a pontuação e salva a jogada no arquivo.

        Parâmetros:
            arquivo: O arquivo onde as jogadas são registradas.
            jogada_numero (int): O número da jogada.
            escolha_jogador (str): A escolha do jogador.
            escolha_computador (str): A escolha do computador.
            resultado (str): O resultado da jogada.

        Retorna:
            int: O número da próxima jogada.
        """
        arquivo.write(f"Jogada {jogada_numero}: {escolha_jogador} vs {escolha_computador} - {resultado} | Pontos: Você {self.jogo.pontos_usuario}, Computador {self.jogo.pontos_computador}\n")
        return jogada_numero + 1

    def solicitar_nome_jogador(self) -> str:
        """Solicita o nome do jogador e retorna-o."""
        nome = ""
        digitando = True
        while digitando:
            self.tela.fill(self.FUNDO)
            self.exibir_texto("Digite seu nome:", self.fonte_media, self.AZUL, self.LARGURA_TELA/2, self.ALTURA_TELA/2 - 50)
            self.exibir_texto(nome, self.fonte_media, self.PRETO, self.LARGURA_TELA/2, self.ALTURA_TELA/2)
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if nome:  # Certifica-se de que o nome não está vazio
                            digitando = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += evento.unicode
        return nome

    def salvar_ranking(self, nome: str, pontos: int) -> None:
        """Salva a pontuação do jogador no arquivo de ranking."""
        with open("ranking.txt", "a") as arquivo:
            arquivo.write(f"{nome}: {pontos}\n")

    def exibir_ranking(self) -> None:
        """Exibe o ranking dos jogadores em ordem decrescente de pontuação."""
        self.tela.fill(self.FUNDO)
        self.exibir_texto("RANKING", self.fonte_grande, self.AZUL, self.LARGURA_TELA/2, 50)
        
        try:
            with open("ranking.txt", "r") as arquivo:
                ranking = []
                for linha in arquivo:
                    nome, pontos = linha.strip().split(": ")
                    ranking.append((nome, int(pontos)))  # Armazena como tupla (nome, pontos)

                # Classifica o ranking em ordem decrescente de pontos
                ranking.sort(key=lambda x: x[1], reverse=True)

                # Exibe o ranking
                for i, (nome, pontos) in enumerate(ranking):
                    self.exibir_texto(f"{i + 1}º: {nome} - {pontos} pontos", self.fonte_pequena, self.PRETO, self.LARGURA_TELA/2, 120 + i*30)
        except FileNotFoundError:
            self.exibir_texto("Nenhum ranking disponível.", self.fonte_pequena, self.PRETO, self.LARGURA_TELA/2, 120)
        
        pygame.display.flip()
        time.sleep(5)  # Exibe o ranking por 5 segundos

    def jogar(self) -> None:
        """Função principal do jogo, gerencia a lógica e a interação do jogador."""
        nome_jogador = self.solicitar_nome_jogador()
        escolha_jogador, escolha_computador, resultado, mostrando_resultado, tempo_espera, pontuacao_atualizada, jogada_numero = self.inicializar_jogo()

        # Abre o arquivo para registrar as jogadas em modo de escrita (limpa o conteúdo anterior)
        with open("jogadas.txt", "w") as arquivo:
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                self.tela.fill(self.FUNDO)
                
                self.exibir_texto("JOKENPÔ DO SHELDON", self.fonte_grande, self.AZUL, self.LARGURA_TELA/2, 50)
                self.exibir_texto(f"Você: {self.jogo.pontos_usuario}", self.fonte_media, self.VERDE, 150, 120, 'esquerda')
                self.exibir_texto(f"Computador: {self.jogo.pontos_computador}", self.fonte_media, self.VERMELHO, self.LARGURA_TELA - 150, 120, 'direita')
                
                if escolha_jogador:
                    self.exibir_escolhas(escolha_jogador, escolha_computador, tempo_espera)
                    self.exibir_resultado(resultado, tempo_espera)
                    
                    if resultado and time.time() - tempo_espera > 2:
                        if not mostrando_resultado:
                            mostrando_resultado = True
                            if resultado == "Vitória":
                                self.tocar_som(self.sons["vitoria"])
                            elif resultado == "Derrota":
                                self.tocar_som(self.sons["derrota"])
                            else:
                                self.tocar_som(self.sons["empate"])
                        if not pontuacao_atualizada and time.time() - tempo_espera > 3:
                            pontuacao_atualizada = True
                            jogada_numero = self.atualizar_pontuacao(arquivo, jogada_numero, escolha_jogador, escolha_computador, resultado)
                
                for i, item in enumerate(itens):
                    if self.desenhar_botao(item, 50 + i*150, 500, 140, 50, self.VERDE, self.AZUL) and not escolha_jogador:
                        escolha_jogador = item
                        escolha_computador, resultado = self.jogo.escolher_jogada(escolha_jogador)
                        tempo_espera = time.time()
                        mostrando_resultado = False
                        pontuacao_atualizada = False
                
                if self.desenhar_botao("Menu", 20, 20, 80, 30, self.AZUL, (100, 150, 255)):
                    return
                
                if mostrando_resultado and time.time() - tempo_espera > 4:
                    if self.jogo.pontos_usuario >= 10 or self.jogo.pontos_computador >= 10:
                        self.mostrar_resultado_final()
                        self.salvar_ranking(nome_jogador, self.jogo.pontos_usuario)
                        self.exibir_ranking()
                        self.jogo.zerar_pontos()  # Zera o placar após o resultado final
                        return
                    escolha_jogador = None
                    escolha_computador = None
                    resultado = None
                    mostrando_resultado = False
                
                pygame.display.flip()
                pygame.time.delay(50)  # Adiciona um pequeno atraso para controlar a taxa de atualização

    def mostrar_resultado_final(self) -> None:
        """Exibe o resultado final do jogo e aguarda um tempo antes de retornar ao menu.

        Esta função mostra se o jogador ganhou ou perdeu e exibe a imagem correspondente.
        """
        self.tela.fill(self.FUNDO)
        if self.jogo.pontos_usuario >= 10:
            self.tela.blit(self.imagens["vitoria"], (self.LARGURA_TELA/2 - 100, 100))
            self.exibir_texto("Parabéns, você ganhou!", self.fonte_grande, self.VERDE, self.LARGURA_TELA/2, 350)
        else:
            self.tela.blit(self.imagens["derrota"], (self.LARGURA_TELA/2 - 100, 100))
            self.exibir_texto("Decepcionante... Você perdeu!", self.fonte_grande, self.VERMELHO, self.LARGURA_TELA/2, 350)
        
        pygame.display.flip()
        time.sleep(5)  # Mostra a tela de resultado por 5 segundos

    def regras(self) -> None:
        """Exibe as regras do jogo em uma tela separada.

        Esta função apresenta as regras do jogo e aguarda a interação do usuário para retornar ao menu.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.tela.fill(self.FUNDO)
            self.exibir_texto("REGRAS", self.fonte_grande, self.AZUL, self.LARGURA_TELA/2, 50)
            
            regras_texto: list[str] = [
                "Pedra vence Tesoura e Lagarto",
                "Papel vence Pedra e Spock",
                "Tesoura vence Papel e Lagarto",
                "Lagarto vence Papel e Spock",
                "Spock vence Pedra e Tesoura",
                "",
                "Pesos dos itens:",
                "Papel: 1, Tesoura: 2, Pedra: 3, Lagarto: 4, Spock: 5",
                "",
                "Ao vencer, você ganha pontos iguais ao peso do seu item",
                "e o oponente perde pontos iguais ao peso do item dele.",
                "",
                "O jogo termina quando um jogador atinge 10 pontos.",
            ]
            
            for i, regra in enumerate(regras_texto):
                self.exibir_texto(regra, self.fonte_pequena, self.PRETO, self.LARGURA_TELA/2, 120 + i*30)
            
            if self.desenhar_botao("Menu", 20, 20, 80, 30, self.AZUL, (100, 150, 255)):
                return
            
            pygame.display.flip()

    def referencias(self) -> None:
        """Exibe as referências do jogo em uma tela separada.

        Esta função apresenta informações sobre a origem do jogo e aguarda a interação do usuário para retornar ao menu.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.tela.fill(self.FUNDO)
            self.exibir_texto("REFERÊNCIAS", self.fonte_grande, self.AZUL, self.LARGURA_TELA/2, 50)
            
            referencias_texto: list[str] = [
                "Este jogo é baseado na versão de Pedra, Papel,",
                "Tesoura, Lagarto, Spock criada por Sam Kass e",
                "Karen Bryla, popularizada por Sheldon Cooper",
                "na série de TV 'The Big Bang Theory'.",
                "",
                "Desenvolvido por: Eduardo Vinícius e Lucas Fernando",
            ]
            
            for i, referencia in enumerate(referencias_texto):
                self.exibir_texto(referencia, self.fonte_pequena, self.PRETO, self.LARGURA_TELA/2, 150 + i*35)
            
            if self.desenhar_botao("Menu", 20, 20, 80, 30, self.AZUL, (100, 150, 255)):
                return
            
            pygame.display.flip()

    def zerar_pontos(self) -> None:
        """Zera a pontuação do jogador e do computador.

        Esta função é chamada para reiniciar a pontuação durante o jogo.
        """
        self.jogo.zerar_pontos()