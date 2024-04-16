FROM quay.io/jupyter/minimal-notebook:aarch64-ubuntu-22.04


# Install the Python packages 
RUN conda install -y --channel conda-forge \
    numpy==1.26.4 \
    scikit-learn==1.4.2 \
    pandas==2.2.1 \
    matplotlib==3.8.3 \
    nltk==3.8.1 \
    wordcloud==1.9.3 \
    sentence-transformers==2.2.2 \
    jupyterlab==4.1.6 \
    yellowbrick==1.5 \
    make==4.3 \
    bs4==4.12.3 \
    regex==2023.12.25 \
    tabulate==0.9.0 \
    ipython==8.22.2 \
    pypdf==4.2.0 \
    pytest==8.1.1 \
    ipywidgets==8.1.2

# Specify the default command to run
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser"] 