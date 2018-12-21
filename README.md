# Anbindung eines multi-kontextuellen Systems an die Rasa-Dialogsystem-Engine zur Unterstützung von Studierenden


## Installation
__Chatbot__ 
Recommended to use a python venv.  
Firstly you have to install all needed packages and their requirements:
```
$ python -m pip install -r requirements.txt
```
Afterwards install spacy and the model you want to use (needed for rasa_nlu):
```
$ python -m pip install rasa_nlu[spacy]
$ python -m spacy download en_core_web_<sm/md/lg>
$ python -m spacy link en_core_web_<sm/md/lg> en
```
(you might need administrative rights to link the spacy model)



If you want to generate nlp-trainings data make sure you have node
installed and doa `npm install` to install the requirements

## Running the bot locally
#####To train the dialogue and nlu use the following commands:
```
<del>run.py train-nlu #NLU
run.py train-dialogue #DIALOG</del>
```
This seems to be the 'rasa'-way
```
python -m rasa_nlu.train -c chatbot/nlu_pipeline_spacy.yml --data nlu_data_generation/_generated_data\rasa_dataset_training.json -o chatbot/models/nlu --fixed_model_name current --project default --debug -t 4
```
```
python -m rasa_core.train -s chatbot\data\dialogue_stories -o chatbot\models\dialogue01 -d chatbot\domain.yml --history 3 --epochs 400 --nlu_threshold 0.65 --core_threshold 0.4 --fallback_action_name action_fallback
```

tensorflow_embedded takes ~1:30h on i7-4790K
spacy takes ~1:10h on i7-4790K
#####To run the bot locally with debug-output run the following command:
this changed with rasa_core `0.11.2`
```
<del>python -m rasa_core.run -d chatbot/models/dialogue -u chatbot/models/nlu/default/current --debug</del>
```
rasa_core `0.11.2`
```
# running rasa_core server:
python -m rasa_core.run -d chatbot/models/dialogue -u chatbot/models/nlu/default/current --endpoints chatbot/endpoints.yml --debug

# running rasa_core_sdk server (providing custom actions):
python -m rasa_core_sdk.endpoint --actions chatbot.actions
```

if you want to use the telegram channel:
```
python -m rasa_core.run -d chatbot/models/dialogue -u chatbot/models/nlu/default/current --endpoints chatbot/endpoints.yml -p 5005 -c telegram --credentials credentials.yml
```
interactive training:
```
python -m rasa_core.train --online -u chatbot/models/nlu/tensorflow/test03 -o model_test\dialogue03 -d chatbot\domain.yml -s chatbot\data\dialogue_stories --endpoints chatbot\endpoints.yml --dump_stories --epochs 400 --nlu_threshold 0.65 --core_threshold 0.4 --fallback_action_name action_fallback
```
#####Chatito

To generate training data using chatito
```
npx chatito .\nlu_data_generation --format=rasa --outputPath=.\nlu_data_generation\_generated_data
alternatively if you don't want to change the output-directory
npm run chatito
```
## Anmerkungen
- a = MTSModule.select().join(MTSModuleCourseRegulations).join(CourseRegulation).where((CourseRegulation.name.contains('technische informatik')) & (MTSModule.title.contains("analysis")))
- moduleTitle auch per genauer Suchanfrage
- 30 bis 40 Seiten
- related work
- Implentierung
- memoization an/aus
- anzahl der Stories
- code in Arbeit
## Fragen
__Fragen aktuell__
- peewee anfragen besser über joins?
- verknüpfung courseRegulation zu MTSModules vollständig?
--> Analysis nicht in Pflichtbereich
- Menü für Wochentag, außer Samstag und Sonntag --> nächster Montag
- chatito für nlu data sollte gut sein

__Fragen 17/08__
- Legitim/gut/schlecht als erstes nach Kontext zu fragen und am Ende eines Dialogzweigs zu fragen 
wie die nächste Anfrage ablaufen soll?
- entity recognition: modulTitles, personen Namen als synonyme?
--> rasa nlu im server
- Anfrage nach vegetarischem Essen ist ziemlich teuer: Erst alle Mensen anfragen dann nach vegetarischen Gerichten gucken
--> cachen von Anfragen, timestamp
- Stories text slots: der genaue Slot-Wert ist egal (außer memoization??), nur ob er gefüllt ist oder nicht?
-- Ja nur für memoization
- Problem(?): mehrfache queries/requests, einmal zum validieren der Daten und dann zum ausgeben der zusammengefügten anfragen
--> auch cache
- Problem(?): list slot speichert nur letzte entity
--> 

- UX design

## TODO
__module:__
- ects
- person

__mensa:__

__if time:__
- coursedate function
- opening hours function

__Nice-to-haves:__
- set student/employee/extern