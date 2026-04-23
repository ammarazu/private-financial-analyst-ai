# Project Specification — Private Financial Analyst AI

## System Requirements

### Input
- PDF documents up to 100MB
- Supported types: annual reports, SEC filings, 
  earnings transcripts, research reports
- Multiple documents per session
- Metadata: company name, date, document type

### Processing
- Parse with Unstructured.io
- Strip PII with Presidio before any LLM call
- Chunk into 500-token segments with 50-token overlap
- Embed with HuggingFace all-MiniLM-L6-v2
- Store in Weaviate with hybrid search

### Query
- Natural language questions
- Multi-document retrieval
- Cohere Rerank top 5 results
- LiteLLM routes to AWS Bedrock
- Chain of thought prompting
- Structured JSON response with citations

### Output
- Headline answer
- Detailed analysis
- Supporting evidence with page numbers
- Risk factors identified
- Source document references

### Security
- All PII stripped before LLM
- Prompt injection blocked at input
- Output scanned for sensitive data
- IAM least privilege enforced
- Secrets in AWS Secrets Manager

### Evaluation
- 30 question-answer test pairs
- Ragas faithfulness > 0.75
- Ragas answer relevancy > 0.80
- Automated on every deployment# Project Specification — Private Financial Analyst AI

## System Requirements

### Input
- PDF documents up to 100MB
- Supported types: annual reports, SEC filings, 
  earnings transcripts, research reports
- Multiple documents per session
- Metadata: company name, date, document type

### Processing
- Parse with Unstructured.io
- Strip PII with Presidio before any LLM call
- Chunk into 500-token segments with 50-token overlap
- Embed with HuggingFace all-MiniLM-L6-v2
- Store in Weaviate with hybrid search

### Query
- Natural language questions
- Multi-document retrieval
- Cohere Rerank top 5 results
- LiteLLM routes to AWS Bedrock
- Chain of thought prompting
- Structured JSON response with citations

### Output
- Headline answer
- Detailed analysis
- Supporting evidence with page numbers
- Risk factors identified
- Source document references

### Security
- All PII stripped before LLM
- Prompt injection blocked at input
- Output scanned for sensitive data
- IAM least privilege enforced
- Secrets in AWS Secrets Manager

### Evaluation
- 30 question-answer test pairs
- Ragas faithfulness > 0.75
- Ragas answer relevancy > 0.80
- Automated on every deployment
