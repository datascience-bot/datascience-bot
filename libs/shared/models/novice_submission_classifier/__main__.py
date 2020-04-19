from joblib import dump, load
from sklearn.model_selection import train_test_split

from libs.shared.models.novice_submission_classifier import NoviceSubmissionClassifier, DATASET


def main():
    # import labeled data
    classifier = NoviceSubmissionClassifier()
    X, y = classifier.clean_dataset(DATASET)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.6, shuffle=True, random_state=42
    )

    classifier.fit(X_train, y_train)

    print("--------------")
    print("Training Score")
    print("--------------")
    y_train_hat = classifier.predict(X_train)
    classifier.score(X_train, y_train, y_train_hat)

    print("-------------")
    print("Testing Score")
    print("-------------")
    y_test_hat = classifier.predict(X_test)
    classifier.score(X_test, y_test, y_test_hat)

    dump(classifier, "novice_submission_classifier.joblib")

if __name__ == "__main__":
    main()
