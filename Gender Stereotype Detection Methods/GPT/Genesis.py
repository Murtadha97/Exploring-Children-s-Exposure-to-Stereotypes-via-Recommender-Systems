import json

def validate_json_file(file):
    """
        Validate if the json file contains a valid format to be able to use for the experiments and the metrics
    """
    try:
        with open(file) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return False
            for key, value in data.items():
                if not isinstance(key, str) or not isinstance(value, dict):
                    return False
                for inner_key, inner_value in value.items():
                    if not isinstance(inner_key, str) or not isinstance(inner_value, bool):
                        return False
    except (json.JSONDecodeError, FileNotFoundError):
        return False
    return True


def write_model_labels(name, df):
    """
        This method writes a json object with the name of the model as the key
        and as a value a dictionary with MovieIDs as keys and values the label of the stereotype
        name is the name of the model in following format: dataset-name_model-name
        df is a dataframe consisting of 2 columns: MovieID and Stereotype Label
    """
    df_to_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    model = {name: df_to_dict}

    try:
        with open("C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Gender Stereotype Detection Methods\\genesis.json", "r") as f:
            content = f.read()
            # If empty, dump the content. else, append the content.
            if content.strip() == "":
                with open("C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Gender Stereotype Detection Methods\\genesis.json", "w") as f:
                    json.dump(model, f)
            else:
                existing_json = json.loads(content)
                existing_json.update(model)
                with open("C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Gender Stereotype Detection Methods\\genesis.json", "w") as f:
                    json.dump(existing_json, f)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("hi")
