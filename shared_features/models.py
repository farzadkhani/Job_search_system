from django.db import models
from django.conf import settings

from elasticsearch import Elasticsearch

from shared_features.mixins import ModelMixin


class Skill(ModelMixin):
    """Skill model"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ElasticsearchService:
    def __init__(self, hosts=None):
        self.client = Elasticsearch(hosts=settings.ELASTICSEARCH_PARAMETERS["address"])

    def index(self, document: dict, index_name: str) -> None:
        self.client.index(index=index_name, body=document)

    def search(self, query: str, index_name: str) -> list:
        response = self.client.search(
            index=index_name, body={"query": {"query_string": {"query": query}}}
        )
        return response["hits"]["hits"]

    def delete(self, document_id: str, index_name: str) -> None:
        self.client.delete(index=index_name, id=document_id)
