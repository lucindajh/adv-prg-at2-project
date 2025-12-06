from django.shortcuts import render
from ml.predict import predict
from classifier.models import Prediction
from PIL import Image
# Create your views here.


def serialise_prediction(prediction: Prediction) -> dict:
    return {
        "predicted_at": prediction.predicted_at,
        "user": prediction.user,
        "imagenet_class": prediction.imagenet_class,
        "probability": prediction.probability
    }


@csrf_exempt
def prediction_for_image(request):
    if request.method == "GET":
        predictions = Prediction.objects.order_by("-predicted_at")
        data = serialise_prediction(predictions[0])
        return JsonResponse(data)
    if request.method == "POST" and request.FILES.get('image_upload'):
        uploaded_image = request.FILES['image_upload']
        try:
            img = Image.open(uploaded_image)
        except IOError:
            return JsonResponse({"error": "Image file invalid"}, status=400)

        if img:
            prediction_output = predict(img)
            prediction = Prediction.objects.create(
                imagenet_class=prediction_output['class'],
                probability=prediction_output['prob']
            )
            return JsonResponse(status=200)
        else:
            return JsonResponse({"error": "Image not found"}, status=400)
    return HttpResponseNotAllowed(["GET", "POST"])
