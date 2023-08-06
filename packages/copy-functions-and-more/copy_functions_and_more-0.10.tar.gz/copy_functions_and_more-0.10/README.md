

### Create an independent copy of any object, function etc.

```python
pip install copy-functions-and-more 
```

```python
from copy_functions_and_more import copy_func
import pandas as pd

df = pd.read_csv(    "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
copieddescribe = copy_func(df.describe)
print(copieddescribe())
copy_func(df.__str__)
strco=copy_func(df.__str__)
print(strco())
print(copieddescribe is df.describe)
print(copieddescribe == df.describe)
print(strco is df.__str__)
print(strco == df.__str__)
```

```python
       PassengerId    Survived      Pclass  ...       SibSp       Parch        Fare
count   891.000000  891.000000  891.000000  ...  891.000000  891.000000  891.000000
mean    446.000000    0.383838    2.308642  ...    0.523008    0.381594   32.204208
std     257.353842    0.486592    0.836071  ...    1.102743    0.806057   49.693429
min       1.000000    0.000000    1.000000  ...    0.000000    0.000000    0.000000
25%     223.500000    0.000000    2.000000  ...    0.000000    0.000000    7.910400
50%     446.000000    0.000000    3.000000  ...    0.000000    0.000000   14.454200
75%     668.500000    1.000000    3.000000  ...    1.000000    0.000000   31.000000
max     891.000000    1.000000    3.000000  ...    8.000000    6.000000  512.329200
[8 rows x 7 columns]
     PassengerId  Survived  Pclass  ...     Fare Cabin  Embarked
0              1         0       3  ...   7.2500   NaN         S
1              2         1       1  ...  71.2833   C85         C
2              3         1       3  ...   7.9250   NaN         S
3              4         1       1  ...  53.1000  C123         S
4              5         0       3  ...   8.0500   NaN         S
..           ...       ...     ...  ...      ...   ...       ...
886          887         0       2  ...  13.0000   NaN         S
887          888         1       1  ...  30.0000   B42         S
888          889         0       3  ...  23.4500   NaN         S
889          890         1       1  ...  30.0000  C148         C
890          891         0       3  ...   7.7500   NaN         Q
[891 rows x 12 columns]
False
False
False
False
```

```python
newlist=[33354,442,4535,333]
newlist2=copy_func(newlist)
print(newlist2 is newlist)
print(newlist2 == newlist)  
False
True


```
