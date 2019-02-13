Title: Model Selection of Tree Classifiers in R
Slug: tree_selection
Date: 2019-01-28 15:30
Category: Machine Learning
Tags: modeling, classification, r, caret, trees
author: Andrew Trick
Summary: A recent lab for my machine learning class involved fitting and tuning decision tree models in R to find the 'best' option for predicting if a person will default given historic loan data. I work through the process of: processing the data for modeling, fitting it to a C5.0 decision tree model, comparing it to an 10-trial adaptive boosted version, and finally tuning the ensemble model to find the parameters which result in the highest accuracy.

# Model Selection of Tree Classifiers in R (w/ parameter tuning)
<br>
A recent lab for my machine learning class involved fitting and tuning decision tree models in R to find the 'best' option for predicting if a loan will default given fictional historic loan data. I work through the process of: processing the data for modeling, fitting it to a C5.0 decision tree model, comparing it to an 10-trial adaptive boosted version, and finally tuning the ensemble model to find the parameters which result in the highest accuracy.<br><br>
<br>
As most of my past work with machine learning has been done with scikit-learn in Python, I am finding this course to be extremely useful and interesting. Not only has it given me a deeper understanding of the strengths and weaknesses inherent in each type of model, but it also included plenty of practice working in R. The textbook for this course is *"Machine Learning with R"* by Brett Lantz, and much of this process is taken from the book.
Data for this project is located at the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php).

## Data Preprocessing
As this post is focused on model creation and results analysis, I've elected to not report the importing, exploring, and processing steps for this project. Complete code for this project can be found at my [GitHub](https://github.com/leaflettuce/IT460-Coursework/blob/master/week_four/lab_4-2.R).
<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../img/dt_selection/ROC.png" style="width: 800px;"/>