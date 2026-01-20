from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LinearDiscriminantAnalysis())
]) # Noncompliant: the memory parameter is not provided
