# LIPS
Final project for Machine Learning at Boston University

## To build a model (graders, do this):

  - Make sure Python 3, dlib, imutils, opencv, and Tensorflow/Keras are installed

  - Run the pipeline script, which should handle all steps from reading the raw data to creating the model

```
bash pipeline.sh 100 wordFiles/approvedWords.json vidData/vidData.json modelData/x.npy modelData/y.npy 30 50 predictions/pred.csv
```

This will create two CSV files in the `predictions` folder: `pred.csv` and `pred_ground_truth.csv`. The first has the model's probability output for each class. The second has the actual class vectors.

  - To evaluate the model for both topline accuracy and confusion matrix, follow the procedures in `R/confusionMatrix.R`

## For continued development on the SCC:

To send changes to the cluster and test:
```
## local
scp src/* jcmerf@scc1.bu.edu:/projectnb/cs542sp/jcmerf/src/
# or 
scp src/* ainezm@scc1.bu.edu:/projectnb/cs542sp/jcmerf/src/

## on cluster
# load centOS 7 so we can run dlib
scc-centos7
# run scripts, e.g.
bash pipeline.sh 100 approvedWords1.json vidData1.json x1.npy y1.npy 30 50 pred1.csv

## to submit it as a batch job:
qsub pipelineBatch.sh 200 wordFiles/approvedWords1.json vidData/vidData1.json modelData/x1.npy modelData/y1.npy 30 50 predictions/pred2.csv

# you can check on progress with 
qstat -u ainezm 
# or
qstat -u jcmerf

# output will be printed to output.txt (I added a progress bar in some of the scripts)
# errors will be printed to error.txt

## local
scp jcmerf@scc1.bu.edu:/projectnb/cs542sp/jcmerf/predictions/* .

```
## some notes
`approvedWords1.json` should look like this:
```
{
  "I": 1,
  "ME": 2,
  "YOU": 0
}
```
All the other file names can just be names, they don't need to exist yet.
