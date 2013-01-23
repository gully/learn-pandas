from pandas import *
import numpy as np
from statsmodels import *
randn = np.random.randn



ts = Series(randn(20), index=date_range('1/1/2000', periods=20))
print ts
df = DataFrame(randn(20, 2), index=ts.index,
                columns=['A', 'B'])
print df

model = ols(y=df.index, x=df['A'])

print model.predict()


