from __future__ import absolute_import
import logging
import spacy
from config import ServiceConfig
from connector.AbstractDbConnector import AbstractDbConnector
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForPreTraining

from src.models.Aquila import Aquila
from src.models.Llava import Llava
from src.models.Owl import Owl
from src.models.VILT import VILT


class QAService:

    def __init__(self, config: ServiceConfig, connector: AbstractDbConnector):
        self.vaq_model = None
        self.config = config
        self.connector = connector
        logging.basicConfig(level=logging.INFO, filename=self.config.database.logfile)
        console = logging.StreamHandler()
        logging.getLogger('').addHandler(console)
        self.setup_network()

    def ask_question(self, text_input, image):
        return self.vaq_model.ask(image, text_input)


    def setup_network(self):
        if self.config.model.type_model == 'aquila':
            self.vaq_model = Aquila()
            pass
        elif self.config.model.type_model == 'llava':
            self.vaq_model = Llava()
            pass
        elif self.config.model.type_model == 'vilt':
            self.vaq_model = VILT()
            pass
        elif self.config.model.type_model == 'owl':
            self.vaq_model = Owl()
            pass
        pass
