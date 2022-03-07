Setup:

Run:
  createContentTrainingData.py
to parse the input XML files and generate labeled training data.

Run:
  createTrainTestData.py
to read the labeled training data and randomly select training and test
data from that set.

Run:
  createModel.py
to train and test off of the data created by createTrainTestData.py.

Run:
  extractTitles.py
to extract and save the titles of the products.

Run:
  titleModel.py
to generate and save an unsupervised model generated from the titles
extracted by extractTitles.py.
