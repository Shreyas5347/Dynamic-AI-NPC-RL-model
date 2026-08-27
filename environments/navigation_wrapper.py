import gymnasium as gym


class NavigationActionWrapper(
    gym.ActionWrapper
):

    def __init__(self, env):

        super().__init__(env)

        # Only:
        # 0 = left
        # 1 = right
        # 2 = forward

        self.action_space = gym.spaces.Discrete(3)


    def action(self, action):

        return int(action)