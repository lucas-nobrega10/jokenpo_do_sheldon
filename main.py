import pygame
import sys
from interface import InterfaceJogo

def menu_principal(interface: InterfaceJogo) -> None:
    """Função do menu principal do jogo.

    Esta função exibe o menu inicial e gerencia a navegação entre as opções disponíveis.
    """
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        interface.tela.fill(interface.FUNDO)
        interface.exibir_texto("JOKENPÔ DO SHELDON", interface.fonte_grande, interface.AZUL, interface.LARGURA_TELA/2, 100)
        
        largura_botao: int = 300
        altura_botao: int = 70
        
        if interface.desenhar_botao("Jogar", interface.LARGURA_TELA/2 - largura_botao/2, 200, largura_botao, altura_botao, interface.VERDE, (0, 180, 0)):
            print("Botão Jogar pressionado")  # Depuração
            interface.jogar()
        if interface.desenhar_botao("Regras", interface.LARGURA_TELA/2 - largura_botao/2, 300, largura_botao, altura_botao, interface.AZUL, (0, 150, 255)):
            interface.regras()
        if interface.desenhar_botao("Referências", interface.LARGURA_TELA/2 - largura_botao/2, 400, largura_botao, altura_botao, interface.AZUL, (0, 150, 255)):
            interface.referencias()
        if interface.desenhar_botao("Zerar Placar", interface.LARGURA_TELA/2 - largura_botao/2, 500, largura_botao, altura_botao, interface.VERMELHO, (255, 50, 50)):
            interface.zerar_pontos()
        if interface.desenhar_botao("Sair", interface.LARGURA_TELA/2 - largura_botao/2, 600, largura_botao, altura_botao, interface.CINZA, (100, 100, 100)):
            pygame.quit()
            sys.exit()
        
        interface.exibir_texto(f"Você: {interface.jogo.pontos_usuario}", interface.fonte_media, interface.VERDE, 150, 30, 'esquerda')
        interface.exibir_texto(f"Computador: {interface.jogo.pontos_computador}", interface.fonte_media, interface.VERMELHO, interface.LARGURA_TELA - 150, 30, 'direita')
        
        pygame.display.flip()

def main() -> None:
    """Função principal que inicia o menu principal."""
    interface = InterfaceJogo()  # Instancia a interface do jogo
    pygame.mixer.music.load("sons/musica_fundo.mp3")
    pygame.mixer.music.set_volume(0.19)
    pygame.mixer.music.play(-1)  # Inicia a música de fundo em loop

    menu_principal(interface)

# Ponto de entrada do programa
if __name__ == "__main__":
    main()  # Inicia o jogo chamando a função principal