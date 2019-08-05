# TU-Berlin Mensa Chatbot

## Work in progress

This project is a work in progress. I originally build this bot for my bachelor thesis. It was really inconsistent and
not user friendly. In my free time I am now trying to revamp the bot to hopefully have a functioning bot in the future.

## Roadmap

- 05.08.2019: Deleting unnecessary stuff and updating libraries to the newest versions

## Overview

I am using Rasa (https://rasa.com) for the chatbot. All shown data is collected from the Studieredenwerk-Website
(https://www.stw.berlin/) using the request library and parsing it using beautiful-soup.

## Installation

Use a virtual environment. Conda or pip is fine, although I am using pip.
- Start of by following the rasa-docs to install rasa (https://rasa.com/docs/rasa/1.2.0/user-guide/installation/).
They change their preferred way of installing it from time to time. The link should have the instructions for the
used version.
- All other requirements can be installed using:
```
python -m pip install -r requirements.txt
```
- Finally install the used backend for the nlu-component (you might need administrative rights to link the spacy model):
```
python -m pip install rasa_nlu[spacy]
python -m spacy download de_core_web_<sm/md/lg>
python -m spacy link en_core_web_<sm/md/lg> en
```

## Training the bot

### Training the dialogue-model

```
python -m rasa_core.train -s chatbot\data\dialogue_stories -o chatbot\models\dialogue01 -d chatbot\domain.yml --history 3 --epochs 400 --nlu_threshold 0.65 --core_threshold 0.4 --fallback_action_name action_fallback
```
### Training the nlu-model

```
python -m rasa_nlu.train -c chatbot/nlu_pipeline_spacy.yml --data nlu_data_generation/_generated_data\rasa_dataset_training.json -o chatbot/models/nlu --fixed_model_name current --project default --debug -t 4
```
## Running the bot locally

### Running the rasa_core_sdk server
This will start a server on localhost:5055 which will execute the actions defined in the dialogue. 
```
python -m rasa_core_sdk.endpoint --actions chatbot.actions
```

### Running the bot
```
python -m rasa_core.run -d chatbot/models/dialogue -u chatbot/models/nlu/default/current --endpoints chatbot/endpoints.yml --debug
````

if you want to use the telegram channel:
```
python -m rasa_core.run -d chatbot/models/dialogue -u chatbot/models/nlu/default/current --endpoints chatbot/endpoints.yml -p 5005 -c telegram --credentials credentials.yml
```

interactive training:
```
python -m rasa_core.train --online -u chatbot/models/nlu/tensorflow/test03 -o model_test\dialogue03 -d chatbot\domain.yml -s chatbot\data\dialogue_stories --endpoints chatbot\endpoints.yml --dump_stories --epochs 400 --nlu_threshold 0.65 --core_threshold 0.4 --fallback_action_name action_fallback
```

## Optional: Generating a larger nlu dataset using Chatito:

As part of my thesis I tried using chatito to generate more training data using chatito (https://github.com/rodrigopivi/Chatito).
I did this because I had a huge amount of entities. I'm not sure this will still be necessary in the future.

Make sure you have npm installed. Then you can just call `npm install` and chatito should be installed. 

To generate training data using chatito call:

```
npx chatito .\nlu_data_generation --format=rasa --outputPath=.\nlu_data_generation\_generated_data
```
Alternatively if you don't want to change the output-directory:
```
npm run chatito
```