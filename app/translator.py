from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


class Translator:
    def __init__(self):
        self.model = M2M100ForConditionalGeneration.from_pretrained('facebook/m2m100_418M')
        self.tokenizer = M2M100Tokenizer.from_pretrained('facebook/m2m100_418M', src_lang="en", tgt_lang="ja")

    def translate(self, src_text, src_lang="en", tgt_lang="ja"):
        self.tokenizer.src_lang = src_lang
        model_inputs = self.tokenizer(src_text, return_tensors="pt")
        generated_tokens = self.model.generate(**model_inputs, forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang))
        translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return translated_text[0]


if __name__ == "__main__":
    _translator = Translator()

    # src_text = "Life is like a box of chocolates."
    src_texts = [
        "It's never too late to mend."
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
    for src_text in src_texts:
        translated_text = _translator.translate(src_text)

        print(translated_text)
