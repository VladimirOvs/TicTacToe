import pygame
import sys
import numpy as np
from typing import List, Tuple, Optional

pygame.init()

# Константы (все названия приведены к единому виду)
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 650
BOARD_SIZE = 5
WIN_LENGTH = 4
CELL_SIZE = 100
MARGIN = 50  
LINE_WIDTH = 4
X_COLOR = (255, 50, 50)
O_COLOR = (50, 50, 255)
BG_COLOR = (245, 245, 245)
LINE_COLOR = (70, 70, 70)
TEXT_COLOR = (40, 40, 40)
HIGHLIGHT_COLOR = (220, 255, 220)
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER_COLOR = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-нолики 5x5")

# Шрифты
try:
    font = pygame.font.Font(None, 36)
    status_font = pygame.font.Font(None, 32)
    button_font = pygame.font.Font(None, 30)
except:
    font = pygame.font.SysFont('Arial', 36)
    status_font = pygame.font.SysFont('Arial', 32)
    button_font = pygame.font.SysFont('Arial', 30)

class TicTacToe:
    def __init__(self):
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_cells = []
        self.last_move = None
        
    def reset(self):
        """Сброс игры в начальное состояние"""
        self.__init__() 
    
    def draw_board(self):
        """Отрисовка игрового поля и интерфейса"""
        screen.fill(BG_COLOR)
        self._draw_game_status()
        self._draw_grid()
        self._draw_symbols()
        self._draw_restart_button()
        self._highlight_last_move()
    
    def _draw_game_status(self):
        """Отрисовка статуса игры"""
        if self.game_over:
            status_text = f"Победил: {self.winner}!" if self.winner else "Ничья!"
            text_color = X_COLOR if self.winner == 'X' else O_COLOR if self.winner else TEXT_COLOR
        else:
            status_text = f"Ход: {self.current_player}"
            text_color = X_COLOR if self.current_player == 'X' else O_COLOR
            
        status_surface = status_font.render(status_text, True, text_color)
        text_rect = status_surface.get_rect(center=(SCREEN_WIDTH//2, 30))
        screen.blit(status_surface, text_rect)
    
    def _draw_grid(self):
        """Отрисовка игровой сетки"""
        for i in range(BOARD_SIZE + 1):
            # Горизонтальные линии
            pygame.draw.line(screen, LINE_COLOR, 
                          (MARGIN, MARGIN + i * CELL_SIZE), 
                          (SCREEN_WIDTH - MARGIN, MARGIN + i * CELL_SIZE), 
                          LINE_WIDTH)
            # Вертикальные линии
            pygame.draw.line(screen, LINE_COLOR, 
                          (MARGIN + i * CELL_SIZE, MARGIN), 
                          (MARGIN + i * CELL_SIZE, SCREEN_HEIGHT - MARGIN - 50), 
                          LINE_WIDTH)
    
    def _draw_symbols(self):
        """Отрисовка крестиков и ноликов"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
                
                if (row, col) in self.winning_cells:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, 
                                  (MARGIN + col * CELL_SIZE + 2, 
                                   MARGIN + row * CELL_SIZE + 2, 
                                   CELL_SIZE - 4, CELL_SIZE - 4), 
                                  border_radius=5)
                
                if self.board[row, col] == 'X':
                    self._draw_x(center_x, center_y)
                elif self.board[row, col] == 'O':
                    self._draw_o(center_x, center_y)
    
    def _draw_x(self, x, y):
        """крестик"""
        pygame.draw.line(screen, X_COLOR, (x-35, y-35), (x+35, y+35), 6)
        pygame.draw.line(screen, X_COLOR, (x+35, y-35), (x-35, y+35), 6)
    
    def _draw_o(self, x, y):
        """нолик"""
        pygame.draw.circle(screen, O_COLOR, (x, y), 35, 6)
    
    def _draw_restart_button(self):
        """кнопка рестарта"""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT-45, 200, 40)
        
        color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, button_rect, border_radius=5)
        pygame.draw.rect(screen, LINE_COLOR, button_rect, 2, border_radius=5)
        screen.blit(button_font.render("Новая игра", True, TEXT_COLOR), 
                  (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT-38))
    
    def _highlight_last_move(self):
        """подсветка последнего хода"""
        if self.last_move:
            row, col = self.last_move
            pygame.draw.rect(screen, (255, 255, 150), 
                           (MARGIN + col * CELL_SIZE + 5, 
                            MARGIN + row * CELL_SIZE + 5, 
                            CELL_SIZE - 10, CELL_SIZE - 10), 
                           border_radius=3)
    
    def make_move(self, row, col):
        """сам ход"""
        if (self.game_over or row < 0 or row >= BOARD_SIZE or 
            col < 0 or col >= BOARD_SIZE or self.board[row, col] != ' '):
            return False
            
        self.board[row, col] = self.current_player
        self.last_move = (row, col)
        
        if self._check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
            
        if np.all(self.board != ' '):
            self.game_over = True
            return True
            
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def _check_win(self, row, col):
        directions = [
            [(0,1), (0,-1)],  # горизонталь
            [(1,0), (-1,0)],   # вертикаль
            [(1,1), (-1,-1)],  # главная диагональ
            [(1,-1), (-1,1)]   # побочная диагональ
        ]
        
        for direction_pair in directions:
            count = 1
            self.winning_cells = [(row, col)]
            
            for dx, dy in direction_pair:
                x, y = row + dx, col + dy
                while (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 
                       self.board[x, y] == self.current_player):
                    count += 1
                    self.winning_cells.append((x, y))
                    x += dx
                    y += dy
                    if count == WIN_LENGTH:
                        return True
        
        self.winning_cells = []
        return False

def main():
    game = TicTacToe()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Проверка клика на кнопку
                if (SCREEN_WIDTH//2 - 100 <= x <= SCREEN_WIDTH//2 + 100 and 
                    SCREEN_HEIGHT-45 <= y <= SCREEN_HEIGHT-5):
                    game.reset()
                    continue
                
                # Проверка клика на поле
                if (MARGIN <= x <= SCREEN_WIDTH - MARGIN and 
                    MARGIN <= y <= SCREEN_HEIGHT - MARGIN - 50):
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN) // CELL_SIZE
                    game.make_move(row, col)
        
        game.draw_board()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
