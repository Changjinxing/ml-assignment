# coding: utf-8
import logging
import time
import torch

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class Translator:
    def __init__(self, model_path: str = 'facebook/m2m100_418M', src_lang: str = "en", tgt_lang: str = "ja", verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.model = None
        self.tokenizer = None
        self.forced_bos_token_id = None
        self.device = 'cpu'

        self.model_path = model_path
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.verbose = verbose

    def load_model(self):
        _load_start = time.time()

        num_gpus = torch.cuda.device_count()
        if num_gpus == 0:
            self.logger.warning("No GPU found. Using CPU.")
        else:
            self.logger.info(f"Number of GPUs found: {num_gpus}")
            self.device = 'cuda'

        self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_path)
        self.model.to(self.device)

        self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_path, src_lang=self.src_lang, tgt_lang=self.tgt_lang)
        self.forced_bos_token_id = self.tokenizer.get_lang_id(self.tgt_lang)

        _load_end = time.time()
        if self.verbose:
            print(f"Model loaded in {_load_end - _load_start:.2f} seconds.")
        self.logger.info(f"Model loaded in {_load_end - _load_start:.2f} seconds.")

    def translate(self, input_text: str, src_lang: str = None, tgt_lang: str = None,
                  return_tensors: str = "pt", skip_special_tokens: bool = True):
        translated_texts = self.batch([input_text], src_lang, tgt_lang, return_tensors, skip_special_tokens)
        return translated_texts[0]

    def batch(self, input_texts: list[str], src_lang: str = None, tgt_lang: str = None,
              return_tensors: str = "pt", skip_special_tokens: bool = True,
              padding: bool = True, truncation: bool = True, max_length: int = 512):
        _start = time.time()

        if src_lang:
            self.tokenizer.src_lang = src_lang
        if tgt_lang:
            self.forced_bos_token_id = self.tokenizer.get_lang_id(tgt_lang)

        # Prepare inputs for the model
        inputs = self.tokenizer(input_texts, return_tensors=return_tensors,
                                padding=padding, truncation=truncation, max_length=max_length)

        # Translate batch of inputs
        with torch.no_grad():
            outputs = self.model.generate(**inputs, forced_bos_token_id=self.forced_bos_token_id)

        # Decode generated tokens to texts
        translated_texts = self.tokenizer.batch_decode(outputs, skip_special_tokens=skip_special_tokens)

        _end = time.time()
        if self.verbose:
            print(f"Translation done in {_end - _start:.2f} seconds.")
        self.logger.info(f"Translation done in {_end - _start:.2f} seconds.")
        return translated_texts


if __name__ == "__main__":
    _translator = Translator(verbose=False)
    _translator.load_model()

    src_texts = [
        "It's never too late to mend.",
        "Keep good men company and you shall be of the number.",
        "A good book is a good friend.",
        "Nothing is impossible for a willing heart",
        "One today is worth two tomorrows.",
        "Poverty is stranger to industry.",
        "A bird in the hand is worth than two in the bush.",
        "Four short words sum up what has lifted most successful individuals above the crowd: a little bit more.",
        "It is never too old to learn.",
        "From small beginning come great things.",
        "Genius is nothing but labor and diligence.",
        "A good beginning is half done.",
        "New wine in old bottles.",
        "All work and no play makes Jack a dull boy.",
        "Hope for the best, but prepare for the worst.",
        "Good health is over wealth.",
        "A fall into a pit, a gain in your wit.",
        "Better late than never.",
        "A friend in need is a friend indeed.",
        "Birds of a feather flock together.",
        "Complacency is the enemy of study.",
        "Content is better than riches.",
        "Books and friends should be few but good.",
        "All that ends well is well.",
        "A close mouth catches no flies."
    ]

    _ut_start = time.time()
    _results = _translator.batch(src_texts)
    for translated_text in _results:
        print(translated_text)
    _ut_end = time.time()
    print(f"Total time taken: {_ut_end - _ut_start:.2f} seconds for src: {len(src_texts)} texts, result: {len(_results)}.")
