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