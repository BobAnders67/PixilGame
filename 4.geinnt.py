import arcade
import random
import math

class TTT(arcade.Window):
    def __init__(self):
        super().__init__(700, 600, "4 Gewinnt")
        self.spielfeld = {(x, y): "" for x in range(7) for y in range(6)}
        self.gewinner = ""
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_line(200, 0, 200, 600, arcade.color.WHITE, 6)
        arcade.draw_line(400, 0, 400, 600, arcade.color.WHITE, 6)
        arcade.draw_line(100, 0, 100, 600, arcade.color.WHITE, 6)
        arcade.draw_line(300, 0, 300, 600, arcade.color.WHITE, 6)
        arcade.draw_line(500, 0, 500, 600, arcade.color.WHITE, 6)
        arcade.draw_line(600, 0, 600, 600, arcade.color.WHITE, 6)
        for koordinaten in self.spielfeld:
            symbol = self.spielfeld[koordinaten]
            pos_x = (koordinaten[0] * 100 + 50)
            pos_y = (koordinaten[1] * 100 + 50)
            if symbol == 1:
                arcade.draw_circle_filled(pos_x, pos_y, 35, arcade.color.RED)
            elif symbol == 2:
                arcade.draw_circle_filled(pos_x, pos_y, 35, arcade.color.BLUE)
        if self.gewinner == 1:
            arcade.draw_line(0, 300, 700, 300, arcade.color.WHITE, 100)
            arcade.draw_text("Rot hat gewonnen!", 350, 300, arcade.color.RED, 50, anchor_x="center", anchor_y="center")
        elif self.gewinner == 2:
            arcade.draw_line(0, 300, 700, 300, arcade.color.WHITE, 100)
            arcade.draw_text("Blau hat gewonnen!", 350, 300, arcade.color.BLUE, 50, anchor_x="center", anchor_y="center")

    def computerzug(self):
        def set_move(x, y, player):
            self.spielfeld[(x, y)] = player

        def is_valid_move(x, y):
            return self.spielfeld[(x, y)] == "" and (y == 0 or self.spielfeld[(x, y-1)] != "")

        def get_valid_moves():
            return [(x, y) for x in range(7) for y in range(6) if is_valid_move(x, y)]

        def check_winner(player):
            # Horizontale Gewinnkombinationen
            for y in range(6):
                for x in range(4):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y)] == self.spielfeld[(x+2, y)] == self.spielfeld[(x+3, y)] == player:
                        return True

            # Vertikale Gewinnkombinationen
            for x in range(7):
                for y in range(3):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x, y+1)] == self.spielfeld[(x, y+2)] == self.spielfeld[(x, y+3)] == player:
                        return True

            # Diagonale Gewinnkombinationen (von unten links nach oben rechts)
            for x in range(4):
                for y in range(3):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y+1)] == self.spielfeld[(x+2, y+2)] == self.spielfeld[(x+3, y+3)] == player:
                        return True

            # Diagonale Gewinnkombinationen (von oben links nach unten rechts)
            for x in range(4):
                for y in range(3, 6):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y-1)] == self.spielfeld[(x+2, y-2)] == self.spielfeld[(x+3, y-3)] == player:
                        return True

            return False

        def evaluate_board():
            score = 0

            def count_patterns(player):
                patterns = 0
                # Horizontale Muster
                for y in range(6):
                    for x in range(4):
                        if all(self.spielfeld[(x + i, y)] in [player, ""] for i in range(4)):
                            patterns += 1

                # Vertikale Muster
                for x in range(7):
                    for y in range(3):
                        if all(self.spielfeld[(x, y + i)] in [player, ""] for i in range(4)):
                            patterns += 1

                # Diagonale Muster (von unten links nach oben rechts)
                for x in range(4):
                    for y in range(3):
                        if all(self.spielfeld[(x + i, y + i)] in [player, ""] for i in range(4)):
                            patterns += 1

                # Diagonale Muster (von oben links nach unten rechts)
                for x in range(4):
                    for y in range(3, 6):
                        if all(self.spielfeld[(x + i, y - i)] in [player, ""] for i in range(4)):
                            patterns += 1

                return patterns

            if check_winner(2):
                score += 1000
            elif check_winner(1):
                score -= 1000
            else:
                score += count_patterns(2) * 10
                score -= count_patterns(1) * 10

            return score

        def minimax(depth, alpha, beta, maximizingPlayer):
            valid_moves = get_valid_moves()
            is_terminal = check_winner(1) or check_winner(2) or not valid_moves
            if depth == 0 or is_terminal:
                return evaluate_board()

            if maximizingPlayer:
                value = -math.inf
                for (x, y) in valid_moves:
                    set_move(x, y, 2)
                    value = max(value, minimax(depth-1, alpha, beta, False))
                    self.spielfeld[(x, y)] = ""
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value
            else:
                value = math.inf
                for (x, y) in valid_moves:
                    set_move(x, y, 1)
                    value = min(value, minimax(depth-1, alpha, beta, True))
                    self.spielfeld[(x, y)] = ""
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return value

        def best_move():
            valid_moves = get_valid_moves()
            best_value = -math.inf
            best_move = None
            for (x, y) in valid_moves:
                set_move(x, y, 2)
                move_value = minimax(3, -math.inf, math.inf, False)  # Reduzierte Tiefe
                self.spielfeld[(x, y)] = ""
                if move_value > best_value:
                    best_value = move_value
                    best_move = (x, y)
            print(best_value)
            return best_move

        move = best_move()
        if move:
            set_move(move[0], move[1], 2)

    def gewinnprüfen(self):
        def check_winner(player):
            # Horizontale Gewinnkombinationen
            for y in range(6):
                for x in range(4):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y)] == self.spielfeld[(x+2, y)] == self.spielfeld[(x+3, y)] == player:
                        return True

            # Vertikale Gewinnkombinationen
            for x in range(7):
                for y in range(3):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x, y+1)] == self.spielfeld[(x, y+2)] == self.spielfeld[(x, y+3)] == player:
                        return True

            # Diagonale Gewinnkombinationen (von unten links nach oben rechts)
            for x in range(4):
                for y in range(3):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y+1)] == self.spielfeld[(x+2, y+2)] == self.spielfeld[(x+3, y+3)] == player:
                        return True

            # Diagonale Gewinnkombinationen (von oben links nach unten rechts)
            for x in range(4):
                for y in range(3, 6):
                    if self.spielfeld[(x, y)] == self.spielfeld[(x+1, y-1)] == self.spielfeld[(x+2, y-2)] == self.spielfeld[(x+3, y-3)] == player:
                        return True

            return False

        if check_winner(1):
            self.gewinner = 1
        elif check_winner(2):
            self.gewinner = 2

    def on_mouse_press(self, x, y, button, modifiers):
        self.gewinnprüfen()
        if self.gewinner:
            return

        column = x // 100
        for y in range(6):
            if self.spielfeld[(column, y)] == "":
                self.spielfeld[(column, y)] = 1
                break

        self.gewinnprüfen()
        if not self.gewinner:
            self.computerzug()
            self.gewinnprüfen()

if __name__ == "__main__":
    window = TTT()
    arcade.run()
