import tempfile
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# 캐시를 위한 임시 디렉토리 생성
cachedir = tempfile.mkdtemp()

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LinearDiscriminantAnalysis())
], memory=cachedir)
