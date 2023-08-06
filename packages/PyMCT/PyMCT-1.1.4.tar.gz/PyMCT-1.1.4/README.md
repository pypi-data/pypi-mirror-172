# PyMCT
This is a simple implement for Manto Carlo Tree Search algorithm.

# Install
    
    pip install --upgrade PyMCT

## Example
This is a example for searching a randomly generated tree, each transcation to a new state is given with random reward.

Import moudles:

    from random import randint
    from PyMCT.MCT import MCTNode, MCTS, State

create the test case:

    class Test:
        _root:MCTNode
        _MCTS:MCTS
        
        def __init__(self, root_state:int, c:int=2, max_iter:int=10):       
            root_state = State(root_state)
            self._root = MCTNode(state=root_state)
            #Set the serach with max iteration and max tree heights
            self._MCTS = MCTS(self.root,c=c,max_iter=max_iter, max_height=2, debug=True)
            
        #Always return a random reward. Note that the function must take one MCTNode as argument, and return a value.
        def reward_func(slef, node:MCTNode):
            return randint(0, 10)
        
        #Randomly expand the tree with new node. Note that the function must take one MCTNode as argument, and return a list of new states.
        def discover_func(self, node:MCTNode):
            new_states = list()
            for i in range(randint(1,10)):
                new_states.append(State(i))
            return new_states

        def run(self):
            #Pass in the reward and discover function, start the algorithm!
            self.MCTS.iterate(self.reward_func, self.discover_func)
            
            #Find the optimal path.
            self.MCTS.find_optimal_path()
            
            #Display the tree, Note that if no tag is given to MCTNode, a random tag will be generated and display here.
            self.MCTS.render_tree()
            
            #Print the oprimal path. This is the list of MCTNodes.
            print(self.MCTS.optimal_path)
        
        @property
        def root(self):
            return self._root
        
        @property
        def MCTS(self):
            return self._MCTS

run the test:

    if __name__ == '__main__':
        test = Test(0)
        test.run()
    
