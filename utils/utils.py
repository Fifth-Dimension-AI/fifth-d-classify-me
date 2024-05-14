import json
import pandas as pd
import base64
import os
import json

def load_json_file(data=None,)-> list|dict :
    
    classes = data['classes']
    options = data['options']
    queries = [a['query'] for a in data['queries']]
    
    return data, classes, options, queries


def map_dicts_to_dataframe(filepath):
    data, classes, options, queries = load_json_file(filepath)
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(classes)
    
    # Set 'class_id' as the index
    df.set_index('class_id', inplace=True)
    df
    
    return df


def convert_df_to_link(df,file_name='model_results',label='Get this data! :sunglasses:',drop_index=1):
    # Provide a download link for the DataFrame
    if drop_index:
        csv = df.to_csv(index=False,encoding='utf-8-sig')
    else:
        csv = df.to_csv(encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}.csv">{label}</a>'
    return href

def write_json_to_directory(data, filename):
    # Create temp directory if it does not exist
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    # Write JSON object to temp directory
    with open(f'temp/{filename}.json', 'w') as file:
        json.dump(data, file)

