from keras.models import Sequential, save_model, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from statistics import mean, median
from collections import deque
from tqdm import tqdm
import numpy as np
import random

INPUT_SIZE = [20, 10, 1]
MEM_SIZE = 20000
DISCOUNT = 0.95
EPSILON = 1
EPSILON_MIN = 0
EPSILON_STOP_EPISODE = 1800
EPSILON_DECAY = (EPSILON - EPSILON_MIN) / EPSILON_STOP_EPISODE
env = Tetris()
episodes = 2000
max_steps = 2000
batch_size = 512
epochs = 2
log_every = 50
train_every = 1

class DQNAgent:
    def __init__(self):
        self.memory = deque(maxlen=MEM_SIZE)
        self.model = self._build_model()
        self.epsilon = EPSILON

    def _build_model(self):
        '''Builds a Keras deep neural network model'''
        model = Sequential()

        model.add(Conv2D(64, (3, 3), input_shape=INPUT_SIZE))  # OBSERVATION_SPACE_VALUES = (10, 10, 3) a 10x10 RGB image.
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(128, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(64, activation='relu'))

        model.add(Dense(1, activation='linear'))
        model.compile(loss="mse", optimizer="adam", metrics=['accuracy'])
        print(model.summary())
        return model


    def add_to_memory(self, current_state, next_state, reward, done):
        '''Adds a play to the replay memory buffer'''
        self.memory.append((current_state, next_state, reward, done))


    def random_value(self):
        '''Random score for a certain action'''
        return random.random()


    def predict_value(self, state):
        '''Predicts the score for a certain state'''
        state = np.reshape(state, [1] + INPUT_SIZE)
        return self.model.predict(state)[0]


    def best_state(self, next_states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_action = None
        best_state = None

        if random.random() <= self.epsilon:
            return random.choice(list(next_states.items()))

        else:
            for action,state in next_states.items():

                value = self.predict_value(state)
                if not max_value or value > max_value:
                    max_value = value
                    best_action = action
                    best_state = state

        return best_action, best_state


    def train(self, batch_size=32, epochs=1):
        '''Trains the agent'''
        n = len(self.memory)
    
        if n >= batch_size:

            batch = random.sample(self.memory, batch_size)

            # Get the expected score for the next states, in batch (better performance)
            next_states = np.array([x[1] for x in batch])
            next_qs = [x[0] for x in self.model.predict(next_states)]

            x = []
            y = []

            # Build xy structure to fit the model in batch (better performance)
            for i, (state, _, reward, done) in enumerate(batch):
                if not done:
                    # Partial Q formula
                    new_q = reward + DISCOUNT * next_qs[i]
                else:
                    new_q = reward

                x.append(state)
                y.append(new_q)

            # Fit the model to the given values
            self.model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs, verbose=0)

            # Update the exploration variable
            if self.epsilon > EPSILON_MIN:
                self.epsilon -= EPSILON_DECAY

def train_agent():
    agent = DQNAgent()
    scores = []
    for episode in tqdm(range(episodes//log_every)):
        progress = tqdm(range(log_every), desc="current score = ")
        for i in progress:
            current_state = env.reset()
            done = False
            steps = 0

            # Game
            while not done and (not max_steps or steps < max_steps):
                next_states = env.get_next_states()
                best_action, best_state = agent.best_state(next_states)
                reward, done = env.play(best_action[0], best_action[1])
                
                agent.add_to_memory(current_state, next_states[best_action], reward, done)
                current_state = next_states[best_action]
                steps += 1

            scores.append(env.get_game_score())
            progress.set_description(f"current score = {scores[-1]}")

            # Train
            if episode % train_every == 0:
                agent.train(batch_size=batch_size, epochs=epochs)

            # Logs
            if i==log_every-1:
                avg_score = mean(scores[-log_every:])
                min_score = min(scores[-log_every:])
                max_score = max(scores[-log_every:])
                print(avg_score, min_score, max_score)

if __name__ == '__main__':
    train_agent()