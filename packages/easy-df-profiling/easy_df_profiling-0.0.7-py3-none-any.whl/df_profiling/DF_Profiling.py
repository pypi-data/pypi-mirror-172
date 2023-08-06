def profiling(file):
    import pandas as pd

    # Creating dataframe while reading csv file
    df = pd.read_csv(file,  # file name variable
                     encoding='utf8',  # We set the encoding to utf8 to support Portuguese accents
                     sep=',',  # we set the fields / column separator to comma
                     decimal='.',  # we set the decimal separator to dot
                     parse_dates=True)  # We use the parse_dates parameter to make pandas turn columns into datetime types.

    list_df = []

    columns = df.select_dtypes(include=['integer', "float"]).columns

    if len(columns) >= 0:
        for x, i in enumerate(df.select_dtypes(include=['integer', "float"]).columns):

            current_feature = df[i]

            feature = pd.DataFrame(current_feature.describe())

            feature = feature.round(2).T

            feature.insert(0, "Type", current_feature.dtype)

            feature = feature.rename(columns={'25%': '1st_quartile', '50%': 'median', '75%': '3rd_quartile'})

            feature.insert(2, "missing_values", current_feature.isnull().sum())

            feature.insert(3, "ms%", round((current_feature.isnull().sum() / df.shape[0]) * 100, 2))

            feature.insert(10, "iqr", feature['3rd_quartile'] - feature['1st_quartile'])

            feature.insert(6, "lower_bound_limit", feature["1st_quartile"] - 1.5 * feature["iqr"])

            feature.insert(12, "upper_bound_limit", feature["3rd_quartile"] + 1.5 * feature["iqr"])

            feature.insert(14, "potential_outliers", (feature["max"] > feature["upper_bound_limit"]).any() or (
                        feature["min"] < feature["lower_bound_limit"]).any())

            if x == 0:
                main_df = feature.copy()
                list_df.append(feature)

            if x > 0:
                main_df.append(feature)
                list_df.append(feature)
        try:
            int_float_list_concat = pd.concat(list_df)
        except ValueError:
            pass

    columns = df.select_dtypes(include=['object']).columns

    if len(columns) >= 0:

        list_object = []

        for x in df.select_dtypes(include=['object']).columns:
            feature = pd.DataFrame(df[x].describe()).T

            current_feature = df[x]

            feature.insert(0, "Type", current_feature.dtype)

            feature["unique_V"] = (
                str(current_feature.unique()).replace("[", "").replace("]", "").replace("'", "").replace(" ", ","))

            feature.insert(2, "missing_values", current_feature.isnull().sum())

            feature.insert(3, "ms%", round((current_feature.isnull().sum() / df.shape[0]) * 100, 2))

            list_object.append(feature)
        try:
            list_object_concat = pd.concat(list_object)
        except:
            pass

    if ("int_float_list_concat" in locals() or 'var' in globals()) and (
            "list_object_concat" in locals() or 'var' in globals()):
        final_df = int_float_list_concat.append(list_object_concat)
        final_df.fillna("", inplace=True)
    else:
        try:
            final_df = int_float_list_concat
        except:
            pass
        try:
            final_df = list_object_concat
        except:
            pass

    return final_df
