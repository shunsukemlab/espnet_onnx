from typing import Union, Dic
import numpy as np


class Hypothesis(NamedTuple):
    """Hypothesis data type."""

    yseq: np.ndarray
    score: Union[float, np.ndarray] = 0
    scores: Dict[str, Union[float, np.ndarray]] = dict()
    states: Dict[str, Any] = dict()

    def asdict(self) -> dict:
        """Convert data to JSON-friendly dict."""
        return self._replace(
            yseq=self.yseq.tolist(),
            score=float(self.score),
            scores={k: float(v) for k, v in self.scores.items()},
        )._asdict()


class BatchHypothesis(NamedTuple):
    """Batchfied/Vectorized hypothesis data type."""

    yseq: np.ndarray = np.ndarray([])  # (batch, maxlen)
    score: np.ndarray = np.ndarray([])  # (batch,)
    length: np.ndarray = np.ndarray([])  # (batch,)
    scores: Dict[str, np.ndarray] = dict()  # values: (batch,)
    states: Dict[str, Dict] = dict()

    def __len__(self) -> int:
        """Return a batch size."""
        return len(self.length)


class TransducerHypothesis(NamedTuple):
    """Default hypothesis definition for Transducer search algorithms."""

    score: float
    yseq: List[int]
    dec_state: Union[
        Tuple[torch.Tensor, Optional[torch.Tensor]],
        List[Optional[torch.Tensor]],
        torch.Tensor,
    ]
    lm_state: Union[Dict[str, Any], List[Any]] = None


class ExtendedHypothesis(TransducerHypothesis):
    """Extended hypothesis definition for NSC beam search and mAES."""

    dec_out: List[torch.Tensor] = None
    lm_scores: torch.Tensor = None










