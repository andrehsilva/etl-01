import pandas as pd

from ydata_profiling import ProfileReport

df = pd.read_csv('output/clientes_com_erros.csv')
df.head()


profile = ProfileReport(df, title="Report Clientes")
profile.to_file("output/report_clientes.html")

