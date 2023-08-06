from mlplatform_lib.mlplatform.mlplatform_http_client import (
    MlPlatformHttpClient,
    MlPlatformRequestType,
)
from mlplatform_lib.dataclass.experiment import ExperimentMllabDto
from mlplatform_lib.dataclass.model.model_dto import ModelDto
from mlplatform_lib.dataclass.inference.inference_dto import InferenceDto
from mlplatform_lib.utils.dataclass_utils import from_dict, to_dict
from typing import List
import os
import tarfile
from pathlib import Path

class MllabHttpClient(MlPlatformHttpClient):
    def __init__(self, mlplatform_addr, api_client):
        super().__init__(mlplatform_addr=mlplatform_addr, api_client=api_client)

    def get_experiment(self, experiment_id: int) -> ExperimentMllabDto:
        result = self.send_request("", {"experiments": experiment_id}, {}, {}, MlPlatformRequestType.READ)
        return from_dict(ExperimentMllabDto, result.data)

    def get_model_list(self, experiment_id: int) -> List[ModelDto]:
        res = self.send_request(
            "models", {"experiments": experiment_id}, {}, {}, MlPlatformRequestType.READ
        )

        model_infos = []
        for model_info in res.data:
            model_infos.append(from_dict(ModelDto, model_info))
        return model_infos

    def get_model_by_id(self, experiment_id: int, train_id: int) -> ModelDto:
        res = self.send_request(
            "models",
            {"experiments": experiment_id, "trains": train_id},
            {},
            {},
            MlPlatformRequestType.READ,
        )

        model_infos = []
        for model_info in res.data:
            model_infos.append(from_dict(ModelDto, model_info))
        return model_infos[0]

    def update_model(
        self, experiment_id: int, train_id: int, dto: ModelDto
    ) -> dict:
        res = self.send_request(
            "models",
            {"experiments": experiment_id, "trains": train_id},
            {},
            to_dict(dto),
            MlPlatformRequestType.UPDATE,
        )
        if res.status_code == 200:
            return True
        else:
            return False

    def upload_model(self, experiment_id: int, train_id: int, model_id: int, model_path: str) :
        is_dir = os.path.isdir(model_path)
        if is_dir:
            tar_path = os.path.join(model_path, os.path.basename(model_path) + ".tar.gz")
            with tarfile.open(tar_path, "w:gz") as tar:
                for file in os.listdir(model_path):
                    tar.add(os.path.join(model_path, file), arcname=file)
        else:
            tar_path = os.path.join(os.path.dirname(model_path), "model.tar.gz")
            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(model_path, arcname=os.path.basename(model_path))

        self.send_request(
            "upload",
            {"experiments": experiment_id, "trains": train_id, "models": model_id},
            {},
            Path(tar_path),
            MlPlatformRequestType.CREATE,
        )

        os.remove(tar_path)



    def get_latest_model(self, experiment_id=int) -> ModelDto:
        res = self.send_request(
            "models",
            {"experiments": experiment_id},
            {"latest": "latest"},
            {},
            MlPlatformRequestType.READ,
        )
        return from_dict(ModelDto, res.data[0])

    def get_inference_by_id(
        self, experiment_id: int, train_id: int, model_id: int, inference_id: int
    ) -> InferenceDto:
        res = self.send_request(
            "",
            {"experiments": experiment_id, "trains":train_id, "models": model_id, "inferences": inference_id},
            {},
            {},
            MlPlatformRequestType.READ,
        )

        return from_dict(InferenceDto, res.data)

    def update_inference(self, experiment_id: int, train_id: int, model_id: int, dto: InferenceDto) -> dict:
        res = self.send_request(
            "inferences",
            {"experiments": experiment_id, "trains":train_id, "models": model_id},
            {},
            to_dict(dto),
            MlPlatformRequestType.UPDATE,
        )
        if res.status_code == 200:
            return True
        else:
            return False
