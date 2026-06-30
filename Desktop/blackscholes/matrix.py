import numpy as np
import pandas as pd

x = np.array([1, 2, 3])
y = np.array([4, 5])
X, Y = np.meshgrid(x, y)

st.subheader("Grid X (Horizontal coordinates)")
st.dataframe(pd.DataFrame(X))

st.subheader("Grid Y (Vertical coordinates)")
st.dataframe(pd.DataFrame(Y))
