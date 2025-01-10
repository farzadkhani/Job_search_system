from ..models import ElasticsearchService

es_service = ElasticsearchService()


def index_document(sender, index_name, document):
    """
    master function to index a document in elasticsearch

    TODO: manage sender model
    """

    es_service.index(document, index_name=index_name)


def delete_document(document_id, index_name):
    """
    master function to delete a document in elasticsearch.

    TODO: manage sender model
    """

    es_service.delete(document_id=str(document_id), index_name=index_name)
