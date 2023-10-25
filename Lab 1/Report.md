All the following is valid for the work done after monday (23/10/2023) when professor told us that the h function in a* algorithm needs to be optimistic and not pessimistic.

Firstly I tried to implement a simple h function -simple_h- that just returned 0 if we were covering all states, and 1 otehrwise.

I also worked on the is_overlapping and num_of_overlap optimizations, that will be introduces later.

After professor shown us the actual a* algorithm (with notebook set-covering_path-search.ipynb).
The showed h function calculate the distance to the solution, taking into consideration how the
not taken sets can help reaching the goal.
I thought about improving the h function, but nothing came to my mind. 

So I focused on 4 optimizations:

1. is_overlapping function: In the search function, we don't need to explore actions that do not allow us to cover new state.
2. queued_taken_state: In the search function, I check if current_state.taken | action is a state already queued. If queued we won't queue it anymore (since the insertion operation in the priority queue is linear).
3. Finally I focused on minimizing the number of overlap. This is not an optimization of the a* (since the number of steps increases), but is an optimization on the quality of the solution. 
if a =([True, False, True]   and b =  ([True, False, True]    
       [False, True, True])            [False, True, False])
    In some condition we may want b as a solution. 
    So I added a flag (minimize_overlap) in the a_star_func that is set as default to False.
    When flagged True, the a_star_func returns the sum of g, h and num_of_overlap, that returns the number of overlap (in a range between 0,1 so that it won't influence too much the distance function).


I finally tested the a* algorithm (with and without optimizations) on 100 different instatiation of the set_covering problem. Here are the results: 
1) without optimizations (professor implementation): 
    avg steps: 71.56, avg execution times: 0.27638682126998904, avg overlap: 6.53
2) with is_overlappings:
    avg steps: 67.63, avg execution times: 0.2577618145942688, avg overlap: 6.38
3) with queued_state_taken:
    avg steps: 63.82, avg execution times: 0.18714907884597778, avg overlap: 6.37
4) Minimizing overlap:
    avg steps: 101.62, avg execution times: 0.313340585231781, avg overlap: 4.27

Notice: The minimizing overlapping idea was developed together with Andrea Pellegrino