import json
from PIL import Image
from types import SimpleNamespace
from io import BytesIO
from datetime import datetime, timezone

from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from classifier.models import Prediction
import classifier.views as classifier_views


def build_test_image_upload() -> SimpleUploadedFile:
    img = Image.new("RGB", (224, 224))
    image_buffer = BytesIO()
    img.save(image_buffer, format="jpeg")
    image_buffer.name = "dummy.jpg"
    image_buffer.seek(0)

    return SimpleUploadedFile(
        name=image_buffer.name,
        content=image_buffer.read(),
        content_type="image/jpeg"
    )


def build_stub_prediction() -> SimpleNamespace:
    predicted_at = datetime(2025, 12, 7, 0, 0, 0, tzinfo=timezone.utc)
    return SimpleNamespace(
        predicted_at=predicted_at,
        user="test user",
        imagenet_class="cat",
        probability=95.00
    )


class PredictionForImageTests(TestCase):

    def test_request_prediction(self):
        image = build_test_image_upload()
        url = reverse("prediction_for_image")
        response = self.client.post(
            url,
            {"file": image},
            format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['imagenet_class'])
        self.assertTrue(response.json()['probability'])


class SerialiseDocumentTests(TestCase):

    def test_serialise_prediction(self):
        prediction = build_stub_prediction()
        data = classifier_views.serialise_prediction(prediction)
        self.assertEqual(data['predicted_at'], prediction.predicted_at)
        self.assertEqual(data['user'], prediction.user)
        self.assertEqual(data['imagenet_class'], prediction.imagenet_class)
        self.assertEqual(data['probability'], prediction.probability)

