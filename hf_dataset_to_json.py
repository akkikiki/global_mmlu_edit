import datasets
from datasets import load_dataset

#global_mmlu_ja = load_dataset("CohereForAI/Global-MMLU", 'ja')
#global_mmlu_ja["dev"].to_json("data/global_mmlu_dev_ja.json")

global_mmlu_ja = load_dataset("CohereForAI/Global-MMLU", 'en')
global_mmlu_ja["dev"].to_json("data/global_mmlu_dev_en.json")
