"""
Defines wrappers to help get information from a customer's code development to
Truera's system. Since NN development environments are so varied, we need to do
this to convert to some standards that Truera can guarantee. Wrappers are
designed with 2 paradigms. 

1) Loading into memory '[X]LoadWrappers' - The most common things that we need
   loaded into memory for NN is the model and the dataset. This can be expanded
   to domain specifics. In local compute mode: we don't need the model load
   since it is already loaded. SplitLoadWrappers are still used because most NN
   datasets are backed by file storage.

  - ModelLoadWrapper - includes model and tokenizer loading

  - SplitLoadWrapper - data loading

   The pathways datasets take in the demo are as follows: 
   
   a. Path -- SplitLoadWrapper.__init__ receives data_path from where it will
      load things.

   b. Iterable[DataBatch] -- Users implement SplitLoadWrapper.get_ds which
      produces an iterable over data batches.

   c. (for model execution) Iterable[Inputs], Dict[str, Inputs] -- Users
      implement ModelRunWrapper.model_input_args_kwargs which takes in a
      DataBatch and produces arguments to send to a model.

   e. (for ui/display purposes) TruBatch -- Users implement
      ModelRunWrapper.ds_elements_to_truera_elements that converts DataBatch to
      TruBatch.

 2) Running the model and capturing important artifacts '[X]ModelRunWrappers' -
    These wrappers have methods defined that take the in-memory objects from the
    load wrappers (model and dataset), to transform into Truera system needs.
    The models are expected to be callable, and the datasets are expected to be
    iterable, with batched inputs alongside other arbitrary inputs.

  - ModelRunWrapper

Base wrappers should not depend on neural network backend (pytorch or
tensorflow). There are two classes here that are specific to each of these
backends and further refine the base classes with backend-specific requirements.

# Design Notes 

Run wrappers contain only static methods. We did not want to impose requirements
that users store relevant data in wrappers. As a result of this, the wrapper
contain static methods that accept arbitrary inputs named "model" and/or
"tokenizer" which are the users' existing structures. We do not impose
requirements on these structures so the users can use whatever they already have
with zero changes to these hopefully. However, we require that in wrappers, the
users write methods for loading and saving models and tokenizers. The load
wrappers are not static; the SplitLoadWrapper is especially non-static as
different instantiations with different data paths are made during artifact
generation.

* TokenizerWrapper is presently an exception to the "static
wrappers" only rule. 

# "Initialize-time" checking 

The wrappers here make heavy use of abstract methods which have the benefit of
throwing errors during class initialization if a required method is not provided
by the user. Some wrappers come with "optional" methods for some analyses. These
are put into sub-classes with (required) abstract methods. A user wishing to
perform those analyses needs to extend/mixin those classes to indicate so. The
abstract method system will then require they implement the required methods.
These are: 

- Base.ModelRunWrapper.WithBinaryClassifier

- Timeseries.ModelRunWrapper.WithOneHot

- NLP.ModelRunWrapper.WithEmbeddings

- NLP.SplitLoadWrapper.WithSegmentByWord

See their docstrings for info about their means.

TODO: In the future we might redesign the wrapper/input structure so as to
require users store anything they need (model, tokenizer) in the wrapping class
itself which could then be provided as self to all of the presently static
methods that they need to implement.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
import logging
from math import ceil
from pathlib import Path
from typing import (
    Any, Callable, Dict, Iterable, List, Optional, TypeVar, Union
)

import numpy as np
import numpy.typing as npt

from truera.client.nn import Batch
from truera.client.nn import NNBackend as NNB
from truera.client.util.func_utils import Deprecate
from truera.client.util.func_utils import doc_prepend
from truera.client.util.func_utils import import_optional
from truera.client.util.func_utils import WrapperMeta
from truera.client.util.iter_utils import LenIterable
from truera.client.util.iter_utils import tqdm_or_not

logger = logging.getLogger(__name__)

MODEL_RUN_WRAPPER_SAVE_NAME = 'truera_model_run_wrapper.pickle'
MODEL_LOAD_WRAPPER_SAVE_NAME = 'truera_model_load_wrapper.pickle'
SPLIT_LOAD_WRAPPER_SAVE_NAME = 'truera_split_load_wrapper.pickle'

# For generics and type hints.
T = TypeVar("T")


class Wrapping:
    # TODO: When decorating a method, include into its docstring what its type aliases alias to.

    @staticmethod
    def deprecates(oldfunc_name: str, dep_version: str, remove_version: str):
        # TODO: docstrings
        return WrapperMeta.deprecates(
            oldfunc_name=oldfunc_name,
            dep_version=dep_version,
            remove_version=remove_version
        )

    @staticmethod
    def require_init(func):
        doc_prepend(
            func,
            "REQUIRED: Extending classes need to define an __init__ method and call this parent initializer."
        )

        return WrapperMeta.require(func)

    @staticmethod
    def require_init_if_extended(func):
        doc_prepend(
            func,
            "OPTIONAL: If extending classes define an __init__ method, they need to call this parent initializer."
        )

        return WrapperMeta.require_if_extended(func)

    @staticmethod
    def required(func):
        """
        Decorator for required methods in wrappers.
        """

        doc_prepend(func, "REQUIRED")

        return func

    @staticmethod
    def optional(func):
        """
        Decorator for optional methods in wrappers.
        """

        doc_prepend(func, "OPTIONAL")

        return func

    @staticmethod
    def utility(obj):
        """
        Decorator for utility methods which should not be overriden in wrappers.
        """

        doc_prepend(
            obj,
            "UTILITY: This method is defined for you and can be used in your wrappers."
        )

        # Mark object protected.
        return WrapperMeta.protect(obj)

    @staticmethod
    def protected(obj):
        """
        Decorator for methods which should not be overriden in wrappers.
        """

        # Mark object protected.
        return WrapperMeta.protect(obj)


# Organizing base types into a separate class. This could be inside NLP but
# would need a lot of verbosity to refer to the various defined types to define
# the others.
class Types:
    """
    Types covering all NN model wrappers.
    """

    class DataBatch(Batch):
        """
        Client-specific, framework-specific data batch. Need to be able to
        produce InputBatch and TruBatch from this. One iteration from
        iter(get_ds()). 

        Extend this class and decorate with @dataclass, for example:
        
        ```
        @dataclass
        class TruHugsDataBatch(Types.DataBatch):
            text: np.ndarray = Batch.field(factory=np.array)
            label: np.ndarray = Batch.field(factory=np.array)
            index: np.ndarray = Batch.field(factory=np.array) 
        ```
        Notice that all fields must be produced by Batch.field and given the
        appropriate factory. Other common factories are described in Batch
        docstring.
        """
        pass

    @dataclass
    class InputBatch:  # TODO: use a generic Batch class
        """
        Model input batches ready to be sent to a model. The contents must be
        organized as a list of positional arguments and a dictionary of keyword
        arguments. The contents are project and framework specific.
        """

        args: List[NNB.Inputs]
        kwargs: Dict[str, NNB.Inputs]

        def __len__(self):
            from trulens.nn.backend import get_backend
            from trulens.utils.typing import TensorAKs
            tl_model_inputs = TensorAKs(args=self.args, kwargs=self.kwargs)
            return len(tl_model_inputs.first_batchable(get_backend()))

        def unit(self):
            return f"{self.__class__.__name__} of {len(self)} instances"

        def for_batch(
            self,
            func: Callable[[Types.InputBatch], None],
            batch_size: int,
            tqdm_options: Dict[str, Any] = None
        ) -> None:
            """
            Calls the given function with stored args but rebatched into the given
            batch_size. Ignores the result so should only be used with effectful
            functions. Rest of args are sent to tqdm when iterating.
            """

            assert len(self) > 0, "cannot call `func` on empty InputBatch"

            if tqdm_options is not None:
                tqdm_options['unit'] = self.unit()

            for batch in tqdm_or_not(tqdm_options)(
                self.rebatch(batch_size=batch_size)
            ):
                func(batch)

        def map_batch(
            self,
            func: Callable[[Types.InputBatch], T],
            batch_size: int,
            tqdm_options: Dict[str, Any] = None
        ) -> T:
            """
            Call the given function with stored args but rebatched into the
            given batch_size, outputs are collected and stacked. Looping is done
            with tqdm if `tqdm_args` is not None. Value is sent as kwargs to
            tqdm if so.
            """

            assert len(self) > 0, "cannot call `func` on empty InputBatch"

            outputs = []

            if tqdm_options is not None:
                tqdm_options['unit'] = self.unit()

            for batch in tqdm_or_not(tqdm_options)(
                self.rebatch(batch_size=batch_size)
            ):
                outputs.append(func(batch))

            # move this to some utility or backend module
            #if isinstance(outputs[0], torch.Tensor):
            #    return torch.cat(outputs, axis=0)
            if isinstance(outputs[0], np.ndarray):
                return np.concatenate(outputs, axis=0)
            elif isinstance(outputs[0], Batch):
                return Batch.collate(outputs)
            else:
                raise RuntimeError(
                    f"do not know how to stack items of type {type(outputs[0])}"
                )

        def rebatch(self, batch_size: int) -> LenIterable[Types.InputBatch]:
            """
            Batch this batch into (smaller) batches.
            """
            from trulens.nn.backend import get_backend
            from trulens.utils.typing import TensorAKs
            tl_model_inputs = TensorAKs(args=self.args, kwargs=self.kwargs)
            args_first = tl_model_inputs.first_batchable(get_backend())
            original_batch_size = len(
                args_first
            )  # assume first dim is batch_size

            # TODO DIM_ORDER

            def generator():

                def slice_fn(sliceable, start, offset):
                    return sliceable[start:start + offset]

                from functools import partial

                from trulens.utils.typing import nested_map
                for i in range(0, original_batch_size, batch_size):
                    slice_fn_with_range = partial(
                        slice_fn, start=i, offset=batch_size
                    )
                    args = nested_map(self.args, slice_fn_with_range)
                    kwargs = nested_map(self.kwargs, slice_fn_with_range)
                    yield Types.InputBatch(args=args, kwargs=kwargs)

            return LenIterable(
                generator(),
                len=ceil(len(self) / batch_size),
                batch_size=batch_size
            )

    @dataclass
    class OutputBatch(DataBatch):
        """
        Model output batches in numpy format. Only classification outputs of probit
        vectors are supported presently.
        """
        probits: np.ndarray = Batch.field(factory=np.array)

    @dataclass
    class TruBatch(Batch):
        """
        Instance information required for Truera. Currently only supervised models
        with labels are supported.
        """

        ids: npt.NDArray[np.long] = Batch.field(np.array)
        labels: npt.NDArray[int] = Batch.field(np.array)

        @property
        def batch_size(self) -> int:
            return len(self.ids)


class Wrappers:  # WANT: Generic in an implementation of NNBackend
    """
    Base requirements over all nn model / data types. Each project must provide
    the following wrappers:
    
    - `SplitLoadWrapper` - responsible for loading data splits `get_ds`,
        producing an iteration over `DataBatch` which itself is
        project-specific. The value `DataBatch` defined here is merely a type
        variable used to annotate methods with type hints.

    - `ModelLoadWrapper` - loads a model, producing `model`. This is, again,
        a project-specific type defined as a type variable here.

    - `ModelRunWrapper` - the meat of the wrappers:

        - inputbatch_of_databatch - transforms `DataBatch` into `InputBatch`.
        `InputBatch` specifies the positional and keyword arguments with which a
        model is evaluated. The values of these arguments are
        project/framework-specific tensors.

        - evaluate_model - evaluates a model on a given `InputBatch`,
        producing `OutputBatch`. This is a framework-specific tensor whose first
        dimension is the batch index. Additional requirements on this tensor are
        specified under `Timeseries` and `NLP` wrapper variants.
        
        - trubatch_of_databatch - transforms `DataBatch` into
        `TruBatch`, which is a collection of tensors required for operation of
        the Truera product. Each type of model imposes different requirements of
        what a `TruBatch` must contain.
    """

    # Adding this pointer so that help(Wrappers) will include a mention of it.
    Types = Types

    class ModelRunWrapper(metaclass=WrapperMeta):
        """
        A wrapper to run nn models. The base class contains methods that will be
        needed for nn models of any type.
        
        * Static methods only. *
        """

        @Wrapping.deprecates(
            "ds_elements_to_truera_elements",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @Wrapping.required
        @staticmethod
        @abstractmethod
        def trubatch_of_databatch(
            ds_batch: Types.DataBatch, *, model: NNB.Model
        ) -> Types.TruBatch:
            """
            This method should convert what comes out of a dataset into DataBatch with the appropriate properties
            
            Input
            ----------------
            - ds_batch: the output of a single iteration over the
              DataLoadWrapper.get_ds object
            - model: client's model
            ----------------
            Output
            ----------------
            - TruBatch with indexes, labels, and other data
            ----------------
            """
            ...

        @Wrapping.deprecates(
            "model_input_args_kwargs",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        @Wrapping.required
        @staticmethod
        @abstractmethod
        def inputbatch_of_databatch(
            databatch: Types.DataBatch, model: NNB.Model
        ) -> Types.InputBatch:
            """
            This method should convert what comes out of a dataset into model
            args and kwargs
            
            Input
            ----------------
            - ds_batch: the output of a single iteration over the
              DataLoadWrapper.get_ds object
            - model: client's model
            ----------------
            Output
            ----------------
            - InputBatch of args and kwargs to run the ModelLoadWrapper.get_model object
            ----------------
            """
            ...

        @staticmethod
        @abstractmethod
        @Wrapping.required
        def evaluate_model(
            model: NNB.Model, inputs: Types.InputBatch
        ) -> Types.OutputBatch:
            """
            This method return a batched evaluation of the model.
            Input
            ----------------
            - model: NNB.Model -- framework-specific, project-specific model.
            - batch: Types.InputBatch -- containing args and kwargs
            ----------------
            Output
            ----------------
            - Types.OutputBatch -- a batched evaluation of the model.
            ----------------
            """
            ...

        class WithBinaryClassifier(ABC):
            """
            Models that can be converted to a binary classifier. This is
            required for certain error analyses.
            """

            # TODO: verify type hints
            @staticmethod
            @abstractmethod
            def convert_model_eval_to_binary_classifier(
                ds_batch: Types.DataBatch,
                model_eval_output_or_labels: NNB.Outputs,
                labels: bool = False
            ) -> NNB.Outputs:
                """
                [Optional] Only used if post_model_filter_splits is used. See
                README on run_configuration.yml This method returns batched
                binary evaluations to help determine model performance. The
                value should be between 0 and 1, with 1 indicating a 'truth'
                value. This method is used to create post_model_filters This
                method already contains the model_eval_output_or_labels to save
                compute time If labels=True, the explainer will send the labels
                from ds_elements_to_truera_elements['labels'] into
                model_eval_output_or_labels
                
                Input
                ----------------
                - ds_batch: contains a batch of data from the dataset. This is
                  an iteration of SplitLoadWrapper.get_ds .
                - model_eval_output: the output of ModelWrapper.evaluate_model
                  this is precomputed to save time.
                - labels: boolean indicating whether model output is being
                  converted to binary preds, or if labels are being passed in
                ----------------
                Output
                ----------------
                - predictions - batched binary predictions or labels - batched
                  binary labels
                ----------------
                """
                ...

    class WithModelLoadWrapperUtility():

        @Deprecate.method(
            message="Use the model_path property instead.",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        def get_model_path(self) -> Path:
            return self.model_path

        @Wrapping.utility
        @property
        def model_path(self) -> Path:
            """
            The path where the model is expected to be stored.
            """

            return self._model_path  # pylint: disable=E1101

    class ModelLoadWrapper(WithModelLoadWrapperUtility, metaclass=WrapperMeta):
        """
        A wrapper to load nn models. The base class contains methods that will
        be needed for nn models of any type.
        """

        @Wrapping.require_init_if_extended
        def __init__(self, model_path: Optional[Union[Path, str]] = None):
            """
            Load wrappers are constructed in context of a path where models
            are expected to be stored.
            """

            self._model_path = model_path

        @Wrapping.required
        @abstractmethod
        def get_model(self) -> NNB.Model:
            """
            This method should return the framework-specific project-specific
            model object.
            """
            ...

    class WithSplitLoadWrapperUtility():

        @Deprecate.method(
            message="Use the data_path property instead.",
            dep_version="0.0.1",
            remove_version="0.1.0"
        )
        def get_data_path(self) -> Path:
            return self.data_path

        @Wrapping.utility
        @property
        def data_path(self) -> Path:
            """
            The path where the splits are loaded from.
            """

            return self._data_path  # pylint: disable=E1101

    class SplitLoadWrapper(WithSplitLoadWrapperUtility, metaclass=WrapperMeta):
        """
        A wrapper to load nn splits. The base class contains methods that will
        be needed for nn models of any type.
        """

        @Wrapping.require_init_if_extended
        def __init__(self, data_path: Optional[Union[Path, str]] = None):
            self._data_path = data_path

        @Wrapping.required
        @abstractmethod
        def get_ds(self) -> Iterable:
            # TODO: DataReaders in RNN do not implement any abstract class
            # presently. What they need to implement is unclear. Fix.
            """
            Load or construct a dataset object.
            ----------------
            Output
            ----------------
            - Collection of DataBatch in some iterable container.
            ----------------
            """
            ...


@dataclass
class WrapperCollection:  # for lack of a better name
    split_load_wrapper: Wrappers.SplitLoadWrapper
    model_load_wrapper: Wrappers.ModelLoadWrapper
    model_run_wrapper: Wrappers.ModelRunWrapper
