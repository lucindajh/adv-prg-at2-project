# AT2 Project Journal

### Wed 19/11/2025
- UI: decided on streamlit for creating user UI. Researched some of the features it offers, the dialogue function will come in handy for user error messages.

### Wed 26/11/2025
- Started working on the logging wrapper as the first part of actual code for the app, as it will be fairly easy to make independent of other components and will probably come in handy for testing as I work on the rest of the app
- the other part of this issue is meeting the requirement for implementing the observer pattern - I've created an action logger decorator in the services file for the classifier app. I'm considering for ml-specific event driven logging (logging events throughout the prediction process), create an observer inside the ml directory?
- for now I will move on to implimenting prediction logic for my model - I will be using a torchvision pretrained resnet model and the iris dataset.
- I found [this article](https://medium.com/data-science/create-an-image-classification-web-app-using-pytorch-and-streamlit-f043ddf00c24) that may be useful as it goes through creating a classifier app using a streamlit and a resnet model https://medium.com/data-science/create-an-image-classification-web-app-using-pytorch-and-streamlit-f043ddf00c24
