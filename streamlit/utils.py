import base64
import numpy as np
import pandas as pd


def download_csv(
    df: pd.DataFrame, download_filename: str, download_link_text: str
) -> str:
    """Generates link to download csv of DataFrame.
    Args:
        df: DataFrame to download.
        download_filename: filename and extension of file. e.g. myplot.pdf
        download_link_text: Text to display for download link.
    """
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{download_filename}" target="_blank">{download_link_text}</a>'
    return href


def excel_processor(filename):
    """
    This function processes the uploaded excel file and converts it to a pandas dataframe.
    """
    data = pd.read_excel(filename)
    data = (
        data.iloc[10:16]
        .drop(["Unnamed: 1", "Unnamed: 12"], axis=1)
        .set_index("Unnamed: 0")
    )
    data.columns = range(2, 12)
    data = data.melt(ignore_index=False).reset_index()
    data["label"] = data["Unnamed: 0"] + data["variable"].astype(str)
    data = data[["label", "value"]]
    data.dropna(inplace=True)
    return data


def split_replicates(alldata):
    """
    This function splits the replicates into different columns.
    """
    alldata = alldata.copy()
    alldata[["plate", "replicate"]] = alldata["experiment"].str.extract(
        r"([0-9]*)-([0-9])", expand=True
    )
    alldata.drop("experiment", axis=1, inplace=True)
    alldata = pd.pivot(
        alldata, index=["label", "plate"], columns="replicate", values="value"
    ).reset_index()
    newnames = "replicate" + alldata.columns[2:].values
    alldata.columns = np.append(alldata.columns[:2].values, newnames)

    alldata = alldata.sort_values(["plate", "label"])
    return alldata


def control_based_norm(data, negative_controls):
    """
    This function normalizes the data based on the negative controls.
    """
    data = data.copy()
    average = data[data.label.isin(negative_controls)]["value"].mean()
    data["value"] = data["value"] / average
    data = split_replicates(data)
    data["Average"] = data.iloc[:, 2:].mean(axis=1)
    return data


def zscore_norm(data, negative_controls, positive_controls):
    """
    This function normalizes the data based on the negative controls.
    """
    data = data.copy()
    data_subset = data[
        ~(data.label.isin(negative_controls)) & (~(data.label.isin(positive_controls)))
    ].copy()

    data["value"] = (data["value"] - data_subset["value"].mean()) / data_subset[
        "value"
    ].std()
    data = split_replicates(data)
    data["Average"] = data.iloc[:, 2:].mean(axis=1)
    return data


def robust_zscore_norm(data, negative_controls, positive_controls):
    """
    This function normalizes the data based on the negative controls.
    """
    data = data.copy()
    data_subset = data[
        ~(data.label.isin(negative_controls)) & (~(data.label.isin(positive_controls)))
    ].copy()

    data["value"] = (data["value"] - data_subset["value"].median()) / data_subset[
        "value"
    ].mad()
    data = split_replicates(data)
    data["Average"] = data.iloc[:, 2:].mean(axis=1)
    return data


def calculate_single_z_factor(positive_control_values, negative_control_values):
    """
    This function calculates the z-factor given the value of positive and negative controls.
    """
    zfactor = 1 - 3 * (
        positive_control_values.std() + negative_control_values.std()
    ) / abs(positive_control_values.mean() - negative_control_values.mean())
    return zfactor


def calculate_z_factor(data, positive_controls, negative_controls):
    """
    This function calculates the z-factor for all plates.
    """
    zfactors = pd.DataFrame()
    for plate, subdata in data.groupby("plate"):
        mydict = {"plate": plate}
        for idx in range(2, len(subdata.columns)):
            positive_control_values = subdata.iloc[:, idx][
                subdata.label.isin(positive_controls)
            ]
            negative_control_values = subdata.iloc[:, idx][
                subdata.label.isin(negative_controls)
            ]
            zfactor = calculate_single_z_factor(
                positive_control_values, negative_control_values
            )
            mydict[f"zfactor{idx - 1}"] = zfactor

        zfactors = pd.concat(
            [
                zfactors,
                pd.DataFrame(
                    mydict,
                    index=[0],
                ),
            ]
        )
    return zfactors
