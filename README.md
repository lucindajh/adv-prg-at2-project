# AT2 Project Journal

### Wed 19/11/2025
- UI: decided on streamlit for creating user UI. Researched some of the features it offers, the dialogue function will come in handy for user error messages.

### Wed 26/11/2025
- Started working on the logging wrapper as the first part of actual code for the app, as it will be fairly easy to make independent of other components and will probably come in handy for testing as I work on the rest of the app
- the other part of this issue is meeting the requirement for implementing the observer pattern - I've created an action logger decorator in the services file for the classifier app. I'm considering for ml-specific event driven logging (logging events throughout the prediction process), create an observer inside the ml directory?
- for now I will move on to implimenting prediction logic for my model - I will be using a torchvision pretrained resnet18 model and the iris dataset.
