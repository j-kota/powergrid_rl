"""
import grid2op
from grid2op.Reward import GameplayReward, L2RPNReward
env = grid2op.make("l2rpn_2019", reward_class=L2RPNReward, other_rewards={"gameplay": GameplayReward})
obs = env.reset()
act = env.action_space()  
obs, reward, done, info = env.step(act) 
"""


import os
import warnings
import grid2op
from grid2op.Episode import EpisodeReplay
from grid2op.Agent import GreedyAgent, RandomAgent, BaseAgent
from grid2op.Runner import Runner
from tqdm import tqdm


path_agents = "./" # "agent_pseudo_random"
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    env = grid2op.make("rte_case14_realistic")
    
    


class DoNothingAgent(BaseAgent):
    """
    This is the most basic BaseAgent. It is purely passive, and does absolutely nothing.
    """
    def __init__(self, action_space):
        BaseAgent.__init__(self, action_space)


    def act(self, observation, reward, done=False):
        """
        As better explained in the document of :func:`grid2op.BaseAction.update` or
        :func:`grid2op.BaseAction.ActionSpace.__call__`.

        The preferred way to make an object of type action is to call :func:`grid2op.BaseAction.ActionSpace.__call__` with
        the
        dictionnary representing the action. In this case, the action is "do nothing" and it is represented by the
        empty dictionnary.

        Parameters
        ----------
        observation: :class:`grid2op.Observation.Observation`
            The current observation of the :class:`grid2op.Environment.Environment`

        reward: ``float``
            The current reward. This is the reward obtained by the previous action

        done: ``bool``
            Whether the episode has ended or not. Used to maintain gym compatibility

        Returns
        -------
        res: :class:`grid2op.Action.Action`
            The action chosen by the bot / controller / agent.

        """
        res = self.action_space({})
        return res



class CustomRandom(RandomAgent):
    
    #This agent takes 1 random action every 10 time steps.
    
    def __init__(self, action_space):
        RandomAgent.__init__(self, action_space)
        self.i = 0

    def my_act(self, transformed_observation, reward, done=False):
        if self.i % 10 != 0:
            res = 0
        else:
            res = self.action_space.sample()
        self.i += 1
        return res


"""
class DoNothing(RandomAgent):
    
    #This agent takes 1 random action every 10 time steps.
    
    def __init__(self, action_space):
        RandomAgent.__init__(self, action_space)
        self.i = 0

    def my_act(self, transformed_observation, reward, done=False):
        return self.action_space({})
"""



# execute this agent on 1 scenario, saving the results
runner = Runner(**env.get_params_for_runner(), agentClass=CustomRandom) #DoNothingAgent)
path_agent = os.path.join(path_agents, "DoNothingAgent")
res = runner.run(nb_episode=1, path_save=path_agent, pbar=tqdm)
# and now reload it and display the "movie" of this scenario
plot_epi = EpisodeReplay(path_agent)
plot_epi.replay_episode(res[0][1],  gif_name="episode")  # second argument max_fps=2 resulted in errors



"""
import grid2op
from grid2op import Agent   # I had to add this line, but why should that be? -JK
env = grid2op.make()
agent = grid2op.Agent.RandomAgent(env.action_space)

reward = env.reward_range[0]
done = False
obs = env.reset()
while not done:
    act = agent.act(obs, reward, done)
    obs, reward, done, info = env.step(act)
"""































