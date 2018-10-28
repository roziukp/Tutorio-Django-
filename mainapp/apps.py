from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class MainappConfig(AppConfig):
    name = 'mainapp'

class SuitConfig(DjangoSuitConfig):
    name = 'suit'