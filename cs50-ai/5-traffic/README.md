# **Traffic**

In this project I wrote an AI to identify which traffic sign appears in a photograph.

Project details: https://cs50.harvard.edu/ai/2020/projects/5/traffic/

### **Things I tried to create the convolutional neural network (CNN)...**

> Starting off with the CNN design shown in the lecture for recognition of handwritten numbers and testing it with this dataset (after changing the input_shape of the first layer and the number of units of the output layer) resulted in a very low performance (low accuracy and great loss). <br/><br/> My goal was to design a CNN that wasn't complex with a great performance.<br/>I first tried increasing the number of hidden layers and units for each hidden layer, because having a more complex CNN leads to more connections and lower training error at the cost of an overfitting risk... and it did improve the performance, but, having a complex CNN was not my goal. Then I tried changing the activation function 'relu' to 'elu' and the improvement was great. <br/>After trial and error I ended up having a single hidden layer with only 64 units with an 'elu' activation function that was better than the complex CNN.<br/><br/>I also tried changing the number of convolutional (and number of filters) and max-pooling layers, with the goal of having a series of convolutional layers that wouldn't affect heavily the time for eah epoch.<br/>So, my plan was to start with a convolutional layer that would learn a few filters, and after pooling, increase the number of filters for the next convolutional layer, and repeat that process. And it did improve the performance of the CNN!.
