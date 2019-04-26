# LIPS
Final project for Machine Learning at Boston University

To send changes to the cluster and test:
```
## local
scp src/* jcmerf@scc1.bu.edu:/projectnb/cs542sp/jcmerf/src/

## on cluster
# load centOS 7 so we can run dlib
scc-centos7
# run scripts, e.g.
bash pipeline.sh 100 approvedWords1.json vidData1.json x1.npy y1.npy 30 50 pred1.csv

# analysis scripts to come!

```

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
