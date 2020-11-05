from keras.models import Sequential, save_model, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from collections import deque
import numpy as np
import random

INPUT_SIZE = [20, 10, 3]
MEM_SIZE = 10000
DISCOUNT = 0.95
EPSILON = 1
EPSILON_MIN = 0
EPSILON_STOP_EPISODE = 500
EPSILON_DECAY = (EPSILON - EPSILON_MIN) / EPSILON_STOP_EPISODE


class DQNAgent:
    def __init__(self):
        self.memory = deque(maxlen=MEM_SIZE)
        self.model = self._build_model()
        self.epsilon = EPSILON


    def _build_model(self):
        '''Builds a Keras deep neural network model'''
        model = Sequential()

        model.add(Conv2D(256, (3, 3), input_shape=INPUT_SIZE))  # OBSERVATION_SPACE_VALUES = (10, 10, 3) a 10x10 RGB image.
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Conv2D(256, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(64))

        model.add(Dense(1, activation='linear'))
        model.compile(loss="mse", optimizer="adam", metrics=['accuracy'])
        return model


    def add_to_memory(self, current_state, next_state, reward, done):
        '''Adds a play to the replay memory buffer'''
        self.memory.append((current_state, next_state, reward, done))


    def random_value(self):
        '''Random score for a certain action'''
        return random.random()


    def predict_value(self, state):
        '''Predicts the score for a certain state'''
        return self.model.predict(state)[0]


    def act(self, state):
        '''Returns the expected score of a certain state'''
        state = np.reshape(state, [1] + INPUT_SIZE)
        if random.random() <= self.epsilon:
            return self.random_value()
        else:
            return self.predict_value(state)


    def best_state(self, states):
        '''Returns the best state for a given collection of states'''
        max_value = None
        best_state = None

        if random.random() <= self.epsilon:
            return random.choice(list(states))

        else:
            for state in states:
                value = self.predict_value(np.reshape(state, [1] + INPUT_SIZE))
                if not max_value or value > max_value:
                    max_value = value
                    best_state = state

        return best_state


    def train(self, batch_size=32, epochs=3):
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
