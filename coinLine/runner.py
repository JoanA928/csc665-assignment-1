# runner.py

import pygame
import sys
import random
import time
import coinline as cl

# Pygame Setup  ----------------
pygame.init()
WIDTH, HEIGHT = 1000, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Line Game")
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 40)
CLOCK = pygame.time.Clock()

# Coin Details ----------------
NUM_COINS = 40
GAP = 20
COIN_RADIUS = (WIDTH - GAP*(NUM_COINS+2))//(NUM_COINS*2)
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - 20
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Buttons
buttons = {
    "L1": pygame.Rect(100, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT),
    "L2": pygame.Rect(275, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT),
    "R1": pygame.Rect(550, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT),
    "R2": pygame.Rect(725, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT),
}

def draw_game(state, message=""):
    SCREEN.fill((30, 30, 30))
    coins = state.coins

    # Draw coins
    x = (WIDTH - ((COIN_RADIUS * 2 + GAP) * NUM_COINS - GAP)) // 2
    y = HEIGHT // 2 - 50
    for value in coins:
        pygame.draw.circle(SCREEN, (200, 200, 0), (x + COIN_RADIUS, y), COIN_RADIUS)
        text = FONT.render(str(value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + COIN_RADIUS, y))
        SCREEN.blit(text, text_rect)
        x += COIN_RADIUS * 2 + GAP

    # Scores
    p_text = FONT.render(f"You: {state.pScore}", True, (255, 255, 255))
    a_text = FONT.render(f"AI: {state.aiScore}", True, (255, 255, 255))
    t_text = FONT.render(f"Turn: {state.turn.upper()}", True, (200, 200, 255))
    SCREEN.blit(p_text, (20, 20))
    SCREEN.blit(a_text, (20, 50))
    SCREEN.blit(t_text, (20, 80))

    # Buttons
    for label, rect in buttons.items():
        is_hovered = rect.collidepoint(pygame.mouse.get_pos())
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(SCREEN, color, rect)
        pygame.draw.rect(SCREEN, (255, 255, 255), rect, 2)
        btn_text = FONT.render(label, True, BUTTON_TEXT_COLOR)
        SCREEN.blit(btn_text, btn_text.get_rect(center=rect.center))

    if message:
        msg_text = BIG_FONT.render(message, True, (255, 100, 100))
        SCREEN.blit(msg_text, msg_text.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

    pygame.display.flip()

def handle_player_action(state, label):
    label = label.upper()
    if label == "L1":
        action = ('L', 1)
    elif label == "L2":
        action = ('L', 2)
    elif label == "R1":
        action = ('R', 1)
    elif label == "R2":
        action = ('R', 2)
    else:
        return state

    if action in cl.actions(state):
        return cl.succ(state, action)
    return state

# --- Main Game Loop ---
def main():
    initial_coins = [random.randint(1, 15) for _ in range(NUM_COINS)]
    state = cl.State(initial_coins)

    game_over = False
    result_message = ""

    while True:
        CLOCK.tick(30)
        
        if cl.terminal(state) and not game_over:
            win = cl.winner(state)
            game_over = True
            if win.lower() == "player":
                result_message = "You Win!"
            elif win.lower() == "ai":
                result_message = "AI Wins!"
            else:
                result_message = "It's a Tie!"

        draw_game(state, result_message)

        

        # click, _, _ = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and not game_over and cl.player(state) == 'player':# and event.type == pygame.MOUSEBUTTONDOWN:
                print("Player turn")
                for label, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        print("action turn: ", label)
                        state = handle_player_action(state, label)

            # Start new game if game is over and SPACE is pressed
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initial_coins = [random.randint(1, 15) for _ in range(NUM_COINS)]
                state = cl.State(initial_coins)
                game_over = False
                result_message = ""

        # AI Move
        if not game_over and cl.player(state) == 'ai':
            print("AI turn")
            pygame.time.delay(500)
            time.sleep(0.5)
            _, action = cl.minimax(state, is_maximizing=True)
            if action:
                state = cl.succ(state, action)



if __name__ == "__main__":
    main()
