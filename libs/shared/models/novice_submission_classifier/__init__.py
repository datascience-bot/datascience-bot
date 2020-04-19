# -*- coding: utf-8 -*-
"""Novice Submission Classifier

Notes:
    This file needs serious improvement before going to prod
        - Tests are non-existant;
        - No training data are saved;
        - Methods are ill-defined and not documented
    to name a few problems

    We should think more deeply about the model requirements.
    Precision/Recall are just the first model evaluation metrics that came
    to mind for this POC.
"""
from typing import Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB

from libs.shared.models.novice_submission_classifier.dataset import DATASET_SCHEMA


DATASET = pd.read_csv(
    # This file is intentionally left out of source control
    "libs/shared/models/novice_submission_classifier/data/novice_submission_labels.csv",
    index_col="id",
)


class NoviceSubmissionClassifier:
    """A proof-of-concept novice submission classifier

    Label novice submissions that belong in the 
    weekly entering & transitioning thread (e.g. arskfw vs. auelq7)

    Notes:
        This model performs quite poorly. That's fine for a POC, but
        we will want to improve (or rewrite entirely) before we go to prod.
        
        Some suggestions for improvement:
            1. Control for unbalanced classes
            2. Consider adding selftext length as a predictor
            3. Tune to improve precision over recall (related to 1)

        Sample scores from private testing:

        --------------
        Training Score
        --------------
        Accuracy Score:   0.755056179775281
        Precision Score:  0.7429245283018868
        Recall Score:     1.0
        # Obs:            445

        -------------
        Testing Score
        -------------
        Accuracy Score:   0.7239057239057239
        Precision Score:  0.7239057239057239
        Recall Score:     1.0
        # Obs:            297
    """

    _required_columns = list(DATASET_SCHEMA.keys())

    def __init__(self):
        # TODO
        pass

    @classmethod
    def clean_dataset(cls, dataset: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Clean the dataset for the model
        """
        # fmt: off
        dataset = (
            dataset.reset_index()
            [cls._required_columns]
            .set_index("id")
            .dropna(subset=["author_name", "selftext"])
        )
        # fmt: on
        dataset["selftext"] = dataset["selftext"].str.lower()

        return dataset[["selftext"]], dataset["label"]


    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.X = X.copy()
        self.y = y.copy()

        self.tv = TfidfVectorizer(
            strip_accents="unicode",
            lowercase=True,
            stop_words="english",
            encoding="utf-8",
        )
        tfidf_vec = self.tv.fit_transform(self.X["selftext"])

        self.naive_bayes = MultinomialNB().fit(tfidf_vec, self.y.ravel())

    def predict(self, X: pd.DataFrame):
        tfidf_vec = self.tv.transform(X["selftext"])
        y_hat = self.naive_bayes.predict(tfidf_vec)

        return y_hat

    def score(self, X: pd.DataFrame, y: pd.Series, y_hat: pd.Series):
        print("Accuracy Score:  ", accuracy_score(y, y_hat))
        print("Precision Score: ", precision_score(y, y_hat))
        print("Recall Score:    ", recall_score(y, y_hat))
        print("# Obs:           ", len(y))
