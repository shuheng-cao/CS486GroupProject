import os
import numpy as np
from tetris import Tetris
from keras.models import load_model

INPUT_SIZE = [20, 10, 1]
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
class DQNAgent:
    def __init__(self, path_to_model):
        self.model = load_model(path_to_model)

    def predict_value(self, state):
        '''Predicts the score for a certain state'''
        state = np.reshape(state, [1] + INPUT_SIZE)
        return self.model.predict(state)[0]

    def best_state(self, next_states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_action = None
        best_state = None


        for action,state in next_states.items():

            value = self.predict_value(state)
            if not max_value or value > max_value:
                max_value = value
                best_action = action
                best_state = state

        return best_action, best_state

if __name__ == "__main__":
    try:
        agent = DQNAgent(os.path.join(CUR_DIR,'models/dqn_agent.h5'))
        env = Tetris()
        env._init_game()
        done = False
        while not done:
            next_states = env.get_next_states(full_board=True)
            best_action, best_state = agent.best_state(next_states)
            _, done = env.play(best_action[0], best_action[1], render=True)
    except Exception as e:
        print(e)
