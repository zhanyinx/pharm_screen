from utils import *
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


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

        control_normalised = control_based_norm(
            alldata, negative_controls, positive_controls
        )
        zscore_normalised = zscore_norm(alldata, negative_controls, positive_controls)

        st.subheader("Download the normalized data")
        st.markdown(
            download_csv(
                zfactors,
                "zfactors.csv",
                "Download zfactors",
            ),
            unsafe_allow_html=True,
        )
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

        ###
        st.subheader("Plot the results")
        zscore_threshold = float(
            st.text_input("Select a threshold based on z-score to filter hits", "-1")
        )
        control_threshold = float(
            st.text_input("Select a threshold based on control to filter hits", "0.5")
        )

        control_normalised.color[
            control_normalised.Average > control_threshold
        ] = "negative hits"
        zscore_normalised.color[
            zscore_normalised.Average > zscore_threshold
        ] = "negative hits"
        col1, col2 = st.columns(2)

        fig = plt.figure()

        ax = sns.scatterplot(
            x=range(len(zscore_normalised)),
            y="Average",
            hue="color",
            data=zscore_normalised,
            ax=fig.add_subplot(111),
        )

        ax.set_ylabel("Normalised average")

        col1.pyplot(fig)

        fig = plt.figure()

        ax = sns.scatterplot(
            x=range(len(control_normalised)),
            y="Average",
            hue="color",
            data=control_normalised,
            ax=fig.add_subplot(111),
        )

        ax.set_ylabel("Normalised average")

        col2.pyplot(fig)

        st.subheader("Download the normalized and filtered data")

        st.markdown(
            download_csv(
                control_normalised[
                    ~(control_normalised.label.isin(positive_controls))
                    & (control_normalised.Average < control_threshold)
                ],
                f"control_normalised_filtered_{control_threshold}.csv",
                "Download control normalised filtered data",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            download_csv(
                zscore_normalised[
                    ~(zscore_normalised.label.isin(positive_controls))
                    & (zscore_normalised.Average < zscore_threshold)
                ],
                f"zscore_normalised_filtered{zscore_threshold}.csv",
                "Download zscore normalised filtered data",
            ),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
