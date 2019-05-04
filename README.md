# LIPS
Final project for Machine Learning at Boston University

## Running experiments
To send changes to the cluster and test:
```
## local
scp src/* jcmerf@scc1.bu.edu:/projectnb/cs542sp/jcmerf/src/

## on cluster
# load centOS 7 so we can run dlib
scc-centos7
# run scripts, e.g.
bash pipeline.sh 100 approvedWords1.json vidData1.json x1.npy y1.npy 30 50 pred1.csv

archive  modelData   pipeline.sh       predictions  shape_predictor_68_face_landmarks.dat  vidData
lib	 output.txt  pipelineBatch.sh  pythonlibs   src	

## to submit it as a batch job:
qsub pipelineBatch.sh 200 wordFiles/approvedWords1.json vidData/vidData1.json modelData/x1.npy modelData/y1.npy 30 50 predictions/pred2.csv

# you can check on progress with 
qstat -u ainezm 
# or
qstat -u jcmerf

# output will be printed to output.txt (I added a progress bar in some of the scripts)
# errors will be printed to error.txt

# analysis scripts to come!

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

Presentation flow:
1. What is lip reading?
2. Where did the data come from?
3. What do the data look like?
4. How did we process the data?
5. How did we train the model?
6. What are our results?


```
scp -r jcmerf@scc1.bu.edu:/projectnb/cs542sp/ainezm/mvlrs_v1/pretrain/5555* .
```
