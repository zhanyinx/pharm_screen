[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zhanyinx-hic-scaling-scaling-hic-geuryt.streamlit.app/)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub code licence is MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)]

# Application made for pharma screen at European Institute of Oncology

The application allows to to analyze pharmacological screens. In particular, it allows to compare drug screen hits with positive and negative controls.
It uses different normalisation (control based normalisation and zscore based normalisation).

## Local instance

To have a local instance of the app, install streamlit and the requirements

```bash

conda env create -n hic_scaling --file environment.yml
conda activate hic_scaling
pip install streamlit
```

To run the app

```bash
streamlit run path2/scaling_hic.py
```
