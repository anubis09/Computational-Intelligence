# LAB10

The following solution was developed together with [Lorenzo Tozzi](https://github.com/anubis09/Computational-Intelligence).

Two main classes are implemented:
- `Player`: this class serves as an abstract foundation from which various player types can be built. We implemented three kind of plyers from it:
  - ```RandomPlayer```: a player that makes random moves among the possible ones, given a board configuaration.
  - ```RLayer```: this player uses reinforcement learning strategies to learn a policy during training phase. It makes moves following the learnt policy when a game takes place against an other player.
  - ```HumanPlayer```: this class enable users to play a real game against our RLayers plyers.

- ```TicTacToe```: it implements main functionalities of the game and the possibility to play matches in training mode, setting ```TicTacToe.train_mode=True```. This allows the player to learn a policy and save it in a file when training ends.

*TODO: explain some other important stuff of the game and presents results with some comments SIUUUUUUM*

The ```RLayer``` has an internal dictionary called policy, where each state of the game (discovered by the agent) is associated with a value. 
When the agent is in train mode, it has a 0.3 probability to make a random move (this allows exploration), otherwise it takes the best possible move that can be done, based on the values in the policy and returns it. 
All the used moves in a training game are stored in a list.
When a training game is over, we have a backpropagation step where the values associated with the used moves (policy states) are updated based on the outcome of the game.

## Train

We decided to train our agent against three different type of players:
- 
