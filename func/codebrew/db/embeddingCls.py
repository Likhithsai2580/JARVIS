from rich import print
from rich.table import Table

class Model:
    def __init__(self,
                model_name:str,
                peformance_Sentence_Embedding:float,
                peformance_Semantic_Search:float,
                avg_Peformance:float,
                speed:float,
                model_Size_MB:float) -> None:
        self.model_name = model_name
        self.peformance_Sentence_Embedding = peformance_Sentence_Embedding
        self.peformance_Semantic_Search = peformance_Semantic_Search
        self.avg_Peformance = avg_Peformance
        self.speed = speed
        self.model_Size_MB = model_Size_MB

    def __repr__(self) -> str:
        return f"Model(Name: {self.model_name}, Peformance_Sentence_Embedding: {self.peformance_Sentence_Embedding}, Peformance_Semantic_Search: {self.peformance_Semantic_Search}, Avg_Peformance: {self.avg_Peformance}, Speed: {self.speed}, Model_Size_MB: {self.model_Size_MB})"
    

all_mpnet_base_v2 = Model("all-mpnet-base-v2", 69.57, 57.02, 63.30, 2800, 420)
multi_qa_mpnet_base_dot_v1 = Model("multi-qa-mpnet-base-dot-v1", 66.76, 57.60, 62.18, 2800, 420)
all_distilroberta_v1 = Model("all-distilroberta-v1", 68.73, 50.94, 59.84, 4000, 290)
all_MiniLM_L12_v2 = Model("all-MiniLM-L12-v2", 68.70, 50.82, 59.76, 7500, 120)
multi_qa_distilbert_cos_v1 = Model("multi-qa-distilbert-cos-v1", 65.98, 52.83, 59.41, 4000, 250)
all_MiniLM_L6_v2 = Model("all-MiniLM-L6-v2", 68.06, 49.54, 58.80, 14200, 80)
multi_qa_MiniLM_L6_cos_v1 = Model("multi-qa-MiniLM-L6-cos-v1", 64.33, 51.83, 58.08, 14200, 80)
paraphrase_multilingual_mpnet_base_v2 = Model("paraphrase-multilingual-mpnet-base-v2", 65.83, 41.68, 53.75, 2500, 970)
paraphrase_albert_small_v2 = Model("paraphrase-albert-small-v2", 64.46, 40.04, 52.25, 5000, 43)
paraphrase_multilingual_MiniLM_L12_v2 = Model("paraphrase-multilingual-MiniLM-L12-v2", 64.25, 39.19, 51.72, 7500, 420)
paraphrase_MiniLM_L3_v2 = Model("paraphrase-MiniLM-L3-v2", 62.29, 39.19, 50.74, 19000, 61)
distiluse_base_multilingual_cased_v1 = Model("distiluse-base-multilingual-cased-v1", 61.30, 29.87, 45.59, 4000, 480)
distiluse_base_multilingual_cased_v2 = Model("distiluse-base-multilingual-cased-v2", 60.18, 27.35, 43.77, 4000, 480)

models = [
    all_mpnet_base_v2,
    multi_qa_mpnet_base_dot_v1,
    all_distilroberta_v1,
    all_MiniLM_L12_v2,
    multi_qa_distilbert_cos_v1,
    all_MiniLM_L6_v2,
    multi_qa_MiniLM_L6_cos_v1,
    paraphrase_multilingual_mpnet_base_v2,
    paraphrase_albert_small_v2,
    paraphrase_multilingual_MiniLM_L12_v2,
    paraphrase_MiniLM_L3_v2,
    distiluse_base_multilingual_cased_v1,
    distiluse_base_multilingual_cased_v2
]

def ShowAllModels():
    table = Table(title="Model Performance Comparison")

    table.add_column("Model Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Performance Sentence Embedding", justify="right", style="magenta")
    table.add_column("Performance Semantic Search", justify="right", style="magenta")
    table.add_column("Avg Performance", justify="right", style="magenta")
    table.add_column("Speed", justify="right", style="green")
    table.add_column("Model Size (MB)", justify="right", style="yellow")

    for model in models:
        table.add_row(
            model.model_name,
            f"{model.peformance_Sentence_Embedding:.2f}",
            f"{model.peformance_Semantic_Search:.2f}",
            f"{model.avg_Peformance:.2f}",
            f"{model.speed:.2f}",
            f"{model.model_Size_MB:.2f}"
        )

    print(table)
if __name__=="__main__":
    ShowAllModels()