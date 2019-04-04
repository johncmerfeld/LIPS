# LIPS
Final project for Machine Learning at Boston University

Notes / thoughts about data:

  - At least anecdotally, it looks like there's face tracking happening. THat would appear to help us a lot.
  - The folders appear to be grouped by whom is speaking. Not sure if that is relevant to us or not.
  - My current thinking is that we need to feed uniformally-shaped things to the network (that might not be true - I don't really know what I'm talking about). Keras appears to have support for time-dependent stuff like this. That might mean we need to downsample/duplicate frames so that each word fits in the same span of time. So every word is a 3D block of known size, mapped to a value in our dictionary?

