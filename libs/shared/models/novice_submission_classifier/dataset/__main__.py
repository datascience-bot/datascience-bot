"""Export dataset to csv
"""
import pandas as pd

from libs.shared.authpraw import get_datascience_bot
from libs.shared.models.novice_submission_classifier.dataset import make_dataset


def main():
    # TODO: I'm pretty sure one doesn't need a reddit user with mod privileges
    # to pull the same dataset
    bob = get_datascience_bot()
    dataset = make_dataset(bob, limit=None)
    dataset.to_csv(
        "novice_submission_labels.csv",
        sep=",",
        index=True,
        encoding="utf-8",
        na_rep="N/A",
    )


if __name__ == "__main__":
    main()
