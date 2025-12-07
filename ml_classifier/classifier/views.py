import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ml.predict import predict
from classifier.models import Prediction
from classifier.services import action_logger
from PIL import Image
from io import BytesIO
# Create your views here.


def serialise_prediction(prediction: Prediction) -> dict:
    return {
        "predicted_at": prediction.predicted_at,
        "user": prediction.user,
        "imagenet_class": prediction.imagenet_class,
        "probability": prediction.probability
    }


@action_logger
def get_prediction_response(img: Image) -> dict:
    prediction_output = predict(img)
    prediction = Prediction.objects.create(
        imagenet_class=prediction_output['class'],
        probability=prediction_output['prob']
    )
    return serialise_prediction(prediction)


def classify_view(request):
    # logging.basicConfig(level=logging.INFO)
    #
    # user = create_user("admin", "Ben")
    # upload_document(user, "project_plan.pdf")
    #
    # logs = []
    # try:
    #     for line in read_logs("notifier/logs.txt"):
    #         logs.append(line)
    # except FileNotFoundError:
    #     logs.append("No logs yet.")
    #
    # asyncio.run(fetch_all_metadata())

    # return render(request, "notifier/index.html", {
    #     "user": user,
    #     "logs": logs
    # })
    return render(request, "notifier/index.html")


@csrf_exempt
def prediction_for_image(request):
    if request.method == "GET":
        predictions = Prediction.objects.order_by("-predicted_at")
        data = serialise_prediction(predictions[0])
        return JsonResponse(data)
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_image = request.FILES['file']
        # stream = uploaded_image.open()
        try:
            img = Image.open(uploaded_image)
        except IOError:
            return JsonResponse({"error": "Image file invalid"}, status=400)

        if img:
            return JsonResponse(get_prediction_response(img), status=200)
        else:
            return JsonResponse({"error": "Image not found"}, status=400)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
