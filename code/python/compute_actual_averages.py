"""
The way to compute actual avareges based on observed ones.
This is very sensetive to rounding and therefore not used.


Let $O_{p}, O_{n}$ be the observed averages, computed on hits,  for positives and negatives, and $A_{p}, A_{n}$ be the actual averages, that should be computed on the true labels.
Let $TP, FP, FN, TN$ be the probability of being true positive, false positive, false negative and true negative.
\begin{equation}\label{eq:observes-positive}
O_{p} = TP \cdot A_{p} +
FP \cdot A_{n}
\end{equation}
\begin{equation}\label{eq:observes-negative}
O_{n} = FN \cdot A_{p} +
TN \cdot A_{n}
\end{equation}

Therefore
\begin{equation}\label{eq:actual-negative}
A_{n} =\frac{O_{p} - O_{n}\frac{TP}{FN}}{FP- \frac{TP \cdot TN}{FN}}
\end{equation}
and
\begin{equation}\label{eq:actual-positive}
A_{p} =\frac{O_{n}- O_{p}\frac{FP}{TN}}{FN- \frac{TP \cdot FP}{TN}  }
\end{equation}
This computation is very sensitive to rounding and lead to average of 14.3 file for non corrective commits yet 374.0 for corrective.



"""

def compute_negative_average(observed_positive
                             , observed_negative
                             , tp=( 228/1100)
                             , tn=(795/1100)
                             , fp=(34/1100)
                             , fn=(43/1100)):

    return (observed_positive - observed_negative*tp/fn)/(fp - tp*tn/fn)

def compute_positive_average(observed_positive
                             , observed_negative
                             , tp=(228 / 1100)
                             , tn=(795 / 1100)
                             , fp=(34 / 1100)
                             , fn=(43 / 1100)):

    return (observed_negative -observed_positive*fp/tn)/(fn - tp*fp/tn)

def compute_coupling_average():

    print("Corrective avg commit size"
          , compute_positive_average(observed_positive=6.9
                             , observed_negative=11.6))

    print("Non Corrective avg commit size"
          , compute_negative_average(observed_positive=6.9
                             , observed_negative=11.6))


if __name__ == '__main__':
    compute_coupling_average()