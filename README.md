# Cite Me If You Can
 Will AI replace scientists?
 Maybe will, maybe won't, but I'm sure it is helpful for scientists.

## Ingestion Pipeline Architecture Design
1. Scheduled Daily New File Detection and Duplicate Filtering System  
   Scheduled Execution:  
   A cronjob or scheduler runs a detection script at the same time every day to automatically scan the secure upload folder for new journal files.  
   
   New File Detection:  
   The system compares the list of files currently in the upload directory against a record of previously processed files to identify newly added documents.  
   
   Duplicate Detection Using Cosine Similarity:  
   For each newly detected file, the system extracts its textual content and generates an embedding vector. It then compares this vector to embeddings of all previously ingested documents using cosine similarity.  
   
   Duplicate Filtering Threshold:  
   If the cosine similarity between the new document and any existing document exceeds 99%, the new file is considered a near-duplicate and is excluded from further ingestion processing.  
   
   Pipeline Continuation:  
   Only files that are confirmed as sufficiently unique (below the similarity threshold) proceed to downstream ingestion steps such as chunking, indexing, and embedding storage.  
   
   Outcome:  
   This scheduled system ensures systematic daily ingestion of genuinely new content while preventing redundant processing of near-duplicate journal articles.

2. Chunking Strategy for Scientific Articles    
   Chunking is a critical and sensitive step in ensuring that user prompts retrieve relevant content, return accurate information, and ultimately meet the user’s expectations. To perform effective chunking, it is essential to understand the structure and nature of the source material and apply a strategy tailored to it.

   Scientific articles typically follow a standardized structure consisting of sections such as Abstract, Introduction, Materials and Methods, Results, Discussion, and Conclusion. Each of these sections carries its own semantic, conceptual, and contextual integrity. Therefore, the chunking process should treat each section as a separate unit when parsing the content.

   Within these sections, paragraphs represent the smallest coherent units of meaning and logical flow. In scientific writing, paragraphs are carefully constructed to convey a single idea or finding, making them ideal candidates for chunk boundaries.

   As such, the proposed chunking strategy is to:

      1. First, segment the article by its main sections (e.g., Introduction, Results).

      2. Then, split each section into individual paragraphs, treating each paragraph as a distinct chunk.

   This approach preserves both the structural and semantic coherence of the content, enabling better embedding representation, improved retrieval accuracy, and more contextually grounded responses from the generative AI system.

3. Embedding Strategy – Using SPECTER2    
   The selected embedding model for this system is SPECTER2, a transformer-based model specifically trained on scientific literature.  
   
   Given that the overall use case involves processing scientific articles and generating answers based on their content, it is crucial to use an embedding model that understands the structure, language, and flow of academic writing. SPECTER2 excels in this domain, as it has been trained not only on scientific text but also on citation relationships, allowing it to capture the semantic relevance between documents in a way that aligns with scholarly communication.    
   
   Compared to general-purpose embedding models, SPECTER2 consistently outperforms alternatives in tasks such as scientific paper retrieval, similarity search, and citation prediction. Its focus on citation-informed representations makes it particularly well-suited for grounding generative AI outputs in credible, research-backed sources.   
   
   By leveraging SPECTER2, the system ensures that each chunk of scientific content is embedded with a deep understanding of its academic context, ultimately enabling more accurate and trustworthy retrieval and response generation.