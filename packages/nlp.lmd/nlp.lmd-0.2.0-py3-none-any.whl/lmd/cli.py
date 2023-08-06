"""Console script for lmd."""
import argparse
import itertools
import json
import logging
import os
import random
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from itertools import chain
from typing import Dict, List, Optional, Union

import pandas as pd
import torch
import transformers
from datasets import DatasetDict, load_dataset
from tqdm import tqdm
from transformers import (
    AutoModel,
    AutoTokenizer,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)

logger = logging.getLogger(__name__)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    level="INFO",
)

if torch.cuda.is_available():
    dev = "cuda:0"
else:
    dev = "cpu"


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


MODELS = [
    "xlm-roberta-base",
    "bert-base-multilingual-cased",
    "allenai/longformer-base-4096",
    "microsoft/deberta-base",
    "distilbert-base-multilingual-cased",
    "roberta-base",
    "xlnet-base-cased",
    "bert-base-uncased",
    "google/electra-base-discriminator",
    "distilroberta-base",
    "distilbert-base-uncased",
    "albert-base-v2",
]


def parse_args():
    parser = argparse.ArgumentParser(
        "Language Model Decomposition",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--target", type=str, default="bert-base-uncased", help="target model in LMD"
    )
    parser.add_argument(
        "--basis",
        type=str,
        default=None,
        help="basis model in LMD, separated by comma",
    )
    parser.add_argument(
        "--tokenizer-name",
        type=str,
        default="bert-base-uncased",
        help="tokenizer used for generating sequences (used by all models as text input)",
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=512,
        help="max_seq_length",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="batch size for model inference",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        default="wikicorpus",
        help="The name of the dataset (corpus) to use (via the datasets library). E.g., (bookcorpus, None)/(wikicorpus, raw_en)/(wikitext, wikitext-103-v1)",
    )
    parser.add_argument(
        "--dataset-config-name",
        type=str,
        default="raw_en",
        help="The configuration name of the dataset (corpus) to use (via the datasets library). E.g., (bookcorpus, None)/(wikicorpus, raw_en)/(wikitext, wikitext-103-v1)",
    )
    parser.add_argument(
        "--val-split-percentage",
        type=int,
        default=5,
        help="The percentage of the train set used as validation set in case there's no validation split",
    )
    parser.add_argument(
        "--test-split-percentage",
        type=int,
        default=5,
        help="The percentage of the train set used as test set in case there's no test split",
    )
    parser.add_argument(
        "--max-train-samples",
        type=int,
        default=128000,
        help="max train samples",
    )
    parser.add_argument(
        "--max-val-samples",
        type=int,
        default=12800,
        help="max validation samples",
    )
    parser.add_argument(
        "--max-test-samples",
        type=int,
        default=12800,
        help="max test samples",
    )
    parser.add_argument(
        "--preprocessing-num-workers",
        type=int,
        default=None,
        help="preprocessing_num_workers for datasets.map()",
    )
    parser.add_argument(
        "--overwrite_cache",
        type=bool,
        default=False,
        help="if we overwrite cache for datasets.map()",
    )
    parser.add_argument(
        "--preprocess-dir",
        type=str,
        default="data/preprocess",
        help="data dir to save preprocessed datasets",
    )
    parser.add_argument(
        "--embedding-dir",
        type=str,
        default="data/embeddings",
        help="data dir to save embedding datasets",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="data dir to save LMD results",
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default="models",
        help="data dir to save LMD models",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1e-6,
        help="L2 regularization coefficient",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="logging level",
    )
    parser.add_argument(
        "--try-models",
        type=bool,
        default=False,
        help="try load model and run inference for all models before running main",
    )
    parser.add_argument(
        "--pre-select-multiplier",
        type=int,
        default=1,
        help="Filter based on rows in DatasetDict before filtering based on num of seq",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="random seed to ensure reproducibility",
    )
    args = parser.parse_args()
    return args


