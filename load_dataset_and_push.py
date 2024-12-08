from datasets import load_dataset

# From JSON annotation
ds = load_dataset('json', data_files='data/ja_dev_edited.jsonl')

ds.push_to_hub("akkikiki/global_mmlu_ja_edited")
