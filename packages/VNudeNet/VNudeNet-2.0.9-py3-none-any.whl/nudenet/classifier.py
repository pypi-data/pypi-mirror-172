from os import mkdir
from os.path import expanduser, join, basename, exists
import cv2
import tarfile
import pydload
import logging
import numpy as np
from numpy import argsort
import onnxruntime
from onnxruntime import InferenceSession

from nudenet.video_utils import get_interest_frames_from_video
from nudenet.image_utils import load_images

from PIL import Image as pil_image
from requests import get

class Classifier:
    """
    Class for loading model and running predictions.
    For example on how to use take a look the if __name__ == '__main__' part.
    """

    nsfw_model = None

    def __init__(self):
        """
        model = Classifier()
        """
        url = "https://huggingface.co/gqfwqgw/NudeNet_classifier_model/resolve/main/classifier_model.onnx"
        model_folder = join(expanduser("~"), ".NudeNet/")
        if not exists(model_folder):
            mkdir(model_folder)

        model_path = join(model_folder, basename(url))

        if not exists(model_path):
            print(f" Downloading the checkpoint {url} to {model_path}")
            with get(url, stream=True) as r:
                print(r.status_code)
                with open(model_path, 'wb') as model_file:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        model_file.write(chunk)
                    # print("\x1b[2k", f"{(i * 8 * 1024) / total:%} Complete", end='\r')

        providers = ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
        self.nsfw_model = InferenceSession(model_path, providers=providers)

    def classify_video(
        self,
        video_path,
        batch_size=4,
        image_size=(256, 256),
        categories=["unsafe", "safe"],
    ):
        frame_indices = None
        frame_indices, frames, fps, video_length = get_interest_frames_from_video(
            video_path
        )
        logging.debug(
            f"VIDEO_PATH: {video_path}, FPS: {fps}, Important frame indices: {frame_indices}, Video length: {video_length}"
        )

        frames, frame_names = load_images(frames, image_size, image_names=frame_indices)

        if not frame_names:
            return {}

        preds = []
        model_preds = []
        while len(frames):
            _model_preds = self.nsfw_model.run(
                [self.nsfw_model.get_outputs()[0].name],
                {self.nsfw_model.get_inputs()[0].name: frames[:batch_size]},
            )[0]
            model_preds.append(_model_preds)
            preds += np.argsort(_model_preds, axis=1).tolist()
            frames = frames[batch_size:]

        probs = []
        for i, single_preds in enumerate(preds):
            single_probs = []
            for j, pred in enumerate(single_preds):
                single_probs.append(
                    model_preds[int(i / batch_size)][int(i % batch_size)][pred]
                )
                preds[i][j] = categories[pred]

            probs.append(single_probs)

        return_preds = {
            "metadata": {
                "fps": fps,
                "video_length": video_length,
                "video_path": video_path,
            },
            "preds": {},
        }

        for i, frame_name in enumerate(frame_names):
            return_preds["preds"][frame_name] = {}
            for _ in range(len(preds[i])):
                return_preds["preds"][frame_name][preds[i][_]] = probs[i][_]

        return return_preds

    def classify(
        self,
        image_paths=[],
        batch_size=4,
        image_size=(256, 256),
        categories=["unsafe", "safe"],
    ):
        """
        inputs:
            image_paths: list of image paths or can be a string too (for single image)
            batch_size: batch_size for running predictions
            image_size: size to which the image needs to be resized
            categories: since the model predicts numbers, categories is the list of actual names of categories
        """
        if not isinstance(image_paths, list):
            image_paths = [image_paths]

        loaded_images, loaded_image_paths = load_images(
            image_paths, image_size, image_names=image_paths
        )

        if not loaded_image_paths:
            return {}

        preds = []
        model_preds = []
        while len(loaded_images):
            _model_preds = self.nsfw_model.run(
                [self.nsfw_model.get_outputs()[0].name],
                {self.nsfw_model.get_inputs()[0].name: loaded_images[:batch_size]},
            )[0]
            model_preds.append(_model_preds)
            preds += argsort(_model_preds, axis=1).tolist()
            loaded_images = loaded_images[batch_size:]

        probs = []
        for i, single_preds in enumerate(preds):
            single_probs = []
            for j, pred in enumerate(single_preds):
                single_probs.append(
                    model_preds[int(i / batch_size)][int(i % batch_size)][pred]
                )
                preds[i][j] = categories[pred]

            probs.append(single_probs)

        images_preds = []

        for i, loaded_image_path in enumerate(loaded_image_paths):
            if not isinstance(loaded_image_path, str):
                loaded_image_path = i

            images_p = {}
            for _ in range(len(preds[i])):
                images_p[preds[i][_]] = float(probs[i][_])
            images_preds.append(images_p)

        return images_preds


if __name__ == "__main__":
    model = Classifier()
    message = (
        "\n Image classifier:\n Enter single image path or multiple images "
        "seperated by || (2 pipes) and and empty line \n")

    while True:
        print(message)
        image_paths = input(" >> ").split("||")
        images = [path.strip() for path in image_paths]
        print(model.classify(images), "\n")
