import numpy as np
from rlberry.agents.bandits import BanditWithSimplePolicy
import logging

logger = logging.getLogger(__name__)

# TODO : fix bug when doing several fit, the fit do not resume. Should define
#        self.rewards and self.action and resume training.


class IndexAgent(BanditWithSimplePolicy):
    """
    Agent for bandit environment using Index-based policy like UCB.

    Parameters
    -----------
    env : rlberry bandit environment
        See :class:`~rlberry.envs.bandits.Bandit`.

    index_function : callable or None, default = None
        Compute the index for an arm using the past rewards on this arm and
        the current time t. If None, use UCB bound for Bernoulli.


    Examples
    --------
    >>> from rlberry.agents.bandits import IndexAgent
    >>> import numpy as np
    >>> class UCBAgent(IndexAgent):
    >>>     name = "UCB"
    >>>     def __init__(self, env, **kwargs):
    >>>     def index_function(tr):
    >>>         return [
    >>>             tr.read_last_tag_value("mu_hat", arm)
    >>>             + np.sqrt(
    >>>                 np.log(tr.read_last_tag_value("t") ** 2)
    >>>                 / (2 * tr.read_last_tag_value("n_pulls", arm))
    >>>             )
    >>>             for arm in tr.arms
    >>>         ]
    >>>         IndexAgent.__init__(self, env, index, **kwargs)

    """

    name = "IndexAgent"

    def __init__(self, env, index_function=None, **kwargs):
        BanditWithSimplePolicy.__init__(self, env, **kwargs)
        if index_function is None:

            def index_function(tr):
                return [
                    tr.read_last_tag_value("mu_hat", arm)
                    + np.sqrt(
                        np.log(tr.read_last_tag_value("t") ** 2)
                        / (2 * tr.read_last_tag_value("n_pulls", arm))
                    )
                    for arm in tr.arms
                ]

        self.index_function = index_function

    def fit(self, budget=None, **kwargs):
        """
        Train the bandit using the provided environment.

        Parameters
        ----------
        budget: int
            Total number of iterations, also called horizon.
        """
        horizon = budget
        total_reward = 0.0
        indices = np.inf * np.ones(self.n_arms)

        for ep in range(horizon):
            # Warmup: play every arm one before starting computing indices
            if ep < self.n_arms:
                action = ep
            else:
                indices = self.index_function(self.tracker)
                action = np.argmax(indices)

            _, reward, _, _ = self.env.step(action)

            # Feed the played action and the resulting reward to the tracker.
            self.tracker.update(action, reward)

            total_reward += reward

        self.optimal_action = np.argmax(indices)
        info = {"episode_reward": total_reward}
        return info
