General Thoughts
---
- Die models können einfach übernommen werden?


Fragen
---
__ModuleCrawler__
- Versionen werden so lange erhöht bis 404?
- was ist mit Ersatzterminen?
- course: annotations, detailed_description und requirements (fast) immer leer
- mehrere Personen für ein Modul?
- filter Klasse: Funktion? Übernehmen?
- Electronic Script / English Script
- django: 
- Unterschiede spaCy-Modelle


HINTS
---

show current state of slots
```
tracker = agent.tracker_store.get_or_create_tracker("default") 
# get current tracker state
tracker.current_state()
```