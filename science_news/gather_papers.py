
#--------------------------------

# Imports
import arxiv
from semanticscholar import SemanticScholar
#--------------------------------

# Something about science
def gather_papers():
    arxiv_search_client = arxiv.Client()
    scholar_search_clien = SemanticScholar()

    search = arxiv.Search(
        # Computer Science, Physics, Biology, Chemistry
        query="cat:cs.* OR cat:physics.* OR cat:q-bio.* OR cat:chem-ph",
        max_results=30,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    arxiv_ID_list = []
    for r in arxiv_search_client.results(search):
        raw_id = r.entry_id.split("/")[-1]       # 2602.12281v1
        base_id = raw_id.split("v")[0]           # 2602.12281
        arxiv_ID_list.append(f"ARXIV:{base_id}") # tag that bad boy
        #print(r.title, r.primary_category)

    print(arxiv_ID_list)
    papers_enriched = scholar_search_clien.get_papers(arxiv_ID_list)
    print(papers_enriched)
#--------------------------------

# Temporary main
if __name__ == "__main__":
    gather_papers()
