from tetris import Tetris
import keyboard
import time

if __name__ == "__main__":
    env = Tetris()
    env._init_game()
    while True:
        try:
            if keyboard.is_pressed('w'):
                env.play(-2, 0, render=True, player_mode=True)
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('a'):
                env.play(-1, 0, render=True, player_mode=True)
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('s'):
                env.play(0, 0, render=True, player_mode=True)
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('d'):
                env.play(1, 0, render=True, player_mode=True)
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('q'):
                env.play(0, -1, render=True, player_mode=True)
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('e'):
                env.play(0, 1, render=True, player_mode=True)
                time.sleep(0.1)
                continue
        except Exception as e:
            print(f"finding exception {e}")
            break
