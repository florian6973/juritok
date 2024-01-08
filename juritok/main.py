import pandas as pd
from pathlib import Path
import sentencepiece as spm
import argparse


# https://github.com/google/sentencepiece/blob/master/doc/options.md
def build_trainer(sentence_array):
    input_text = "\n\n".join(sentence_array)

    print("Writing input text")
    with open("jorf_2023.txt", "w", encoding="utf-8") as f:
        f.write(input_text)

    vocab_size = 1000
    input_sentence_size = 100000

    print("Training SentencePiece")
    # spm.SentencePieceTrainer.Train('--input=jorf_2023.txt --model_prefix=juritok --vocab_size=32000 --model_type=bpe --character_coverage=1.0 --pad_id=0 --unk_id=1 --bos_id=-1 --eos_id=-1 --pad_piece=[PAD] --unk_piece=[UNK] --bos_piece=[BOS] --eos_piece=[EOS] --user_defined_symbols=[SEP],[CLS],[MASK]')
    spm.SentencePieceTrainer.Train(
        f"--input=jorf_2023.txt "
        f"--vocab_size={vocab_size} "
        f"--model_prefix=spm "
        f"--input_sentence_size={input_sentence_size} "
        f"--model_type=bpe "
    )

    print("Loading SentencePiece")
    sp = spm.SentencePieceProcessor()
    sp.Load("spm.model")

    return sp

def test_model(sp, sentence):
    encoded = sp.EncodeAsPieces(sentence)
    print(sp.EncodeAsPieces(sentence))
    print(sp.EncodeAsIds(sentence))
    print(sp.DecodePieces(encoded))

def get_data():
    path = Path(__file__) / "../jorf_2023.feather"
    path_csv = Path(__file__) / "../jorf_2023.csv"

    if not path.exists():
        print("Converting CSV to Feather")
        csv = pd.read_csv(path_csv, sep='|', encoding='utf-8', low_memory=False, header=None)
        csv.to_feather(path)

    print("Reading Feather")
    data = pd.read_feather(path)
    print(data.head())
    return data[5]

def keep_law_only(data):
    return data[data[5].str.startswith("«")]


def main():
    print("JURITOK - Main")
    argparser = argparse.ArgumentParser()
    # argparser.add_argument("--train", action="store_true")
    args = argparser.parse_args()

    data = get_data()

    data = data.iloc[:1000]

    # data = keep_law_only(data)

    sp_all = build_trainer(data)
    sp_law = build_trainer(data[data.str.startswith("«")])
    test_sentence = "« Le présent décret entre en vigueur le 1er janvier 2023. »"
    test_model(sp_all, test_sentence)
    test_model(sp_law, test_sentence)


    
