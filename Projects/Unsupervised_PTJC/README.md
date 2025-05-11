### Overview
We will be working with Washington University in St. Louis. A professor has given us some MRIs of elbows. We will be doing a segmentation for each image to categorize parts of the image for the different types of tissue. Their main objective is to classify the images for PTJC (Post-traumatic Joint Contracture) they want to look at damage to the elbow and classify it that way.

### Tissue
The tissue they specify in the power point to look at for damage:
* Fat
* Bone
* Capsule
* Cartilage
* Ligaments

They emphasize using the Capsule and have traces for capsule already. 

### Steps for Project
* Image Segmentation through Kmeans and Modified UNET with dropout (same structure with 2 dropouts).
* Use a vision transformer to help classify **control** or **injured** from segmented images.
* Make an unsupervised model for classifying level of fibrosis in elbow capsule. 
* Make a web app through Streamlit and Docker. 

### Links to GitHub Gists
* [UNET Segmentation](https://colab.research.google.com/gist/bracken576/51f4c4ad7eed644195c9f80afe153972/advancedsegmentation2.ipynb)
* [UNET Segmentation for All MRIs](https://colab.research.google.com/gist/bracken576/4de2ff72e7021e595646fa025cb18b5e/segslicesandcompressions.ipynb)
* [Classification for Injured and Control](https://colab.research.google.com/gist/bracken576/c74a01273c29647b4c1841e088a41325/mysegmentedversionbiomechanicaldss.ipynb)
* [Masks for Full Segmentation](https://colab.research.google.com/gist/bracken576/7fee22c62a6b97b03c18d8271e18b61f/gettingmasks.ipynb)
* [Kmeans Segmentation w/o Background](https://colab.research.google.com/gist/bracken576/11c6101518f6ceb7d0ccfd212e8e6458/kmeansnobackground.ipynb)
* [Kmeans Segmentation w/o Background for All MRIs](https://colab.research.google.com/gist/bracken576/7a9792e379fd8b1d1c05515e6c39870d/copy-of-previousgroupversionbiomechanicaldss.ipynb)
* [Clustering for PTJC/Capsule Fibrosis Levels](https://colab.research.google.com/gist/bracken576/45c7fd363b39ef8aadab67215ddece7b/unsupervisedclassification_nobackground.ipynb)
