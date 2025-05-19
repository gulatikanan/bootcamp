from game import Game

# Create an empty game object
game = Game()

# Load state from file
game.load("game_state.json")

print("✅ Game state loaded:")
print(f"Level: {game.level}")
print(f"Score: {game.score}")
