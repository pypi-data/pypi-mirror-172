import pyrea
import numpy as np

#import warnings
#warnings.filterwarnings("ignore")

# Ward works now
hc1 = pyrea.clusterer('ward')
hc2 = pyrea.clusterer('ward')

# Fusers:
# Any string is accepted currently
f = pyrea.fuser('agreement')

# Views for ensemble 1
v1 = pyrea.view(np.random.rand(100,10), hc1)
v2 = pyrea.view(np.random.rand(100,10), hc1)
v3 = pyrea.view(np.random.rand(100,10), hc1)

# Ensemble 1
v_computed_1 = pyrea.execute_ensemble([v1, v2, v3], f, hc1)


# Views for ensemble 2
v4 = pyrea.view(np.random.rand(100,10), hc2)
v5 = pyrea.view(np.random.rand(100,10), hc2)
v6 = pyrea.view(np.random.rand(100,10), hc2)

e2 = pyrea.execute_ensemble([v4, v5, v6], f, hc1)

v_t_1 = e1.execute()
v_t_2 = e2.execute()

e3 = pyrea.execute_ensemble([v_t_1, v_t_2], f, hc1)

e3.execute()