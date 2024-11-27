from __future__ import absolute_import
import logging
import spacy
from config import ServiceConfig
from connector.AbstractDbConnector import AbstractDbConnector


class NERService:

    def __init__(self, config: ServiceConfig, connector: AbstractDbConnector):
        self.config = config
        self.connector = connector
        self.nlp = spacy.load(self.config.spacy.path)
        logging.basicConfig(level=logging.INFO, filename=self.config.database.logfile)
        console = logging.StreamHandler()
        logging.getLogger('').addHandler(console)

    def returns_all_entities(self, text_input):
        doc = self.nlp(text_input)

        entities = []
        for ent in doc.ents:
            entities.append({"entity": str(ent.text), "type": str(ent.label_)})
        return entities

    def return_list_of_locations_from_text(self, text_input):
        doc = self.nlp(text_input)

        gpe = []  # countries, cities, states
        loc = []  # non gpe locations, mountain ranges, bodies of water
        rest = []
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                gpe.append(ent.text)
            elif ent.label_ == 'LOC':
                loc.append(ent.text)
            else:
                rest.append(ent)
        return gpe + loc, rest