class Timer:
    def __init__(self, what: str, total: int = None) -> None:
        self.what = what
        self.total = total

    def __enter__(self):
        self.start = datetime.now()
        logger.info(f"Starting {self.what}...")

    def __exit__(self, type, value, traceback):
        end = datetime.now()
        total_seconds = (end - self.start).total_seconds()
        logger.info(f"{self.what} took {total_seconds} seconds")
        if self.total:
            logger.info(
                f"{self.what} took {total_seconds / self.total} seconds per iteration"
            )


def log_few_samples(raw_datasets: DatasetDict, k: int = 1):
    for split, ds in raw_datasets.items():
        for index in random.sample(range(len(ds)), k):
            logger.debug(f"Sample {index} of the {split} set: {ds[index]}.")


def sample_datasets_subset(
    raw_datasets: DatasetDict, keep: Dict[str, int]
) -> DatasetDict:
    for split, max_samples in keep.items():
        if max_samples is not None and split in raw_datasets.keys():
            max_samples = min(len(raw_datasets[split]), max_samples)
            raw_datasets[split] = raw_datasets[split].select(range(max_samples))
    return raw_datasets


def gen_sequence(
    raw_datasets: DatasetDict, data_args: argparse.Namespace
) -> DatasetDict:
    """_summary_
    Reference
    https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_mlm.py#L450

    Args:
        raw_datasets (DatasetDict): _description_
        data_args (argparse.Namespace): _description_

    Returns:
        DatasetDict: _description_
    """

    tokenizer = AutoTokenizer.from_pretrained(data_args.tokenizer_name)

    column_names = raw_datasets["train"].column_names
    text_column_name = "text" if "text" in column_names else column_names[0]

    if data_args.max_seq_length is None:
        max_seq_length = tokenizer.model_max_length
        if max_seq_length > 1024:
            logger.warning(
                f"The tokenizer picked seems to have a very large `model_max_length` ({tokenizer.model_max_length}). "
                "Picking 1024 instead. You can change that default value by passing --max_seq_length xxx."
            )
            max_seq_length = 1024
    else:
        if data_args.max_seq_length > tokenizer.model_max_length:
            logger.warning(
                f"The max_seq_length passed ({data_args.max_seq_length}) is larger than the maximum length for the"
                f"model ({tokenizer.model_max_length}). Using max_seq_length={tokenizer.model_max_length}."
            )
        max_seq_length = min(data_args.max_seq_length, tokenizer.model_max_length)

    # Otherwise, we tokenize every text, then concatenate them together before splitting them in smaller parts.
    # We use `return_special_tokens_mask=True` because DataCollatorForLanguageModeling (see below) is more
    # efficient when it receives the `special_tokens_mask`.
    def tokenize_function(examples):
        return tokenizer(examples[text_column_name])

    tokenized_datasets = raw_datasets.map(
        tokenize_function,
        batched=True,
        num_proc=data_args.preprocessing_num_workers,
        remove_columns=column_names,
        load_from_cache_file=not data_args.overwrite_cache,
        desc="Running tokenizer on every text in dataset",
    )

    logger.info(f"after tokenization:\n{tokenized_datasets=}")
    log_few_samples(tokenized_datasets)

    filename = os.path.join(
        data_args.preprocess_dir,
        str(data_args.max_seq_length),
        data_args.tokenizer_name,
        "tokenized",
    )
    logger.info(f"save tokenized_datasets to {filename}")
    tokenized_datasets.save_to_disk(filename)

    # Main data processing function that will concatenate all texts from our dataset and generate chunks of
    # max_seq_length.
    def group_texts(examples):
        # Concatenate all texts.
        concatenated_examples = {k: list(chain(*examples[k])) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
        if total_length >= max_seq_length:
            total_length = (total_length // max_seq_length) * max_seq_length
        # Split by chunks of max_len.
        result = {
            k: [
                t[i : i + max_seq_length]
                for i in range(0, total_length, max_seq_length)
            ]
            for k, t in concatenated_examples.items()
        }
        return result

    # Note that with `batched=True`, this map processes 1,000 texts together, so group_texts throws away a
    # remainder for each of those groups of 1,000 texts. You can adjust that batch_size here but a higher value
    # might be slower to preprocess.
    #
    # To speed up this part, we use multiprocessing. See the documentation of the map method for more information:
    # https://huggingface.co/docs/datasets/package_reference/main_classes.html#datasets.Dataset.map

    grouped_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        num_proc=data_args.preprocessing_num_workers,
        load_from_cache_file=not data_args.overwrite_cache,
        desc=f"Grouping texts in chunks of {max_seq_length}",
    )

    logger.info(f"after grouping text:\n{grouped_datasets=}")
    log_few_samples(grouped_datasets)

    grouped_datasets = sample_datasets_subset(
        grouped_datasets,
        {
            "train": data_args.max_train_samples,
            "validation": data_args.max_val_samples,
            "test": data_args.max_test_samples,
        },
    )

    logger.info(f"after selecting subset\ngrouped_datasets: {grouped_datasets}")

    filename = os.path.join(
        data_args.preprocess_dir,
        str(data_args.max_seq_length),
        data_args.tokenizer_name,
        "grouped",
    )
    logger.info(f"save grouped_datasets to {filename}")
    grouped_datasets.save_to_disk(filename)

    # reconstruct original text
    # https://huggingface.co/docs/datasets/v2.5.2/en/package_reference/main_classes#datasets.Dataset.map
    # `function(batch: Dict[str, List]) -> Dict[str, List]` if `batched=True` and `with_indices=False`
    def get_sequence_text(examples: Dict[str, List]) -> Dict[str, List]:
        # https://huggingface.co/docs/transformers/main_classes/tokenizer
        # https://huggingface.co/docs/transformers/v4.22.2/en/main_classes/tokenizer#transformers.BatchEncoding
        # type(examples) = dict
        # examples.keys() = dict_keys(['input_ids', 'token_type_ids', 'attention_mask'])
        # examples['input_ids'] is tensor of size (batch_size, seq_length)
        return {
            "text": tokenizer.batch_decode(
                examples["input_ids"], skip_special_tokens=True
            )
        }

    column_names = tokenized_datasets["train"].column_names

    sequence_datasets = grouped_datasets.map(
        get_sequence_text,
        batched=True,
        num_proc=data_args.preprocessing_num_workers,
        remove_columns=column_names,
        load_from_cache_file=not data_args.overwrite_cache,
        desc="Get sequence text",
    )

    logger.info(f"after get_sequence_text():\n{sequence_datasets=}")
    log_few_samples(sequence_datasets)

    filename = os.path.join(
        data_args.preprocess_dir,
        str(data_args.max_seq_length),
        data_args.tokenizer_name,
        "sequence",
    )
    logger.info(f"save sequence_datasets to {filename}")
    sequence_datasets.save_to_disk(filename)

    return sequence_datasets


# https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens
# https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/models/Pooling.py#L84
# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(
    token_embeddings: torch.Tensor, attention_mask: torch.Tensor
) -> torch.Tensor:
    # (batch_size, seq_len, hidden_size)
    # (batch_size, hidden_size)
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.mean(token_embeddings * input_mask_expanded, dim=1)


