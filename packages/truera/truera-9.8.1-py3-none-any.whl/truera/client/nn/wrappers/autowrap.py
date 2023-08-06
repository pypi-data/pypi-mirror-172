from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Union

from truera.client.cli.verify_nn_ingestion.nlp import NLPAutowrapVerifyHelper
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers as NLP


def autowrap(
    *,
    # general args
    n_tokens: int,
    n_embeddings: int,
    # split load wrapper args
    ds_from_source: Callable,
    # load wrapper args
    get_model: Callable,
    # run wrapper args
    databatch_to_trubatch: Callable,
    # tokenizer args
    vocab: Dict[str, int],
    unk_token_id: int,
    pad_token_id: int,
    special_tokens: List[int],
    text_to_inputs: Callable,
    text_to_token_ids: Callable,
    # Optional args
    eval_model: Optional[Callable] = None,
    text_to_spans: Optional[Callable] = None,
    model_path: Optional[Union[str, Path]] = None,
    data_path: Optional[Union[str, Path]] = None
) -> nlp.WrapperCollection:
    """
    Given a number of parameters, automatically create and 
    return a SplitLoadWrapper, ModelLoadWrapper, ModelRunWrapper,
    and TokenizerWrapper, bundled as a WrapperCollection.

    Args:
        n_tokens (int): The sequence size of the model
        n_embeddings (int): The dimensionality of the model's embeddings
        ds_from_source (Callable): Function that loads a dataset into memory from a path
        get_model (Callable): Function that loads model into memory from a path
        databatch_to_trubatch (Callable): Function extracting raw text, labels, and ids from the loaded dataset 
        vocab (Dict[str, int]): Dictionary mapping tokens to their respective IDs
        unk_token_id (int): The token ID of the UNK token
        pad_token_id (int): The token ID of the PAD token
        special_tokens (List[int]): A list of special tokens (i.e CLS, MASK, SEP, PAD) 
        text_to_inputs (Callable): Function given text and returns args and kwargs to pass to `eval_model`
        text_to_token_ids (Callable): Function tokenizing raw text into token IDs
        eval_model (Callable): Function evaluating the model on args and kwargs from `text_to_inputs`. If None, will use model return value
        text_to_spans (Optional[Callable], optional): Function converting raw text into spans. 
            Spans mark the start and end index of each token in the original text.
            If None, token-level influences are still available, but word-level influences will be disabled. Defaults to None.
        model_path (Optional[Union[str, Path]], optional): Path to your model checkpoint. 
            If None, `get_model` is assumed to return a model in memory. Defaults to None.
        data_path (Optional[Union[str, Path]], optional): Path to your dataset. 
            If None, `ds_from_source` is assumed to return a dataset in memory. Defaults to None.

    Returns:
        nlp.WrapperCollection: A container class containing TruEra wrappers
    """
    verify_helper = NLPAutowrapVerifyHelper()
    verify_helper.verify_flow(
        n_tokens=n_tokens,
        ds_from_source=ds_from_source,
        get_model=get_model,
        databatch_to_trubatch=databatch_to_trubatch,
        unk_token_id=unk_token_id,
        pad_token_id=pad_token_id,
        special_tokens=special_tokens,
        text_to_inputs=text_to_inputs,
        text_to_token_ids=text_to_token_ids,
        eval_model=eval_model,
        text_to_spans=text_to_spans,
        model_path=model_path,
        data_path=data_path
    )

    class SplitLoadWrapper(NLP.SplitLoadWrapper):

        def get_ds(self) -> Iterable:
            return ds_from_source(self.get_data_path())

    class ModelLoadWrapper(NLP.ModelLoadWrapper):

        def get_tokenizer(self, n_tokens: int) -> NLP.TokenizerWrapper:
            return TokenizerWrapper(
                model_path=self.model_path,
                vocab=vocab,
                n_tokens=n_tokens,
                unk_token_id=unk_token_id,
                pad_token_id=pad_token_id,
                special_tokens=special_tokens
            )

        def get_model(self) -> Callable:
            return get_model(self.model_path)

    class ModelRunWrapper(NLP.ModelRunWrapper):

        @staticmethod
        def trubatch_of_databatch(
            ds_batch: Types.DataBatch, model: Callable
        ) -> NLP.Types.TruBatch:
            tru_batch = databatch_to_trubatch(ds_batch)
            return NLP.Types.TruBatch(**tru_batch)

        @staticmethod
        def evaluate_model(
            model: Callable, inputs: NLP.Types.InputBatch
        ) -> NLP.Types.OutputBatch:
            if eval_model:
                out = eval_model(model, inputs.args, inputs.kwargs)
            else:
                out = model(*inputs.args, **inputs.kwargs)
            return NLP.Types.OutputBatch(probits=out)

    class TokenizerWrapper(NLP.TokenizerWrapper):

        def __init__(
            self,
            model_path: Union[str, Path],
            vocab: Dict[Types.Token, Types.TokenId],
            n_tokens: int,
            unk_token_id: int,
            pad_token_id: int,
            special_tokens: Optional[List[Types.TokenId]] = None
        ):
            super().__init__(
                model_path=model_path,
                vocab=vocab,
                n_tokens=n_tokens,
                unk_token_id=unk_token_id,
                pad_token_id=pad_token_id,
                special_tokens=special_tokens
            )

            self.text_to_inputs = text_to_inputs
            self.text_to_token_ids = text_to_token_ids
            self.text_to_spans = text_to_spans

        def inputbatch_of_textbatch(
            self, texts: Iterable[str]
        ) -> NLP.Types.InputBatch:
            inputs = self.text_to_inputs(texts)
            return NLP.Types.InputBatch(
                args=inputs['args'], kwargs=inputs['kwargs']
            )

        def tokenize_into_tru_tokens(
            self, texts
        ) -> NLP.Types.TruTokenization[NLP.Types.Token]:
            tokenss = self.text_to_token_ids(texts)
            if not callable(self.text_to_spans):
                spans = None
            else:
                offsetss = self.text_to_spans(texts)
                spans = [
                    [
                        NLP.Types.Span(
                            item=self.vocab_inverse[t], begin=o[0], end=o[1]
                        ) for t, o in zip(tokens, offsets)
                    ] for tokens, offsets in zip(tokenss, offsetss)
                ]
            return NLP.Types.TruTokenization(token_ids=tokenss, spans=spans)

    split_load_wrapper = SplitLoadWrapper(data_path=data_path)
    load_wrapper = ModelLoadWrapper(model_path=model_path)
    run_wrapper = ModelRunWrapper(n_tokens=n_tokens, n_embeddings=n_embeddings)
    tokenizer_wrapper = TokenizerWrapper(
        model_path=model_path,
        vocab=vocab,
        n_tokens=n_tokens,
        unk_token_id=unk_token_id,
        pad_token_id=pad_token_id,
        special_tokens=special_tokens
    )

    return nlp.WrapperCollection(
        split_load_wrapper, load_wrapper, run_wrapper, tokenizer_wrapper
    )
