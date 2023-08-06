import json
import os

from typing import Any, Dict

from cinnaroll_internal.environment_check import API_KEY_ENV_VAR_NAME
from cinnaroll_internal.rollout_config import RolloutConfig
from cinnaroll_internal.rollout import rollout

from tests.unit.model_utils import generate_random_data
from tests.unit.tf_model_utils import create_keras_model_object
from tests.unit.test_simple_nn_models import clean, MODEL_SAVE_PATH

import numpy as np


class MyRolloutConfig(RolloutConfig):
    @staticmethod
    def train_eval(model_objec: Any) -> Dict[str, float]:
        num_samples = 10
        X, Y = generate_random_data(num_samples, input_dim)
        model_object.fit(X, Y, epochs=5)

        accuracy = model_object.evaluate(X, Y)
        metrics = {
            "dataset": "random_floats",
            "accuracy": accuracy
        }
        return metrics

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        X = np.array(json.loads(input_data))
        Y = model_object.predict(X)
        output = {"output": int(Y.argmax())}

        return json.dumps(output)


if __name__ == "__main__":
    os.environ[API_KEY_ENV_VAR_NAME] = "my_api_key"

    input_dim = np.random.randint(5, 10)

    # generate random input to the model
    model_input_sample = generate_random_data(1, input_dim)[0]
    infer_func_input_sample = json.dumps(model_input_sample.tolist())

    dense_layers = (8, 4)
    model_object = create_keras_model_object(input_dim, dense_layers)

    rollout_config = MyRolloutConfig(
        project_id="my_project_id",
        model_object=model_object,
        model_input_sample=model_input_sample,
        infer_func_input_format="json",
        infer_func_output_format="json",
        infer_func_input_sample=infer_func_input_sample,
    )

    print("\nCall infer():")
    output = rollout_config.infer(model_object, infer_func_input_sample)
    print(output)

    print("\nRoll out!")
    rollout(rollout_config)
    clean(MODEL_SAVE_PATH)
