from tetris import Tetris

class Handcrafted_agent:
    def __init__(self, state_size):
        self.state_size = state_size
    
    def best_state(self, states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_state = None

        for state in states:
            value = self.predict_value(state)
            if not max_value or value > max_value:
                max_value = value
                best_state = state

        return best_state

    def predict_value(self, state):
        weights = [-4.500158825082766, 3.4181268101392694, -3.2178882868487753, -9.348695305445199, -7.899265427351652, -3.3855972247263626]
        value = 0
        for i in range(len(state)):
            value += weights[i] * state[i]
        return value

def hand_crafted():
    env = Tetris()
    current_state = env.reset()
    done = False
    steps = 0

    agent = Handcrafted_agent(env.get_state_size())

    # Game
    while not done:
        next_states = env.get_next_states_handcrafted()
        best_state = agent.best_state(next_states.values())
        
        best_action = None
        for action, state in next_states.items():
            if state == best_state:
                best_action = action
                break

        reward, done = env.play(best_action[0], best_action[1], render=True,
                                render_delay=None)
        
        current_state = next_states[best_action]
        steps += 1
    
    return env.get_game_score()

if __name__ == "__main__":
    scores = []
    for i in range(1):
        score = hand_crafted()
        scores.append(score)
    avg = sum(scores) / float(len(scores))
    print("Average score: "+ str(avg))
    print("Min score: " + str(min(scores)))
    print("Max score: " + str(max(scores)))