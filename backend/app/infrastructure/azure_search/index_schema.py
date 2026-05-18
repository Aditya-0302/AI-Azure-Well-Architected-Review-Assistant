from __future__ import annotations

from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)

from app.core.config import Settings


def build_knowledge_index(settings: Settings) -> SearchIndex:
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        SimpleField(name="tenant_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="project_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(
            name="architecture_version_id",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SearchableField(name="content", type=SearchFieldDataType.String, retrievable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=settings.rag_embedding_dimensions,
            vector_search_profile_name=settings.rag_vector_profile_name,
        ),
        SimpleField(name="content_hash", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="ordinal", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(
            name="token_estimate",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
        ),
        SearchableField(
            name="file_name",
            type=SearchFieldDataType.String,
            filterable=True,
            sortable=True,
        ),
        SimpleField(name="source_uri", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="document_type", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="sensitivity_label", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="pillars",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
            facetable=True,
        ),
        SearchField(
            name="azure_services",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
            facetable=True,
        ),
        SimpleField(name="ingested_at", type=SearchFieldDataType.String, filterable=True, sortable=True),
        SearchableField(name="metadata_json", type=SearchFieldDataType.String, retrievable=True),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name=settings.rag_vector_algorithm_name)],
        profiles=[
            VectorSearchProfile(
                name=settings.rag_vector_profile_name,
                algorithm_configuration_name=settings.rag_vector_algorithm_name,
            )
        ],
    )

    semantic_search = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name=settings.rag_semantic_configuration_name,
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="file_name"),
                    content_fields=[SemanticField(field_name="content")],
                    keywords_fields=[
                        SemanticField(field_name="pillars"),
                        SemanticField(field_name="azure_services"),
                    ],
                ),
            )
        ]
    )

    return SearchIndex(
        name=settings.resolved_rag_index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )

