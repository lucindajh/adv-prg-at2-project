# AT2 Project Journal

### Wed 19/11/2025
- UI: decided on streamlit for creating user UI. Researched some of the features it offers, the dialogue function will come in handy for user error messages.

### Wed 26/11/2025
- Started working on the logging wrapper as the first part of actual code for the app, as it will be fairly easy to make independent of other components and will probably come in handy for testing as I work on the rest of the app
- the other part of this issue is meeting the requirement for implementing the observer pattern - I've created an action logger decorator in the services file for the classifier app. I'm considering for ml-specific event driven logging (logging events throughout the prediction process), create an observer inside the ml directory?
- for now I will move on to implimenting prediction logic for my model - I will be using a torchvision pretrained resnet model and the iris dataset.
- I found [this article](https://medium.com/data-science/create-an-image-classification-web-app-using-pytorch-and-streamlit-f043ddf00c24) that may be useful as it goes through creating a classifier app using a streamlit and a resnet model
- realised that for now I think I can just make predictions using the ImageNet dataset the resnet model is trained on
- in order to get a human-readable output from the model prediction, I need to get the names of all the classes in a text file and load them into a list.

### Fri 5/12/2025
- The next step i'm considering is the streamlit frontend, to get some idea of final product. Everything else will be easier to build from there.
- I now have a frontend that allows the user to upload an image, and displays it. I will need to revisit my prediction logic to figure out how i can implement it in predict button code.
- I merged the ml branch into my frontend branch to try and access the predict function- streamlit doesnt seem to like importing modules from outside the app's directory. This probably means i need to setup rest api calls to my classifier backend before i can do any testing of the predict functionality through the frontend.
- I'll now work on my prediction model so I can get started on a view for predictions.

### Sat 6/12/2025
- Starting with making a view so i can get the streamlit app working fully
- my understanding of this process is I create the method using the REST framework in the classfifier/views directory (i'll need "POST" and "GET"), define a url for it in a url.py file i'll need to add to the classifier app, and use that url post the image and get the prediction
- note: django objects.order_by method, "-" at start of the field name to order by indicates descending order
- for now to get the prediction for an image I'm just getting a list ordered by (descending) predicted_at field, so just the most recent one. This should be fine for my use case at the moment but there could be a more fail-safe way to do it in future if I use the fields in the prediction model more effectively, or add one that can link the specific image sent to the prediction
- I'm going to change the output of my predict function to a dict to make it easier to get the values i need
- now moving on to testing the UI - i've connected up the urls and made and applied the first migrations, now running the test server gives me this error:
  Using the URLconf defined in ml_classifier.urls, Django tried these URL patterns, in this order:
    admin/
    api/predictions [name='prediction_for_image']
    The empty path didn’t match any of these.
- My guess is I'm probably missing something in my ml_classifier urls
- after reviewing the notifier app, my second guess is that my site is missing a home page. I'm just going to run the streamlit app and see what happens when i try to use that
- I get the same error when trying to call to the api from the streamlit frontend
- The error I was getting from the streamlit frontend was due to my url being written incorrectly in the api call. The calls are now going through to that url and i just need to fix the code
- The front end is now working, and I will be finalising the issue and opening a pull request.

### Sun 7/12/2025
- Now finishing the logging/observer pattern
- I'm going to seperate out some of the code in my prediction view so I can apply the action logger
- I implemented the action logger, but it isn't working at this point (throws an error) as I haven't implemented the authentication functionality that would allow for a user to be determined
- Before moving on to the authentication issue, I'd like to just get some sort of logging working so I can see that it works and the output appears in the logs, so I'm going to change the action logger for now and come back to it later
- The code now runs without errors but i dont see the output in the app.log file I made so I probably missed some configuration steps
- Logs are going through now and I added a timestamp, I'm now going to move on to the observer to log prediction metadata
- I implemented my observer so I can see in the logs the time between each step in the prediction process. This is useful for assessing any need for optimisation but is quite verbose so I may consider moving this elsewhere for V2.
- Before I move on to the authentication, I'm just going to finalise the ml module issue, which I hadn't yet done as it tests havent been implemented- at this point I've made changes to that module on several other branches so I think it will be best to just update it and then push it into main, and do the testing for it when I'm ready to work on the tests for the whole application.
