import streamlit as st
import matplotlib.pyplot as plt
from utils import *


def main():
    """
    This is the main function.
    """

    st.title("Analysis of pharmacological screens")

    negative_controls = ["D11", "E11", "F11", "G11"]
    positive_controls = ["B11", "C11"]
    # Upload a list of files
    uploaded_file = st.sidebar.file_uploader(
        "Please upload your data file(s)",
        type=["xls", "xlsx", "csv"],
        accept_multiple_files=True,
    )

    st.subheader("Below the z factor of each replicate! (needs to be <1)!")
    alldata = pd.DataFrame()
    if uploaded_file is not None:
        for filename in uploaded_file:
            data = excel_processor(filename)
            data["experiment"] = filename.name
            alldata = pd.concat([alldata, data])

        alldata_splitted = split_replicates(alldata)
        zfactors = calculate_z_factor(
            alldata_splitted, positive_controls, negative_controls
        )

        st.dataframe(zfactors)

        control_normalised = control_based_norm(alldata, negative_controls)
        zscore_normalised = zscore_norm(alldata, negative_controls, positive_controls)
        robust_zscore_normalised = robust_zscore_norm(
            alldata, negative_controls, positive_controls
        )

        st.subheader("Download the normalized data")
        st.markdown(
            download_csv(
                control_normalised,
                "control_normalised.csv",
                "Download control normalised data",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            download_csv(
                zscore_normalised,
                "zscore_normalised.csv",
                "Download zscore normalised data",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            download_csv(
                robust_zscore_normalised,
                "robust_zscore_normalised.csv",
                "Download robust zscore normalised data",
            ),
            unsafe_allow_html=True,
        )

        ###
        st.subheader("Plot the results")

        col1, col2 = st.columns(2)

        fig = plt.figure()
        plt.scatter(control_normalised.index, control_normalised.Average)
        plt.scatter(
            control_normalised.index[control_normalised.label.isin(positive_controls)],
            control_normalised.Average[
                control_normalised.label.isin(positive_controls)
            ],
            color="r",
        )
        plt.scatter(
            control_normalised.index[control_normalised.label.isin(negative_controls)],
            control_normalised.Average[
                control_normalised.label.isin(negative_controls)
            ],
            color="green",
        )
        plt.title("Control normalised data")
        plt.legend(["All", "Positive controls", "Negative controls"])
        plt.ylabel("Average control normalised data")
        col1.pyplot(fig)
        plt.show()

        fig = plt.figure()
        plt.scatter(zscore_normalised.index, zscore_normalised.Average)
        plt.scatter(
            zscore_normalised.index[zscore_normalised.label.isin(positive_controls)],
            zscore_normalised.Average[zscore_normalised.label.isin(positive_controls)],
            color="r",
        )
        plt.scatter(
            zscore_normalised.index[zscore_normalised.label.isin(negative_controls)],
            zscore_normalised.Average[zscore_normalised.label.isin(negative_controls)],
            color="green",
        )
        plt.title("Z-score normalised data")
        plt.legend(["All", "Positive controls", "Negative controls"])
        plt.ylabel("Average Z-score")
        col2.pyplot(fig)
        plt.show()


if __name__ == "__main__":
    main()
