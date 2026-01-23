import pandas as pd

trains = pd.read_csv(r'E:/Indian Train/data/trains_with_coaches.csv')
rows = trains[trains['from_code'].isin(['GUHX','PURI']) | trains['to_code'].isin(['GUHX','PURI'])]
print(rows[['train_no','from_station','to_station','from_code','to_code']].to_string(index=False))
