import csv
import numpy
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Create a list of months to acces its index quickly
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Read data in from file
    with open(f'{filename}', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Create empty lists for evidence and labels
        evidence = []
        labels = []
        for row in reader:
            # Create empty sublists of 'evidence' for each 'row' (user)
            evidence_slst = []
            evidence_slst.append(int(row['Administrative']))
            evidence_slst.append(float(row['Administrative_Duration']))
            evidence_slst.append(int(row['Informational']))
            evidence_slst.append(float(row['Informational_Duration']))
            evidence_slst.append(int(row['ProductRelated']))
            evidence_slst.append(float(row['ProductRelated_Duration']))
            evidence_slst.append(float(row['BounceRates']))
            evidence_slst.append(float(row['ExitRates']))
            evidence_slst.append(float(row['PageValues']))
            evidence_slst.append(float(row['SpecialDay']))
            evidence_slst.append(MONTHS.index(row['Month']))
            evidence_slst.append(int(row['OperatingSystems']))
            evidence_slst.append(int(row['Browser']))
            evidence_slst.append(int(row['Region']))
            evidence_slst.append(int(row['TrafficType']))
            evidence_slst.append(int((1 if row['VisitorType'] == 'Returning_Visitor' else 0)))
            evidence_slst.append(int((1 if row['Weekend'] == 'TRUE' else 0)))
            # Append to 'evidence' and 'labels' 
            evidence.append(evidence_slst)
            labels.append(int(1 if row['Revenue'] == 'TRUE' else 0))
    
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create model
    model = KNeighborsClassifier(n_neighbors=1)
    # Fit model
    model.fit(evidence, labels)
    # Return fitted k-nearest neighbor model
    return model
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Get the number of actual positive and negative labels that were accurately 
    # predicted
    actual_positive_predictions = 0
    actual_negative_predictions = 0
    for i in range(len(labels)):
        if labels[i] == predictions[i] == 1:
            actual_positive_predictions += 1
        if labels[i] == predictions[i] == 0:
            actual_negative_predictions += 1
    
    # Get the number of positive and negative predictions
    total_positive_predictions = (1 == predictions).sum()
    total_negative_predictions = (0 == predictions).sum()
    
    # Determine sensitivity and specificity
    sensitivity = actual_positive_predictions/float(total_positive_predictions)
    specificity = actual_negative_predictions/float(total_negative_predictions)

    return (sensitivity, specificity)
    

if __name__ == "__main__":
    main()
