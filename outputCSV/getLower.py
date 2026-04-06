import pandas as pd 
import os

csv_dir = './outputCSV'
csv_path = os.path.join(csv_dir, 'tableSTA.csv')

df = pd.read_csv(csv_path)

def get_lower_arrivals(num_results, arrival_col='arrival_1', cells_col='cells_p1', sort_ascending=True):
    result = df[['design', arrival_col, cells_col, 'size_gates']].copy()
    result = result.sort_values(by=arrival_col, ascending=sort_ascending)
    return result.head(num_results)


print("=== 20 Menores Arrivals - Path 1 ===")
lower_p1 = get_lower_arrivals(20, arrival_col='arrival_1', cells_col='cells_p1')
print(lower_p1.to_string(index=False))

print("=== 20 Menores Arrivals - Path 2 ===")
lower_p1 = get_lower_arrivals(20, arrival_col='arrival_2', cells_col='cells_p2')
print(lower_p1.to_string(index=False))

lower_p1 = get_lower_arrivals(20, arrival_col='arrival_1', cells_col='cells_p1')
lower_p1.to_csv('./outputCSV/lower_path1.csv', index=False)

lower_p2 = get_lower_arrivals(20, arrival_col='arrival_2', cells_col='cells_p2')
lower_p2.to_csv('./outputCSV/lower_path2.csv', index=False)

#print("\n=== 50 Maiores Arrivals - Path 1 ===")
#higher_p1 = get_lower_arrivals(50, arrival_col='arrival_1', cells_col='cells_p1', sort_ascending=False)
#print(higher_p1.to_string(index=False))