def gen_embeddings(
    model_name_or_path: str, raw_datasets: DatasetDict, data_args: argparse.Namespace
) -> DatasetDict:
    """_summary_

    Reference
    https://github.com/huggingface/transformers/blob/main/examples/pytorch/text-classification/run_glue.py#L434

    Args:
        model_name_or_path (str): _description_
        raw_datasets (DatasetDict): _description_
        data_args (argparse.Namespace): _description_

    Returns:
        DatasetDict: _description_
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    model = AutoModel.from_pretrained(model_name_or_path)
    model.to(dev)
    model.eval()

    logger.info(f"{model.device=}")

    column_names = raw_datasets["train"].column_names
    text_column_name = "text" if "text" in column_names else column_names[0]

    if data_args.max_seq_length is None:
        max_seq_length = tokenizer.model_max_length
        if max_seq_length > 1024:
            logger.warning(
                f"The tokenizer picked seems to have a very large `model_max_length` ({tokenizer.model_max_length}). "
                "Picking 1024 instead. You can change that default value by passing --max_seq_length xxx."
            )
            max_seq_length = 1024
    else:
        if data_args.max_seq_length > tokenizer.model_max_length:
            logger.warning(
                f"The max_seq_length passed ({data_args.max_seq_length}) is larger than the maximum length for the"
                f"model ({tokenizer.model_max_length}). Using max_seq_length={tokenizer.model_max_length}."
            )
        max_seq_length = min(data_args.max_seq_length, tokenizer.model_max_length)

    # Tokenize all sequences
    def tokenize_function(examples):
        return tokenizer(
            examples[text_column_name],
            padding="max_length",
            max_length=max_seq_length,
            truncation=True,
        )

    tokenized_datasets = raw_datasets.map(
        tokenize_function,
        batched=True,
        num_proc=data_args.preprocessing_num_workers,
        remove_columns=column_names,
        load_from_cache_file=not data_args.overwrite_cache,
        desc=f"Running tokenizer on every text in dataset, {model_name_or_path}",
    )

    logger.info(f"after tokenization:\n{tokenized_datasets=}")
    log_few_samples(tokenized_datasets)
    filename = os.path.join(
        data_args.embedding_dir,
        str(data_args.max_seq_length),
        model_name_or_path,
        "tokenized",
    )
    logger.info(f"save tokenized_datasets to {filename}")
    tokenized_datasets.save_to_disk(filename)

    # https://huggingface.co/docs/datasets/use_with_pytorch
    logger.info("Set datasets format as torch Tensor")
    tokenized_datasets.set_format("torch")
    log_few_samples(tokenized_datasets)

    # compute embeddings
    # https://huggingface.co/docs/datasets/v2.5.2/en/package_reference/main_classes#datasets.Dataset.map
    # `function(batch: Dict[str, List]) -> Dict[str, List]` if `batched=True` and `with_indices=False`
    logger.info(f"{model.device=}")

    def get_sequence_embedding(examples: Dict[str, List]) -> Dict[str, List]:
        # https://huggingface.co/docs/transformers/main_classes/tokenizer
        # https://huggingface.co/docs/transformers/v4.22.2/en/main_classes/tokenizer#transformers.BatchEncoding
        # type(examples) = dict
        # examples.keys() = dict_keys(['input_ids', 'token_type_ids', 'attention_mask'])
        # examples['input_ids'] is tensor of size (batch_size, seq_length)
        examples = transformers.BatchEncoding(examples)
        examples.to(model.device)
        with torch.no_grad():
            outputs = model(**examples)
            sequence_embeddings = mean_pooling(
                outputs.last_hidden_state, examples["attention_mask"]
            )
            return {"embedding": sequence_embeddings.detach().cpu().numpy()}

    column_names = tokenized_datasets["train"].column_names

    # embeddings are CPU Tensor
    embedding_datasets = tokenized_datasets.map(
        get_sequence_embedding,
        batched=True,
        batch_size=data_args.batch_size,
        num_proc=data_args.preprocessing_num_workers,
        remove_columns=column_names,
        load_from_cache_file=not data_args.overwrite_cache,
        desc=f"Get sequence embeddings, {model_name_or_path}",
    )

    model = model.cpu()
    del model

    logger.info(f"after computing embedding:\n{embedding_datasets=}")
    log_few_samples(embedding_datasets)

    filename = os.path.join(
        data_args.embedding_dir,
        str(data_args.max_seq_length),
        model_name_or_path,
        "embeddings",
    )
    logger.info(f"save embedding_datasets to {filename}")
    embedding_datasets.save_to_disk(filename)

    return embedding_datasets


class LanguageModelDecomposition:
    """_summary_
    u = w_i * v_i + b
    W = [w_1, w_2, ..., w_k]
    z = concat(v_1, v_2, ..., v_k)
    L = E[(u - Wz - b)^T (u - Wz - b)]
    => W = cov(u, z) * cov(z, z^T) (-1)
    => b = E[u] - W * E[z]
    """

    def __init__(
        self,
        input: List[str],
        output: str,
        alpha: float,
    ) -> None:
        assert alpha >= 0
        self.input = input
        if isinstance(self.input, str):
            self.input = [self.input]
        self.output = output
        self.alpha = alpha
        self.W = None
        self.b = None

    def __repr__(self) -> str:
        return f"LanguageModelDecomposition(output={self.output}, input={self.input}, alpha={self.alpha})"

    def train(
        self,
        train_embeddings: Dict[str, torch.Tensor],
    ):
        # (hidden_size * num_inputs, batch_size)
        Z = torch.cat([train_embeddings[i] for i in self.input], dim=1).T

        # (hidden_size, batch_size)
        U = train_embeddings[self.output].T

        # input_size = hidden_size * num_inputs
        # output_size = hidden_size
        num_inputs = len(self.input)
        input_size = Z.shape[0]
        output_size = U.shape[0]
        assert input_size == num_inputs * output_size

        # batch_size
        assert Z.shape[1] == U.shape[1]

        logger.debug(f"{Z.shape=}")
        logger.debug(f"{Z.device=}")
        logger.debug(f"{U.shape=}")
        logger.debug(f"{U.device=}")

        # E[z * z^T]
        # (hidden_size * num_inputs, hidden_size * num_inputs)
        # A = torch.mm(Z, Z.T) / Z.shape[0]
        A = torch.cov(Z)
        assert torch.equal(A, A.T)
        assert A.shape == (input_size, input_size)
        logger.debug(f"{A.shape=}")

        # E[u * z^T]
        # (hidden_size, hidden_size * num_inputs)
        UZ = torch.cat((U, Z), dim=0)
        UZ_cov = torch.cov(UZ)
        assert torch.equal(UZ_cov, UZ_cov.T)

        # B = torch.mm(U, Z.T) / Z.shape[0]
        B = UZ_cov[:output_size, output_size:]
        assert B.shape == (output_size, input_size)
        logger.debug(f"{B.shape=}")

        # W = B * (A)^(-1)
        # W*A = B => A^T * W^T = B^T, A = A^T
        # (hidden_size, hidden_size * num_inputs)
        self.W = torch.linalg.solve(A + self.alpha * torch.eye(A.shape[0]), B.T).T
        assert self.W.shape == (output_size, input_size)

        logger.debug(f"{self.W.shape=}")
        logger.debug(f"{self.W.device=}")

        self.b = U.mean(dim=1) - torch.matmul(self.W, Z.mean(dim=1))
        assert self.b.shape == (output_size,)

        logger.debug(f"{self.b.shape=}")
        logger.debug(f"{self.b.device=}")

    def score(self, embeddings: Dict[str, torch.Tensor]) -> float:
        # (hidden_size * num_inputs, batch_size)
        Z = torch.cat([embeddings[i] for i in self.input], dim=1).T

        # (hidden_size, batch_size)
        U = embeddings[self.output].T

        # input_size = hidden_size * num_inputs
        # output_size = hidden_size
        input_size = Z.shape[0]
        output_size = U.shape[0]
        assert self.W.shape == (output_size, input_size)

        # batch_size
        assert Z.shape[1] == U.shape[1]

        logger.debug(f"{Z.shape=}")
        logger.debug(f"{Z.device=}")
        logger.debug(f"{U.shape=}")
        logger.debug(f"{U.device=}")

        # E.shape = (hidden_size, batch_size)
        E = U - torch.mm(self.W, Z) - self.b.unsqueeze(dim=1)
        assert E.shape == U.shape

        EU = U.mean(dim=1)
        SSR = torch.sum(E ** 2, dim=0).mean().item()
        SST = torch.sum((U - EU.unsqueeze(dim=1)) ** 2, dim=0).mean().item()

        assert SSR >= 0
        assert SST >= 0

        logger.debug(f"{SSR=}, {SST=}")
        return 1 - SSR / SST


def main():
    """Console script for lmd."""
    args = parse_args()

    if args.basis:
        args.basis = args.basis.split(",")
    else:
        args.basis = [model_name for model_name in MODELS if model_name != args.target]

    assert isinstance(args.basis, list)
    assert args.target not in args.basis

    # check there is enough train samples
    assert (
        args.max_train_samples > len(args.basis) * 768
    ), "No enough train samples, LMD solver is under constrained"

    print(f"Arguments:\n{json.dumps(vars(args), indent=4)}")

    logger.setLevel(args.log_level)

    # Set seed before initializing model.
    set_seed(args.seed)

    if args.try_models:
        logger.info(
            f"Try model inference with batch size: {args.batch_size}, max_seq_length: {args.max_seq_length}, {MODELS}"
        )
        for model_name in tqdm(
            MODELS,
            desc=f"Try model inference with batch size: {args.batch_size}, max_seq_length: {args.max_seq_length}",
        ):
            logger.info(f"load model: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            model.to(dev)
            model.eval()
            logger.info(f"{model.device=}")
            with Timer(f"model inference for {model_name}"):
                with torch.no_grad():
                    text = " ".join(["hello"] * args.max_seq_length)
                    texts = [text] * args.batch_size
                    encoded_input = tokenizer(
                        texts,
                        padding="max_length",
                        max_length=args.max_seq_length,
                        truncation=True,
                        return_tensors="pt",
                    )
                    encoded_input.to(model.device)
                    outputs = model(**encoded_input)
                    assert outputs.last_hidden_state.requires_grad == False
            model = model.cpu()
            del model

    # load dataset
    raw_datasets = load_dataset(args.dataset_name, args.dataset_config_name)
    logger.info(f"after loading datasets:\nraw_datasets:{raw_datasets}")

    # split validation if not exists
    # ref: https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_mlm.py#L289
    # https://huggingface.co/docs/datasets/v1.11.0/splits.html
    # https://huggingface.co/docs/datasets/loading#slice-splits
    if "validation" not in raw_datasets.keys():
        logger.warning(f"split validation and test from train")
        # train_test_datasets = raw_datasets["train"].train_test_split(test_size=args.test_split_percentage)
        # raw_datasets["test"] = train_test_datasets["test"]

        # train_val_datasets = train_test_datasets["train"].train_test_split(test_size=args.val_split_percentage/(1 - args.test_split_percentage))
        # raw_datasets["train"] = train_val_datasets["train"]
        # raw_datasets["validation"] = train_val_datasets["test"]

        raw_datasets["validation"] = load_dataset(
            args.dataset_name,
            args.dataset_config_name,
            split=f"train[:{args.val_split_percentage}%]",
        )
        raw_datasets["test"] = load_dataset(
            args.dataset_name,
            args.dataset_config_name,
            split=f"train[{args.val_split_percentage}%:{args.val_split_percentage + args.test_split_percentage}%]",
        )
        raw_datasets["train"] = load_dataset(
            args.dataset_name,
            args.dataset_config_name,
            split=f"train[{args.val_split_percentage + args.test_split_percentage}%:]",
        )
        logger.info(f"after splitting datasets:\nraw_datasets:{raw_datasets}")

    logger.info(f"Shuffle raw_datasets")
    raw_datasets = raw_datasets.shuffle(seed=args.seed)

    logger.info(
        f"pre-select subset to reduce preprocessing time (tokenization, grouping, gen_sequences)"
    )
    raw_datasets = sample_datasets_subset(
        raw_datasets,
        {
            "train": args.max_train_samples * args.pre_select_multiplier,
            "validation": args.max_val_samples * args.pre_select_multiplier,
            "test": args.max_test_samples * args.pre_select_multiplier,
        },
    )
    logger.info(f"after selecting subset\nraw_datasets: {raw_datasets}")

    log_few_samples(raw_datasets)

    # first use bert tokenizer to generate sequences (length = args.max_seq_length)
    sequence_datasets: DatasetDict = gen_sequence(raw_datasets, args)

    # then tokenize using model specific tokenizers
    # compute embedding
    all_models = [args.target] + args.basis

    embeddings_path = os.path.join(
        args.embedding_dir, str(args.max_seq_length), "embeddings.pt"
    )
    try:
        logger.info(f"Try to load embeddings from: {embeddings_path}")
        embeddings = torch.load(embeddings_path)
    except:
        logger.info(f"Failed: Try to load embeddings from: {embeddings_path}")
        logger.info(f"Regen embeddings:")
        embeddings = defaultdict(dict)
        for model_name in tqdm(all_models, desc="Regen embeddings"):
            logger.info(f"gen embeddings for {model_name=}")
            embedding_datasets: DatasetDict = gen_embeddings(
                model_name, sequence_datasets, args
            )
            for split, ds in embedding_datasets.items():
                embeddings[split][model_name] = ds["embedding"]
        logger.info(f"Save embeddings to: {embeddings_path}")
        torch.save(embeddings, embeddings_path)

    logger.info(f"Run LMD for group score")
    group_score = pd.DataFrame(
        index=["train", "validation", "test"], columns=all_models
    )
    group_model_dir = os.path.join(args.models_dir, str(args.max_seq_length), "group")
    os.makedirs(group_model_dir, exist_ok=True)
    for output in tqdm(all_models, desc="Run LMD for group score"):
        input = set(all_models) - set([output])
        input = list(input)
        lmd = LanguageModelDecomposition(input, output, alpha=args.alpha)

        logger.info(f"Run {str(lmd)}")
        lmd.train(embeddings["train"])

        filename = os.path.join(group_model_dir, f"{'%'.join(output.split('/'))}.lmd")
        logger.info(f"save group model {str(lmd)} to {filename}")
        torch.save(lmd, filename)

        for split in ["train", "validation", "test"]:
            R2 = lmd.score(embeddings[split])
            logger.info(f"{str(lmd)}, {split=}, {R2=}")
            group_score.loc[split, output] = R2

    results_dir = os.path.join(args.results_dir, str(args.max_seq_length))
    os.makedirs(results_dir, exist_ok=True)

    logger.info(f"group_score={group_score}")
    filename = os.path.join(results_dir, "group_score.csv")
    logger.info(f"save group_score to: {filename}")
    group_score.to_csv(filename)

    # pairwise
    logger.info(f"Run LMD for pairwise score")
    pairwise_score = dict()

    for split in ["train", "validation", "test"]:
        pairwise_score[split] = pd.DataFrame(columns=all_models, index=all_models)

    pairwise_model_dir = os.path.join(
        args.models_dir, str(args.max_seq_length), "pairwise"
    )
    os.makedirs(pairwise_model_dir, exist_ok=True)
    all_pairs = list(itertools.permutations(all_models, 2))
    for input, output in tqdm(all_pairs, desc="Run LMD for pairwise score"):
        logger.info(f"{input=}, {output=}")
        lmd = LanguageModelDecomposition(input, output, alpha=args.alpha)

        lmd.train(embeddings["train"])

        filename = os.path.join(
            pairwise_model_dir,
            f"output_{'%'.join(output.split('/'))}_input_{'%'.join(input.split('/'))}.lmd",
        )

        logger.info(f"save pairwise model {str(lmd)} to {filename}")

        torch.save(lmd, filename)

        for split in ["train", "validation", "test"]:
            R2 = lmd.score(embeddings[split])
            logger.info(f"{input=}, {output=}, {split=}, {R2=}")
            pairwise_score[split].loc[input, output] = R2

    for split in ["train", "validation", "test"]:
        logger.info(f"{split=}, {pairwise_score[split]=}")
        filename = os.path.join(results_dir, f"pairwise_score_{split}.csv")
        logger.info(f"save pairwise_score to: {filename}")
        pairwise_score[split].to_csv(filename)

    # lmd_from_file = torch.load("lmd.model")
    # logger.info(f"{type(lmd_from_file)=}")

    # logger.info(f"{lmd_from_file.score(embeddings['train'])=}")

    # logger.info(f"{lmd_from_file.score(embeddings['validation'])=}")

    # logger.info(f"{lmd_from_file.score(embeddings['test'])=}")

    # assert torch.equal(lmd.W, lmd_from_file.W)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
