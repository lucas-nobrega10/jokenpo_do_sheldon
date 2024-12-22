import random
from typing import Tuple, Dict

# Lista de itens do jogo com seus respectivos pesos
itens: Dict[str, int] = {
    "Papel": 1,
    "Tesoura": 2,
    "Pedra": 3,
    "Lagarto": 4,
    "Spock": 5
}

class JogoJokenpo:
    def __init__(self) -> None:
        """Inicializa o jogo Jokenpô, configurando a pontuação inicial."""
        self.pontos_usuario: int = 0
        self.pontos_computador: int = 0

    def escolher_jogada(self, escolha_jogador: str) -> Tuple[str, str]:
        """Determina a jogada do computador e o resultado da partida.

        Parâmetros:
            escolha_jogador (str): A escolha do jogador.

        Retorna:
            Tuple[str, str]: A escolha do computador e o resultado da partida.
        """
        escolha_computador = random.choice(list(itens.keys()))
        resultado = self.determinar_vencedor(escolha_jogador, escolha_computador)
        return escolha_computador, resultado

    def determinar_vencedor(self, escolha_jogador: str, escolha_computador: str) -> str:
        """Determina o vencedor da partida.

        Parâmetros:
            escolha_jogador (str): A escolha do jogador.
            escolha_computador (str): A escolha do computador.

        Retorna:
            str: O resultado da partida ("Vitória", "Derrota" ou "Empate").
        """
        if escolha_jogador == escolha_computador:
            return "Empate"

        vitorias = {
            "Pedra": ["Tesoura", "Lagarto"],
            "Papel": ["Pedra", "Spock"],
            "Tesoura": ["Papel", "Lagarto"],
            "Lagarto": ["Papel", "Spock"],
            "Spock": ["Pedra", "Tesoura"]
        }

        if escolha_computador in vitorias[escolha_jogador]:
            self.pontos_usuario += itens[escolha_jogador]
            self.pontos_computador = max(0, self.pontos_computador - itens[escolha_computador])
            return "Vitória"
        else:
            self.pontos_usuario = max(0, self.pontos_usuario - itens[escolha_jogador])
            self.pontos_computador += itens[escolha_computador]
            return "Derrota"

    def zerar_pontos(self) -> None:
        """Zera a pontuação do jogador e do computador."""
        self.pontos_usuario = 0
        self.pontos_computador = 0
        print("Placar zerado!")