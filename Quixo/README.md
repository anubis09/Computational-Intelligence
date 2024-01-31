# Quixo

The following solution was developed together with [Andrea Pellegrino](https://github.com/andry2327/Computational-Intelligence).

Our code refers to the following commit: 36854293decbb4496061a2295f2d2fcd0c61d4d0.

## Overview
In this final Lab we had to develop an agent able to play the Quixo game (you can find a description in ```Quixo.pdf```) and aim to achieve good results against a random player. 
We created an agent based on Reinforcement Learning teqniques, which is able to play through a policy learned with Value Iteration.

## Files description

- ```main.ipynb```: Here are present key functionalities, running games against a random opponent and the option to play against our player.
- ```game.py``` : This is the file presenting the implementation of the Quixo ```Game``` class, the ```Player``` class and the ```Move``` class. We took this file from the commit and we modified the print function, in order to print a prettier board. We also enabled the ```play``` method to print the board after every move.
- ```players.py```: This file contains implementations of players employing various strategies, ```RandomPlayer```, ```HumanPlayer```,  ```RLayer``` (our player trained using reinforcemnt learning techniques).
- ```train.py```: In this file we implemented the methods that allowed us to train our player. We had to subclass the ```game``` class in order to facilitate our training. 
- ```DeepQ.ipynb```: In this notebook we tried to implement a DeepQ-learning approach (following this [guide](https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a)). The net was higly unstable and very slow, so we couldn't optimize it properly. In the future we would like to focus on this approach because we believe it can deliver high performance with fewer computational power when compared to simple Q-learning.
- Policy used by our player can be found in ```Quixo/Policies```. 

## Policy
The policy is a dictionary that, after training, is turned into a JSON file. We structred the policy dictionary in the following format:
```python
{
    Key: str(board) + str(player_id)
    Value: dict{
                Key: str(from_pos) + ";" + str(Move)
                Value: float(value)
                }
}
```
Our policy is a dictionary of dictionaries.
Where the keys of the outer dictionary are a string representing the board state, with also attached the player id. We add the player id because the agent can end up in the same state both if starting as first or as second. So in order to distinguish which moves are the best, we also encode the player id.

The value is another dictionary where the keys are the strings representing the position of the cube to take, plus the slide move to apply. The value is the value representing the goodness of the move.

The policy values are updated following a Q-Learning strategy:
- $V(S) = V(S) + lr * (\text{gamma-decay}*\text{reward} - V(S))$

Where the reward becomes the $V(S)$ at each iteration. When assigning rewards, we start from the last visited state and we end with the first one.

In the following section we will describe how we trained our agent, and how we optimized the size of the policy.

## Training

We decided to initially train our player against others RLayer, in order to not build a sub-optimal policy. We observed that initiating training against a random player resulted in consistently adopting a specific move within the same row or column. While this proved to be a winning strategy against a random player, it could be easily countered by a more intelligent opponent.

### Training strategy

1. Our agent(no policy) vs RLayer2(no policy), for 2 milions games: Here our RLayer will start building its policy starting in full exploration (```epsilon``` = 1), and ending up with a value of 0.3 exploration at the end of this training.
2. Our agent(policy learnt in step 1) vs random player, for 4 milions games.
3. Our agent(policy learnt in step 2) vs RLayer2(policy learnt by our agent in step 2), for 2 milions games: This allows our player to enhance its policy by playing against its own learned strategy.
4. Our agent(policy learnt in step 3) vs random player, 12 milions games: This final step is designed to construct the ultimate optimal policy tailored to the player against which it will be evaluated.

### Training Parameters
- ```epsilon``` = 0.3 (it determines the probaility of making a random move)
- ```lr``` = 0.2
- ```gamma_decay``` = 0.9

Reward values: 
- Win = +1
- Lose = -3
- Draw as starting player = 0.1
- Draw as second player = 0.5

In the training phase, if a game extends beyond 150 moves, we categorize it as a draw.

## Policy pruning
We built a function ```save_space``` in order to reduce dimensions of the final policy:
- It removes all the entries (board states) where the number of discovered moves is lower than the specified threshold, `MIN_MOVES`: having a low number of moves associated with a particular board state indicates that these states have been rarely encountered. Therefore, opting for a learned move instead of a random move in such instances doesn't confer significant advantages, and so they can be removed. We have set ```MIN_MOVES``` = 4.
- It only retains the top-k moves for each key: during inference, our player will make the move with the highest associated value. Thus, there is no need to store all other possible moves different from the best learned one after training. We have set `top_k` = 1.
- It rounds the value associated with each key to `N_DECIMAL` decimal digits. We have set `N_DECIMAL` = 2.

After all this steps our policy weighted around 155 MB.
We decided to investigate the values stored in our policy, using the ```policy_stat``` method of our RL layer. 
It showed us that the policy contained around 2.2 million entries and that the 50th percentile was 0. So more than half values stored were $\le 0$.
We decided to remove all the values below 0.01, since the move discovered was actually not taking any significant reward, so we could afford to play randomly in that case. 

In the end our policy contains around 690k entries and it weights 51.9MB.

Further pruning of the policy reduces the performances of our agents.

## Results

These are the results of our agent against a random player, evaluated when starting as the first player, as well as when starting as the second player, with a total of 50,000 games for each scenario:
- Games won starting as first player: $90.6$%
- Games won starting as second player: $84.4$%
  
In total, it won $87.5$% of games against the random player.
On average, our player make 23 moves/game.
