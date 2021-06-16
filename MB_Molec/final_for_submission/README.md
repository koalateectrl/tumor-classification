# Instructions for setup
1) Ensure that you have Anaconda installed in your system. If not, please see install instructions from Anaconda (https://www.anaconda.com/products/individual#Downloads).

2) In your terminal, create a new conda environment: conda create -n testenv python=3.7

3) Activate the newly created environment: conda activate testenv

3) Install requirements file: pip install -r requirements.txt

4) Open up Jupyter Notebook: jupyter notebook

5) Run the code! If any issues with installs, please check that the kernel in the jupyter notebook is set to be that of the newly created environment "testenv".

# Notebooks
The binary classifiers are named:
1) group3_group4.ipynb
2) group3_rest.ipynb
3) shh_infant_child.ipynb
4) wnt_shh.ipynb

These classifiers were performed initially in order to perform model selection as to which model to include in the overall multiclass classifier.

The two approaches we used for multiclass classification are located:
1) direct_3_way.ipynb
2) two_stage_classifier.ipynb

Our final successful results come from the two_stage_classifier.ipynb, which we name the "Sequential Classifier."
