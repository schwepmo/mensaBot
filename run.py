from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.fallback import FallbackPolicy


def train_dialogue(domain_file="chatbot/domain.yml",
                   model_path="chatbot/models/dialogue",
                   training_data_file="chatbot/data/dialogue_stories"):
    fallback = FallbackPolicy(fallback_action_name="action_reset_dialogue",
                              core_threshold=0.25,
                              nlu_threshold=0.25)
    agent = Agent(domain_file, policies=[KerasPolicy(), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    # training_data = load_data('chatbot/data/nlu_data.md')
    training_data = load_data('nlu_data_generation/_generated_data/rasa_dataset_training.json')
    trainer = Trainer(config.load("chatbot/nlu_model_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('chatbot/models/nlu/', fixed_model_name="current")

    return model_directory


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue"],
            help="what the bot should do - e.g. train-nlu or train-dialogue?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
