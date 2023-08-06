import numpy as np
import matplotlib.pyplot as plt

from pynir.utils import simulateNIR
from pynir.Calibration import plsda
from pynir.Calibration import binaryClassificationReport,plot_confusion_matrix

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# simulate NIR data
X,y,wv = simulateNIR(nSample=200,nComp=10,refType=2, noise=1e-5)

Xtrain, Xtest, ytrain,ytest = train_test_split(X,y,test_size=0.2)

# estabilish PLS model
nComp = 10
plsdaModel = plsda(nComp = nComp)
plsdaModel.fit(Xtrain,ytrain)

# 10 fold cross validation for selecting optimal nlv
accuracy_cv = []
yhat_cv  = plsdaModel.crossValidation_predict(nfold = 10)
for i in range(nComp):
    report_cv = binaryClassificationReport(ytrain, yhat_cv[:,i])
    accuracy_cv.append(report_cv["accuracy"])


fig,ax = plt.subplots()
ax.plot(np.arange(nComp)+1,accuracy_cv, marker = "*",label = "Accuracy$_c$$_v$")
ax.set_xlabel("nLV")
ax.set_ylabel("Accuracy")
ax.legend()
plt.show()


optLV = plsdaModel.get_optLV()  # optimized nLV based on cross validation

plsdaModel_opt = plsda(nComp = optLV)
plsdaModel_opt.fit(Xtrain,ytrain)
yhat_train_opt = plsdaModel_opt.predict(Xtrain)
yhat_test_opt = plsdaModel_opt.predict(Xtest)

cm_train_opt = confusion_matrix(y_true=ytrain, y_pred=yhat_train_opt)
cm_test_opt = confusion_matrix(y_true=ytest, y_pred=yhat_test_opt)



plot_confusion_matrix(cm_train_opt,np.unique(y),normalize=False,
                      title="Confusion matrix for prediction on training set")
plot_confusion_matrix(cm_test_opt,np.unique(y),normalize=False,
                      title="Confusion matrix for prediction on testing set")
