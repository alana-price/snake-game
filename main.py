import random
import pygame
import sys


def main():
    pygame.init()

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    pink = (255, 192, 203)

    # Set the width and height of the game window
    width, height = 800, 600
    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Define the size of the snake and the radius of the food in pixels
    snake_size = 20
    food_radius = 10

    # Create fonts for displaying messages and the score
    message_font = pygame.font.Font(None, 30)
    score_font = pygame.font.Font(None, 30)

    # Function to print the player's score on the screen
    def print_score(score):
        # Render the score as pink text
        text = score_font.render("Score: " + str(score), True, pink)
        # Display the score
        game_display.blit(text, [20, 20])

    # Function to draw the snake on the game window
    def draw_snake(snake_size, snake_pixels):
        for pixel in snake_pixels:
            # Draw rectangle at the (x, y) coordinate of a given pixel
            pygame.draw.rect(game_display, black, [pixel[0], pixel[1], snake_size, snake_size])

    # The main game loop
    def run_game():
        game_over = False
        game_close = False

        x = width / 2
        y = height / 2

        x_speed = 0
        y_speed = 0

        snake_pixels = []
        snake_length = 1
        snake_speed = 15

        # Initialize the position of the target food
        food_x = round(random.randrange(0, width - food_radius * 2) / 20.0) * 20.0
        food_y = round(random.randrange(0, height - food_radius * 2) / 20.0) * 20.0

        while not game_over:

            while game_close:
                game_display.fill(white)
                game_over_message = message_font.render("GAME OVER", True, red)
                game_display.blit(game_over_message, [width / 3, height / 3])

                score_message = message_font.render("Score: " + str(snake_length -1), True, black)
                game_display.blit(score_message, [width / 3, 50 + height / 3])

                quit_message = message_font.render("Press \'Q\' to Quit", True, black)
                game_display.blit(quit_message, [width / 3, 100 + height / 3])

                restart_message = message_font.render("Press \'R\' to Restart", True, black)
                game_display.blit(restart_message, [width / 3, 150 + height / 3])

                print_score(snake_length - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_r:
                            run_game()
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False

            # Create a flag control whether a key press has processed in the current loop iteration
            key_processed = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Do not allow the user to go the opposite way they're headed
                if event.type == pygame.KEYDOWN:
                    if not key_processed:
                        if event.key == pygame.K_LEFT and x_speed <= 0:
                            x_speed = -snake_size
                            y_speed = 0
                            key_processed = True
                        if event.key == pygame.K_RIGHT and x_speed >= 0:
                            x_speed = snake_size
                            y_speed = 0
                            key_processed = True
                        if event.key == pygame.K_UP and y_speed <= 0:
                            x_speed = 0
                            y_speed = -snake_size
                            key_processed = True
                        if event.key == pygame.K_DOWN and y_speed >= 0:
                            x_speed = 0
                            y_speed = snake_size
                            key_processed = True

            # Reset the flag at the start of each game loop iteration
            key_processed = False

            if x >= width or x < 0 or y >= height or y < 0:
                game_close = True

            x += x_speed
            y += y_speed

            # Draw the white arena background
            game_display.fill(white)

            # Draw the target food
            pygame.draw.circle(game_display, red, (int(food_x + food_radius), int(food_y + food_radius)), food_radius)

            snake_pixels.append([x, y])

            if len(snake_pixels) > snake_length:
                del snake_pixels[0]

            for pixel in snake_pixels[:-1]:
                if pixel == [x, y]:
                    game_close = True

            # Draw the snake
            draw_snake(snake_size, snake_pixels)

            # Print the player's score
            print_score(snake_length - 1)
            pygame.display.update()

            if x == food_x and y == food_y:

                # Randomly reposition the target food and increase the snake's length
                food_x = round(random.randrange(0, width - food_radius * 2) / 20.0) * 20.0
                food_y = round(random.randrange(0, height - food_radius * 2) / 20.0) * 20.0
                snake_length += 1

                # Increase the speed by 5 pixels per frame after every 10 points
                if (snake_length - 1 ) % 10 == 0:
                    snake_speed += 5

            clock.tick(snake_speed)

        pygame.quit()
        sys.exit()

    run_game()


if __name__ == "__main__":
    main()
