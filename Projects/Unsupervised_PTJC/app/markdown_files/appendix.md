## **Appendix**

### Thoughts for the Future:
These are a list of ideas that we didn't have time for this semester, but that we thought could be worthwhile to look into.

#### GANs

**Generative Adversial Networks** is a type of neural network in which there is a generator (a model that tries to generate realistic data) and a discriminator (a model that tries to distinguish real data from the data made from the generator). The way that I would implement this is to create new data. The only problem that would occur is if the generator is not returning good images, so the generator would need to be a very good model in order for the data to be useful. In order to do that we might need to start out with a lot of data as well, which would defeat the intended purpose of creating more data to train on.

**Links for Further Explanation of GAN**: 
* [GeeksForGeeks](https://www.geeksforgeeks.org/generative-adversarial-network-gan/#)
* [AWS](https://aws.amazon.com/what-is/gan/)
* [Medium](https://medium.com/@marcodelpra/generative-adversarial-networks-dba10e1b4424)


#### Different Angles of View

Another aspect to look at is if we were to take slices from different angles. We were taking slices from the saggital view rather than the coronal or the axial view. These could produce better results and could be something to look at in the future.


#### See Application on Other Joints

We recently got a hold of 1370 knee MRI exams. They are categorized into meniscal tears, ACL tears, and general damage. They are also already separated into different views with saggital, coronal, and axial. We could see if the models that we have made can catch similar issues within knee MRIs. We got the images from Standford MRNet challenge and they are not to be used for monetary gain.

