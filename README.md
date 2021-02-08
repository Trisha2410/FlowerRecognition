# FlowerRecognition
In this project we have developed a web-based application, which enables the user to browse an image (flower image) from their system and get relevant details like – Scientific name, Kingdom name, Order, Family name along with description and some fun fact about the flower

- Frontend : A web application where user can browse an image and see the details.
- Backend : A CNN ML algorithm that predicts the flower and a code 
          structure to scrape the web for the information, required to be displayed on the GUI.
- Programming Aspect:  We have used -
    Keras (TensorFlow) for building the CNN model.
    Python  for building GUI (Tkinter) and web-scraping.
- Data-Set:  We have taken the dataset from https://www.robots.ox.ac.uk/~vgg/data/flowers/17/index.html containing 17 category flower dataset with 80 images for each class.

Convolution Neural Network:
There are four main operations in the CNN:
    1. Convolution: We extract features from the input image, preserves the spatial relationship between pixels by learning image features using small squares of input data.The  3x3     
                    matrix is called the filter/Kernel/Feature Detector, and the matrix formed by applying the filter over the image and computing the dot product is called the 
                    ‘Convolved Feature’ or ‘Activation Map’ or the ‘Feature Map‘. The more number of filters we have, the more image features get extracted and the better our network 
                    becomes at recognizing patterns in unseen images.
                    
    2. Activation Function (Relu): Relu stands for Rectified Linear Unit and is a non-linear operation. It perform element wise operation (applied per pixel) and replaces all 
                                   negative pixel values in the feature map by zero. The output is given by = max(0,Input). The purpose of Relu is to introduce non-linearity in our 
                                   CNN, since most of the real-world data we would want our CNN to learn would be non-linear.The Relu operation is applied to one of the feature maps 
                                   obtained from the Convolution step and generates a new map referred as the ‘Rectified’ feature map.
                                   
    3. The Pooling Step:  In this step we reduce the dimensionality of the Feature map, retaining the most important information. Spatial Pooling can be of different types: Max, 
                          Average, Sum etc.	
            In case of Max Pooling, we define a spatial neighborhood for example, a 2×2 stride) and take the largest element from the rectified feature map.
            In case of Average Max Pooling, we define a spatial neighborhood (for example, a 2×2 window) and take the average elements from the rectified feature map.
       The function of Pooling is to progressively reduce the spatial size of the input representation. In particular, pooling 
         -  makes the feature dimensions smaller and manageable and   
         -  reduces the number of parameters and computations in the network, therefore, controlling overfitting.
         -  makes the network invariant to small transformations, distortions and translations in the input image.
         -  helps us arrive at an almost scale invariant representation of our image, as it help us to detect objects in an image no matter where they are located
         
     4. . Fully Connected Layer: 
            - The output of the 2nd Pooling Layer acts as an input to the Fully Connected Layer.
            - The Fully Connected layer is a Multi Layer Perceptron, which uses softmax activation function in the output layer. It  implies that every neuron from  the previous 
              layer is connected to the next layer.
            - The output from the convolutional and pooling layers represent high-level features of the input image. 
            - The purpose of the Fully Connected layer is to use these features for classifying the input image into various classes based on the training dataset.
            - The Softmax function ensures that the sum of output probabilities from  a Fully Connected layer is 1.

Conclusion: The Convolution + Pooling layers act as “Feature Extractors” from the input image and  the Fully Connected layer acts as a “classifier”. 
