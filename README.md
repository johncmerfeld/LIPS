# LIPS
Final project for Machine Learning at Boston University

To send changes to the cluster and test:
```
# local
scp src/* jcmerf@scc1.bu.edu:/projectnb/cs542sp/jcmerf/src/

# on cluster
bash pipeline.sh [NUMBER_OF_FILES_TO_USE]

# analysis scripts to come!

```



Current plan:

  1. Make a dictionary over the entire timestamped dataset and see how many words are in it (done!)
  2. Split the videos by word (take `k` evenly-spaced frames for long words (partially done. Need to decide what `k` is and downsample.
    * consider ways of increasing the data size)
  3. Isolate the mouth frame by frame (will need to be resized)
  4. At this point, data are in 3-dimensional blocks and have a corresponding word
  5. Flatten those blocks into vectors and feed to neural net -> hidden layer -> output layer is the size of the dictionary





```
scp -r jcmerf@scc1.bu.edu:/projectnb/cs542sp/ainezm/mvlrs_v1/pretrain/5555* .
```
Notes / thoughts about data:

  - At least anecdotally, it looks like there's face tracking happening. THat would appear to help us a lot.
  - The folders appear to be grouped by whom is speaking. Not sure if that is relevant to us or not.
  - My current thinking is that we need to feed uniformally-shaped things to the network (that might not be true - I don't really know what I'm talking about). Keras appears to have support for time-dependent stuff like this. That might mean we need to downsample/duplicate frames so that each word fits in the same span of time. So every word is a 3D block of known size, mapped to a value in our dictionary?

