# -*- coding: utf-8 -*-
"""Cross-Validation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p1WSwMP8DtulxlBr4qUZIgT2_Xr0EJmp
"""

#libraries and k-fold validation methods
import numpy as np
import pandas as pd
from scipy.special import comb

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from sklearn.model_selection import (
    KFold,
    RepeatedKFold,
    LeaveOneOut,
    LeavePOut,
    StratifiedKFold,
    cross_validate,
    train_test_split,
)

# load dataset
breast_cancer_X, breast_cancer_y = load_breast_cancer(return_X_y=True)
X = pd.DataFrame(breast_cancer_X)
y = pd.Series(breast_cancer_y).map({0:1, 1:0})

X.head()

# percentage of benign (0) and malign tumors (1)

y.value_counts() / len(y)

# split dataset into a train and test set

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)

X_train.shape, X_test.shape

"""# **K-fold Cross-validation**

**penalty**{‘l1’, ‘l2’, ‘elasticnet’, ‘none’}, default=’l2’

Specify the norm of the penalty:

'none': no penalty is added;

'l2': add a L2 penalty term and it is the default choice;

'l1': add a L1 penalty term;

'elasticnet': both L1 and L2 penalty terms are added.

**solver**{‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’}, default=’lbfgs’

Algorithm to use in the optimization problem. Default is ‘lbfgs’. To choose a solver, you might want to consider the following aspects:

For small datasets, ‘liblinear’ is a good choice, whereas ‘sag’ and ‘saga’ are faster for large ones;

For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’ handle multinomial loss;

‘liblinear’ is limited to one-versus-rest schemes.

max_iterint, default=100

Maximum number of iterations taken for the solvers to converge.
"""

# Logistic Regression
logit = LogisticRegression(
    penalty ='l2', C=10, solver='liblinear', random_state=4, max_iter=10000)

# K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=4)

# estimate generalization error
clf =  cross_validate(
    logit,
    X_train, 
    y_train,
    scoring='accuracy',
    return_train_score=True,
    cv=kf, # k-fold
)

clf['test_score']
#accuracy on the 5-fold cross validations

clf

print('mean train set accuracy: ', np.mean(clf['train_score']), ' +- ', np.std(clf['train_score']))
print('mean test set accuracy: ', np.mean(clf['test_score']), ' +- ', np.std(clf['test_score']))

"""# ***Repeat K-fold***"""

# Logistic Regression
logit = LogisticRegression(
    penalty ='l2', C=1, solver='liblinear', random_state=4, max_iter=10000)

# Repeated K-Fold Cross-Validation
#repeat 5-fold 10 times
rkf = RepeatedKFold(
    n_splits=5,
    n_repeats=10,
    random_state=4,
)

print('We expect K * n performance metrics: ', 5*10)

# estimate generalization error
clf =  cross_validate(
    logit,
    X_train, 
    y_train,
    scoring='accuracy',
    return_train_score=True,
    cv=rkf, # k-fold
)

print('Number of metrics obtained: ', len(clf['test_score']))

clf['test_score']

print('mean train set accuracy: ', np.mean(clf['train_score']), ' +- ', np.std(clf['train_score']))
print('mean test set accuracy: ', np.mean(clf['test_score']), ' +- ', np.std(clf['test_score']))

"""# **Leave one out**"""

# Logistic Regression
logit = LogisticRegression(
    penalty ='l2', C=1, solver='liblinear', random_state=4, max_iter=10000)

# Leave One Out Cross-Validation
loo = LeaveOneOut()

print('We expect as many metrics as data in the train set: ', len(X_train))

# estimate generalization error
clf =  cross_validate(
    logit,
    X_train, 
    y_train,
    scoring='accuracy',
    return_train_score=True,
    cv=loo, # k-fold
)

print('Number of metrics obtained: ', len(clf['test_score']))

len(clf['test_score'])

print('mean train set accuracy: ', np.mean(clf['train_score']), ' +- ', np.std(clf['train_score']))
print('mean test set accuracy: ', np.mean(clf['test_score']), ' +- ', np.std(clf['test_score']))

"""# ***Leave P out***"""

# Logistic Regression
logit = LogisticRegression(
    penalty ='l2', C=1, solver='liblinear', random_state=4, max_iter=10000)

# Leave P Out Cross-Validation
lpo = LeavePOut(p=2)

# I take a smaller sample of the data, otherwise
# my computer runs out of memory
X_train_small = X_train.head(100)
y_train_small = y_train.head(100)

# The number of combinations of N things taken k at a time.
print('We expect : ', comb(100,2), ' metrics')


# estimate generalization error
clf =  cross_validate(
    logit,
    X_train_small, 
    y_train_small,
    scoring='accuracy',
    return_train_score=True,
    cv=lpo, # k-fold
)

print('Number of metrics obtained: ', len(clf['test_score']))

print('mean train set accuracy: ', np.mean(clf['train_score']), ' +- ', np.std(clf['train_score']))
print('mean test set accuracy: ', np.mean(clf['test_score']), ' +- ', np.std(clf['test_score']))

"""# ***Stratified K-fold C-V***"""

# Logistic Regression
logit = LogisticRegression(
    penalty ='l2', C=1, solver='liblinear', random_state=4, max_iter=10000)

# Leave P Out Cross-Validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=4)

# estimate generalization error
clf =  cross_validate(
    logit,
    X_train, 
    y_train,
    scoring='accuracy',
    return_train_score=True,
    cv=skf, # k-fold
)

len(clf['test_score'])

print('mean train set accuracy: ', np.mean(clf['train_score']), ' +- ', np.std(clf['train_score']))
print('mean test set accuracy: ', np.mean(clf['test_score']), ' +- ', np.std(clf['test_score']))

