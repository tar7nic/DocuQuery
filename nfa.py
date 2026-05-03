from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://081b516f-46bd-48ae-b1cb-d84fcd343bfc.eu-central-1-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6OTkxZWE5MzItYjExMS00NGYxLWI0NjEtZmM3NmEzZWZhYTg3In0.m2SRc3lNG8zBKXLTd_UC-tUPYtuj_65TEv2Axs8f_9w",
)

print(qdrant_client.get_collections())


eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6OTkxZWE5MzItYjExMS00NGYxLWI0NjEtZmM3NmEzZWZhYTg3In0.m2SRc3lNG8zBKXLTd_UC-tUPYtuj_65TEv2Axs8f_9w
https://081b516f-46bd-48ae-b1cb-d84fcd343bfc.eu-central-1-0.aws.cloud.qdrant.io