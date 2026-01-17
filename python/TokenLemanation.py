from nltk import word_tokenize,pos_tag
from AnahtarKelimeBulma import bow,find_keys_by_value

def get_main_character(text):
    _tokenized=word_tokenize(text)
    tags = tokens_tag = dict(pos_tag(_tokenized))
    özel_isim=find_keys_by_value(tags,"NNP")
    if len(özel_isim) >0:
        return f"""Main Character:  {" ".join(bow(" ".join(özel_isim)))} """


metin = """"
Ali grew up in an ordinary neighborhood, but his dreams always went beyond the ordinary. From a young age, he saw the world around him through a different lens, searching for hidden meanings in every detail. Though he was quiet and kept to himself, his inner world was full of storms. Every morning at sunrise, Ali would take long walks through the narrow streets of the neighborhood, marveling at the small miracles of nature, drawing lessons from everything around him.

Ali had a free spirit, never wanting to fit into predefined molds. His curiosity for science and technology constantly pushed him to learn new things. While he spent hours in front of the computer, he also found peace in the quiet of nature. Throughout his life, he questioned and explored, preferring to ask more questions rather than just finding answers.

There was a fire of passion and determination hidden in his deep eyes, and it seemed that this would be the key to achieving great things. But Ali’s real strength lay in his ability to see the extraordinary in the ordinary moments. Perhaps this was what truly set him apart from others: his vision not only of the world as it was but also as it could be.

"""
print(get_main_character(metin))
