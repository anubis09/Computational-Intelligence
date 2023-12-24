# LAB10

The following solution was developed together with [Lorenzo Tozzi](https://github.com/anubis09/Computational-Intelligence).

Two main classes are implemented:
- `Player`: this class serves as an abstract foundation from which various player types can be built. We implemented three kind of plyers from it:
  - ```RandomPlayer```: a player that makes random moves among the possible ones, given a board configuaration.
  - ```RLayer```: this player uses reinforcement learning strategies to learn a policy during training phase. It makes moves following the learnt policy when a game takes place against an other player.
  - ```HumanPlayer```: this class enable users to play a real game against our RLayers plyers.

- ```TicTacToe```: it implements main functionalities of the game and the possibility to play matches in training mode, setting ```TicTacToe.train_mode=True```. This allows the player to learn a policy and save it in a file when training ends.

## RLayer

The ```RLayer``` has an internal dictionary called policy, where each discovered state of the game is associated with a value. 
When the agent is in train mode, it has a 0.3 probability to make a random move (this allows exploration), otherwise it takes the best possible move that can be done, based on the values in the policy and returns it. 
All the chosen moves in a training game are stored in a list.

When a training game is over, we have a backpropagation step where the values associated with the moves used in that same game (policy states) are updated based on the outcome of the game. If it's a win, the reward is 1, if it's a loss, the reward is -1, and it's a tie the reward is 0.5.

The policy values are updated following a value iteration strategy:
- V(S) = V(S) + alpha * (gamma_decay*reward - V(S))

Where alpha is the learning rate, set to 0.2 and the gamma_decay is set to 0.9.
## Train
The training steps consists in a 400_000 games against another oppononent.
We decided to train three different reinforcement learning agents:
- ```rl_base```: This agent has been trained against a random player.
- ```rl_RL_trained```: This agent has been trained against another reinforcement learning player.
- ```the_ROCK```: This agent has been trained against both a random player and the "rl_RL_trained".

## Evaluation
All this three agent have been evaluated after 2000 games against a random player.
The results are:
1) The best performing one is ```the_ROCK```, showing a 93% of wins, 6.5% of ties and just 0.5% of losses.
2) The second best performing is ```rl_base```, with 92.9% of victories, 5.7% of ties and 1.4% of losses.
3) Lastly we have ```rl_RL_trained``` with 89.4% of wins, 9.45% of ties and 1.15% of losses.

Notice that with more epochs of training (around 500_000 in total), the ```rl_RL_trained``` agent can reach the performances of the other agents.

