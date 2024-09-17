import pandas as pd
import os

dataset = "gr" # 'crows' or 'stereoset'

dataset_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "datasets")
dataset_dir = "C:/Users/rungruh/OneDrive - Delft University of Technology/Documents/datasets"
if dataset == 'ml':
    st_data_path = dataset_dir + '/raw/Stereotypes/MovieLens_Descriptions.csv'
    save_data_path = "C:/Users/rungruh/OneDrive - Delft University of Technology/Documents/Projects/RecSys2024 - StereotypesRecSysChildren/Re-Analyze data/data/ml_descriptions_processed.csv"
    st_data = pd.read_csv(st_data_path)

    #st_data = st_data.drop(columns=['Unnamed: 0', 'title', 'Year', 'Cast', 'Genres', 'adult'])

    st_data.columns = ['id', 'description']

if dataset == 'gr':
    st_data_path = dataset_dir + '/raw/Stereotypes/GoodReads_Descriptions.csv'
    save_data_path = "C:/Users/rungruh/OneDrive - Delft University of Technology/Documents/Projects/RecSys2024 - StereotypesRecSysChildren/Re-Analyze data/data/gr_descriptions_processed.csv"
    st_data = pd.read_csv(st_data_path)

    st_data.columns = ['id', 'description']
st_data.to_csv(save_data_path, index=False)

