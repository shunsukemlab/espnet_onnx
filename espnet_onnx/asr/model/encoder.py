

import onnxruntime
import numpy as np

from espnet_onnx.asr import Frontend
from espnet_onnx.asr import GlobalMVN
from espnet_onnx.asr import BatchScorerInterface
from .stft import

from espnet_onnx.utils import subsequent_mask, make_pad_mask


class Encoder:
    def __init__(
        self,
        encoder_config
    ):
        self.config = encoder_config
        self.encoder = onnxruntime.InferenceSession(
            self.config.model_path)

        self.frontend = Frontend(self.config.frontend)
        if self.config.do_normalize:
            self.normalize = GlobalMVN(self.config.gmvn)

        if self.config.do_preencoder:
            self.preencoder = Preencoder(self.config.preencoder)

        if self.config.do_postencoder:
            self.postencoder = Postencoder(self.config.postencoder)

    def __call__(
        self, speech: np.ndarray, speech_length: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Frontend + Encoder. Note that this method is used by asr_inference.py
        Args:
            speech: (Batch, Length, ...)
            speech_lengths: (Batch, )
        """
        # 1. Extract feature
        feats, feat_length = self.frontend(speech, speech_length)

        # 2. normalize with global MVN
        if self.config.do_normalize:
            feats, feat_length = self.normalize(feats, feat_length)

        mask = ~make_pad_mask(feat_length)[:, None, :]

        if self.config.do_preencoder:
            feats, feats_lengths = self.preencoder(feats, feats_lengths)

        # 3. forward encoder
        encoder_out, encoder_out_lens = \
            self.encoder.run(["encoder_out", "encoder_out_lens"], {
                "feats": feats,
                "mask": mask
            })

        if self.config.do_postencoder:
            encoder_out, encoder_out_lens = self.postencoder(
                encoder_out, encoder_out_lens
            )

        return encoder_out, encoder_out_lens