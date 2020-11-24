from rlberry.agents.ppo import PPOAgent
from rlberry.agents.avec import AVECPPOAgent
from rlberry.envs.benchmarks.ball_exploration.ball2d import get_benchmark_env


def test_ppo_agent():
    env = get_benchmark_env(level=1)
    n_episodes = 5
    horizon = 30

    agent = PPOAgent(env,
                     n_episodes=n_episodes,
                     horizon=horizon,
                     gamma=0.99,
                     learning_rate=0.001,
                     eps_clip=0.2,
                     k_epochs=4,
                     verbose=0)
    agent.fit()


def test_avec_ppo_agent():
    env = get_benchmark_env(level=1)
    n_episodes = 5
    horizon = 30

    agent = AVECPPOAgent(env,
                         n_episodes=n_episodes,
                         horizon=horizon,
                         gamma=0.99,
                         lr=0.001,
                         eps_clip=0.2,
                         k_epochs=4,
                         verbose=0)
    agent.fit()