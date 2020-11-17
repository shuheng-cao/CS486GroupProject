# CS486GroupProject

## Description:
This project is about the game Tetris, which involves three agents. Handcrafted Agent, Generic Algorithm Agent and Reinforcement Learning Agent. The purpose of this project is to learn about the theory of Generic Algorithm and Reinforcement Learning, and also compare the performances among these three models.

## Features:
The implementation contains the following features:
- number of cleaned rows
- number of holes
- height of the heightest hole
- number of rows with holes
- number of wells (A well is a succession of empty cells such that their left cells and right cells are both filled.)
- row transitions (The total number of row transitions. A row transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.)
- column transitions (The total number of column transitions. A column transition occurs when an empty cell is adjacent to a filled cell on the same column and vice versa.)
- total bumpiness
- maximum bumpines
- sum of height of each column
- maximum row height
- minimum row height
- height of each row

## Required Libarary:
- Tensorflow (`tensorflow-gpu==1.14.0`)
- Keras (`Keras==2.2.4`)
- Opencv-python (`opencv-python==4.1.0.25`)
- Numpy (`numpy==1.16.4`)
- Pillow (`Pillow==5.4.1`)
- Tqdm (`tqdm==4.31.1`)
- cv2 (`opencv-python==4.4.0.44`)

## Commands to run:
### Tetris Interface:
Simply execute [run.py](https://github.com/shuheng-cao/CS486GroupProject/blob/master/src/run.py), the game will start.
Use (W), A, S, D to control the Tetromino, (up), left, down, right respectively.
Use Q to rotate the Tetromino 90 degrees to the left, and use E to rotate the Tetromino 90 degrees to the right.
### Handcrafted Agent:
Execute [handcrafted_agent.py](https://github.com/shuheng-cao/CS486GroupProject/blob/master/src/handcrafted_agent.py) and the game will automatically played. Set render = true if you want to visualize the game.
### Local Search Agent:

#### Training
There are two ways to train the Generic Algorithm Agent.
- __(Recommended)__ train the model in the Colab environment [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1A-agtk1B0af63LAAELrrnmh-6ZzFJFrE?usp=sharing)
- We could also train the model by running the python script [GeneticAgent.py](https://github.com/shuheng-cao/CS486GroupProject/blob/master/src/GeneticAgent.py). However, this may not be the most updated version and the results may not as expected.

#### Executing

*TODO: integrate the model into the environment*

### Reinforcement Learning Agent:
#### Training
There are also two ways to train the Generic Algorithm Agent.
- __(Recommended)__ train the model in the Colab environment [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1EZfONSDWkliLaNQqu9Ew3KlUkLvRhAxX?usp=sharing)
- We could also train the model by running the python script [DQNAgent.py](https://github.com/shuheng-cao/CS486GroupProject/blob/master/src/DQNAgent.py). However, this may not be the most updated version and the results may not as expected.

#### Executing

*TODO: integrate the model into the environment*


## Sample:
<img src="https://github.com/shuheng-cao/CS486GroupProject/raw/master/demo.gif" width="254" height="530" />
