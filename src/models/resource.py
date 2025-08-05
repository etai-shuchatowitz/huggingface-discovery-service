import os
from pathlib import Path
from typing import ClassVar, Mapping, Sequence
from typing_extensions import Self
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model
from viam.services.generic import Generic

import huggingface_hub as hb

FILE_TYPE_TO_MODEL_FILENAME_DICT = {
    "h5": "tf_model.h5",
    "pytorch": "pytorch_model.bin",
    "safetensors": "model.safetensors"
}

HOME_DIR = str(Path.home())


class HuggingfaceDiscoveryPython(Generic, EasyResource):
    MODEL: ClassVar[Model] = "etais-org:huggingface-discovery-python:huggingface-discovery-python"

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        """This method creates a new instance of this generic.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        if "local_dir" in config.attributes.fields:
            self.local_dir = config.attributes.fields["local_dir"].string_value
        else:
            self.local_dir = f"{HOME_DIR}/.viam/models"
    
    async def do_command(self, command, *, timeout = None, **kwargs):
        model_name = command["model_name"]
        model_type = command["model_type"]
        if "model_filename" in command:
            model_filename = command["model_filename"]
        else:
            model_filename = FILE_TYPE_TO_MODEL_FILENAME_DICT[model_type]

        if "config_filename" in command:
            config_filename = command["config_filename"]
        else:
            config_filename = "config.json"
        if not os.path.isfile(config_filename):
            self.logger.info(f"I am in {os.getcwd()}")
            res = hb.hf_hub_download(model_name, filename=config_filename, local_dir=self.local_dir)
            self.logger.info(f"I have downloaded config to: {res}")
        if not os.path.isfile(model_filename):
            self.logger.info("I am downloading model...")
            res = hb.hf_hub_download(model_name, filename=model_filename, local_dir=self.local_dir)
            self.logger.info(f"I have downloaded model to: {res}")
        return

        
