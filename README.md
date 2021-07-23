# Speaker Similarity

```python
pip install -r requirements.txt
```

## Simple Jupiter nb
* Extracts MFCCs, delta1 and zero-crossing-rate from audio clips.
* Simple Neural Network

## Mel-frequency cepstral coefficients (MFCCs)
Mel-frequency cepstral coefficients (MFCCs) are coefficients that collectively make up an MFC. They are derived from a type of cepstral representation of the audio clip (a nonlinear "spectrum-of-a-spectrum"). The difference between the cepstrum and the mel-frequency cepstrum is that in the MFC, the frequency bands are equally spaced on the mel scale, which approximates the human auditory system's response more closely than the linearly-spaced frequency bands used in the normal spectrum. This frequency warping can allow for better representation of sound, for example, in audio compression.


## Zero-crossing rate (ZCR)
Zero crossing rate is the rate at which a signal changes its sign from positive to negative or vice versa within a given time frame.

Zero-crossing rate can be seen as a measure to calculate the noise of a signal. It shows higher values when noise is present. Also it reflects, the spectral characteristics of a signal. It finds use in applications such as speech-music discrimination, speech detection (as in our case) and music genre classification.

## Deep Learning Model
![Alt text](images/nn_model_summary.png?raw=true "Model summary")
![Alt text](images/training_history.png?raw=true "Training history")

## Gaussian Mixture Model
A Gaussian mixture model is a probabilistic model that assumes all the data points are generated from a mixture of a finite number of Gaussian distributions with unknown parameters. One can think of mixture models as generalizing k-means clustering to incorporate information about the covariance structure of the data as well as the centers of the latent Gaussians. A GMM attempts to find a mixture of multi-dimensional Gaussian probability distributions that best model any input dataset.

A GMM uses an expectation–maximization approach which qualitatively does the following:

* Choose starting guesses for the location and shape

* Repeat until converged:

E-step: for each point, find weights encoding the probability of membership in each cluster

M-step: for each cluster, update its location, normalization, and shape based on all data points, making use of the weights

The result of this is that each cluster is associated not with a hard-edged sphere, but with a smooth Gaussian model. Just as in the k-means expectation–maximization approach, this algorithm can sometimes miss the globally optimal solution, and thus in practice multiple random initializations are used.

## Screenshots
![Alt text](images/home.png?raw=true "Home Page")
![Alt text](images/predictions.png?raw=true "Predictions")
![Alt text](images/celebrities.png?raw=true "Celebrities")
