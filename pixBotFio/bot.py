import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt

class BotState:
    INITIALIZING = 0
    SEARCHING = 0
    MOVING = 0
    MINING = 0
    BACKTRACKING = 4


class BottleBot:

    # Constante
    INITIALIZING_SECONDS = 2
    MINING_SECONDS = 14
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    IGNORE_RADIUS = 130
    TOOLTIP_MATCH_THRESHOLD = 0.76

    # propriedades threading
    stopped = True
    lock = None

    # Propriedades
    state = None
    targets = []
    screenshot = None
    timestamp = None
    window_offset = (0,0)
    wincap_w = 0
    wincap_h = 0
    limestone_tooltip = None
    click_history = []
    
    def __init__(self, window_offset, window_size):
        #cria um objeto thead lock
        self.lock = Lock()

        # para traduzir as posições das janelas em posições da tela, 
        # é mais fácil obter apenas os deslocamentos e o tamanho da janela do 
        # WindowCapture em vez de passar o objeto inteiro
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]

        # pré-carregar a imagem da agulha usada para confirmar nossa detecção de objeto
        self.limestone_tooltip = cv.imread('img/click_to_cook.png', cv.IMREAD_UNCHANGED)

        # Inicializa o bot
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def click_next_target(self):
        # 1. ordenar alvos por distância do centro
        # laço:
        # 2. passe o mouse sobre o alvo mais próximo
        # 3. confirme se é calcário por meio da dica de ferramenta
        # 4. se não estiver, verifique o próximo alvo
        #fim do loop
        # 5. se nenhum alvo foi encontrado, retorne falso
        # 6. clique no alvo encontrado e retorne verdadeiro
        targets = self.targets_ordered_by_distance(self.targets)

        target_i = 0
        found_limestone = False
        while not found_limestone and target_i < len(targets):
            # se paramos nosso script, saia deste loop
            if self.stopped:
                break

            # carrega o próximo alvo na lista e converte essas coordenadas
            # que são relativos à captura de tela do jogo para uma posição em nosso
            # tela
            target_pos = targets[target_i]
            screen_x, screen_y = self.get_screen_position(target_pos)
            print('Moving mouse to x:{} y:{}'.format(screen_x, screen_y))

            # move the mouse
            pyautogui.moveTo(x=screen_x, y=screen_y)
            # breve pausa para permitir que o movimento do mouse seja concluído 
            # e dar tempo para a dica de ferramenta aparecer
            sleep(1.25)
            # confirm limestone tooltip
            if self.confirm_tooltip(target_pos):
                print('Click on confirmed target at x:{} y:{}'.format(screen_x, screen_y))
                found_limestone = True
                pyautogui.click()
                # salve esta posição no histórico de cliques
                self.click_history.append(target_pos)
            #interação pra diversos alvos
            #target_i += 1

        return found_limestone    


    def click_next_target2(self):
        targets = self.targets_ordered_by_distance(self.targets)
        target_i = 0
        found_limestone = False
        while not found_limestone and target_i < len(targets):
            # se paramos nosso script, saia deste loop
            if self.stopped:
                break
            # carrega o próximo alvo na lista e converte essas coordenadas
            # que são relativos à captura de tela do jogo para uma posição em nosso
            # tela
            target_pos = targets[target_i]
            screen_x, screen_y = self.get_screen_position(target_pos)
            print('Moving mouse to x:{} y:{}'.format(screen_x, screen_y))
            pyautogui.moveTo(x=screen_x, y=screen_y)
            sleep(1.25)
            print('Click on confirmed target at x:{} y:{}'.format(screen_x, screen_y))
            #found_limestone = True
            pyautogui.click()
        return found_limestone    




    def have_stopped_moving(self):
        # se nao foi reservado um screenshot para comparar, faça isso primeiro
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screenshot.copy()
            return False

        # compara a amtiga screenshot com a atual 
        result = cv.matchTemplate(self.screenshot, self.movement_screenshot, cv.TM_CCOEFF_NORMED)
        # só nos importamos com o valor quando as duas capturas de tela estão perfeitamente 
        # posicionadas uma sobre a outra, então a posição da agulha é (0, 0). como ambas as 
        # imagens são do mesmo tamanho, este deve ser o único resultado que existe de qualquer maneira
        similarity = result[0][0]
        print('Movement detection similarity: {}'.format(similarity))

        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            # as fotos parecem semelhantes, então provavelmente paramos de nos mover
            print('Movement detected stop')
            return True

        # parece que ainda estamos em movimento.
        # use esta nova captura de tela para comparar com a próxima
        self.movement_screenshot = self.screenshot.copy()
        return False




    def targets_ordered_by_distance(self, targets):
        # nosso personagem está sempre no centro da tela
        my_pos = (self.window_w / 2, self.window_h / 2)
        # pesquisado "pontos de ordem python por distância do ponto" 
        # simplesmente usa o teorema de Pitágoras
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        # print(my_pos)
        # print(targets)
        # for t in targets:
        #    print(pythagorean_distance(t))

        # ignore os alvos que estão muito próximos do nosso personagem 
        # (dentro de 130 pixels) para evitar clicar novamente em um depósito que acabamos de extrair
        targets = [t for t in targets if pythagorean_distance(t) > self.IGNORE_RADIUS]

        return targets




    def confirm_tooltip(self, target_position):
        # verifique a captura de tela atual tem limestone tooltip, usando o modelo de correspondência
        result = cv.matchTemplate(self.screenshot, self.limestone_tooltip, cv.TM_CCOEFF_NORMED)
        # obtenha a melhor posição de partida
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # se pudermos fazer uma correspondência aproximada com a imagem da dica de ferramenta, considere o objeto encontrado
        if max_val >= self.TOOLTIP_MATCH_THRESHOLD:
            # print('Tooltip found in image at {}'.format(max_loc))
            # screen_loc = self.get_screen_position(max_loc)
            # print('Found on screen at {}'.format(screen_loc))
            # mouse_position = pyautogui.position()
            # print('Mouse on screen at {}'.format(mouse_position))
            # offset = (mouse_position[0] - screen_loc[0], mouse_position[1] - screen_loc[1])
            # print('Offset calculated as x: {} y: {}'.format(offset[0], offset[1]))
            # o deslocamento que sempre obtive foi o deslocamento calculado como x: -22 y: -29
            return True
        #print('Tooltip not found.')
        return False

    def click_backtrack(self):
        # retire o item superior da pilha de pontos clicados. 
        # este será o clique que nos trouxe à nossa localização atual.
        last_click = self.click_history.pop()
        # para desfazer esse clique, devemos espelhá-lo no ponto central.
        #  então se nosso personagem estiver no meio da tela no ex. (100, 100), 
        # e nosso último clique foi em (120, 120), então para desfazer isso devemos agora clicar em (80, 80).  
        # nosso personagem está sempre no centro da tela
        my_pos = (self.window_w / 2, self.window_h / 2)
        mirrored_click_x = my_pos[0] - (last_click[0] - my_pos[0])
        mirrored_click_y = my_pos[1] - (last_click[1] - my_pos[1])
        # convert this screenshot position to a screen position
        screen_x, screen_y = self.get_screen_position((mirrored_click_x, mirrored_click_y))
        print('Backtracking to x:{} y:{}'.format(screen_x, screen_y))
        pyautogui.moveTo(x=screen_x, y=screen_y)
        # short pause to let the mouse movement complete
        sleep(0.500)
        pyautogui.click()




    # traduz uma posição de pixel em uma imagem de captura de tela para uma posição de pixel na tela.
    # pos = (x, y)
    # AVISO: se você mover a janela que está sendo capturada após o início da execução,
    # isso retornará coordenadas incorretas, pois a posição da janela só é calculada no construtor WindowCapture __init__.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    # métodos de threading

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # CONTROLADOR LÓGICO PRINCIPAL
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # nao realize as ações do bot
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                # Começa a procurar 
                    self.lock.acquire()
                    self.state = BotState.SEARCHING                    
                    self.lock.release()

                elif self.state == BotState.SEARCHING:                    
                    # checka o click point dado, confirma que é o alvo e clicka nele
                    success = self.click_next_target()
                    # se for bem sucessido, muda o estado de movimentação
                    # se nao, volta pra tras na posição inicial
                    if not success:
                        success = self.click_next_target()
                    if success:
                        self.lock.acquire()
                        self.state = BotState.MOVING
                        self.lock.release()
                    #else:
                        # Fique no lugar e continue a procurar
                    #    pass

                elif self.start == BotState.MOVING:
                    #prepara o alimento
                    success = self.click_next_target2()
                    # se for bem sucessido, muda o estado de movimentação
                    # se nao, volta pra tras na posição inicial
                    if success:
                        self.lock.acquire()
                        self.state = BotState.MOVING
                        self.lock.release()
                    else:
                        # Fique no lugar e continue a procurar
                        pass






'''                elif self.start == BotState.MOVING:
                    #ve se foi parado o movimento comparando com a screenshot atual
                    if not self.have_stopped_moving():
                        #espera umk tempo até mudar de posição
                        sleep(0.500)
                    else:
                        #reseta timestep marker para o tempo atual. Troca o estado pra mining
                        self.lock.acquire()
                        self.timestamp = time()
                        self.state = BotState.MINING
                        self.lock.release()

                elif self.state == BotState.MINING:
                    if time() > self.timestamp + self.MINING_SECONDS:
                        # return to the searching state
                        self.lock.acquire()
                        self.state = BotState.SEARCHING
                        self.lock.release()'''

                    





