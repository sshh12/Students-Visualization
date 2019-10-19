import pickle
import plotly.express as px
import pandas as pd

with open('export_merged', 'rb') as f:
    data = pickle.load(f)

df = pd.DataFrame([
    data for sid, data in data.items() 
    if data.get('gpa') and data.get('school')
])

fig = px.scatter(df, x="rank", y="gpa", color="school")
fig.show()