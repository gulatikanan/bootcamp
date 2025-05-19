from game import Game

game = Game(level=3, score=450)
game.save("game_state.json")

print("✅ Game state saved!")
