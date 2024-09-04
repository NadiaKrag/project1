from nltk.corpus import stopwords

STOPWORDS = ["danmark", "denmark", "kbh", "copenhagen", "københavn", "nørrebro", "amager", "vesterbro", "østerbro", "indreby", "delditkbh", "mitkbh", "cph", "torvehallerne"] + stopwords.words(["danish", "english"])