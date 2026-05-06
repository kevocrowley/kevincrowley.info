# Building RAG Pipelines with AWS Bedrock Knowledge Bases

Retrieval Augmented Generation (RAG) has become the standard approach for building AI applications that need to reference specific information. In this post, I'll walk through implementing RAG using AWS Bedrock Knowledge Bases with OpenSearch Serverless.

## Overview

The architecture consists of:
- **Data Ingestion**: Documents stored in S3, processed and chunked
- **Vector Store**: OpenSearch Serverless for semantic search
- **Knowledge Base**: Bedrock's managed RAG solution
- **Agent**: Bedrock Agent for answering questions

## Step 1: Set Up S3 Bucket for Documents

First, create an S3 bucket to store your documents:

```python
import boto3

s3 = boto3.client('s3')
s3.create_bucket(Bucket='your-documents-bucket')
```

## Step 2: Create OpenSearch Serverless Collection

```python
import boto3

opensearch = boto3.client('opensearchserverless')

response = opensearch.create_collection(
    name='bedrock-knowledge-base',
    type='VECTORSEARCH'
)
```

## Step 3: Create Bedrock Knowledge Base

```python
bedrock = boto3.client('bedrock')

kb_response = bedrock.create_knowledge_base(
    name='company-docs-kb',
    embeddingModel='amazon.titan-embed-text-v1',
    vectorStore={
        'type': 'OPENSEARCH_SERVERLESS',
        'opensearchServerlessConfiguration': {
            'collectionArn': 'your-collection-arn',
            'vectorIndexName': 'bedrock-index'
        }
    }
)
```

## Step 4: Sync Data Source

```python
bedrock.create_data_source(
    knowledgeBaseId='your-kb-id',
    name='s3-data-source',
    dataSourceConfiguration={
        's3Configuration': {
            'bucketArn': 'arn:aws:s3:::your-bucket'
        }
    }
)
```

## Querying the Knowledge Base

```python
response = bedrock.retrieve(
    retrievalQuery={
        'text': 'What is our return policy?'
    },
    knowledgeBaseId='your-kb-id'
)
```

## Key Considerations

1. **Chunk Size**: Start with 512-1024 tokens, adjust based on your use case
2. **Embedding Model**: Amazon Titan provides good quality/performance balance
3. **Data Sync**: Set up incremental sync for updated documents

## Conclusion

Bedrock Knowledge Bases provides a managed solution for RAG that integrates seamlessly with other AWS services. The key is proper document preparation and chunking strategy.

---

*Tags: AWS, Bedrock, RAG, OpenSearch*