from typing import Optional, Type

from transformers.models.auto import modeling_auto

try:
    from transformers.models.auto import modeling_flax_auto

    from tango.integrations.flax.model import Model as FlaxModel
except ModuleNotFoundError:
    pass

from tango.integrations.torch.model import Model

from .config import Config


def auto_model_wrapper_factory(cls: type) -> Type[Model]:
    class AutoModelWrapper(cls, Model):  # type: ignore
        @classmethod
        def from_pretrained(
            cls, pretrained_model_name_or_path: str, config: Optional[Config] = None, **kwargs
        ) -> Model:
            return super().from_pretrained(pretrained_model_name_or_path, config=config, **kwargs)

        @classmethod
        def from_config(cls, config: Config, **kwargs) -> Model:
            return super().from_config(config, **kwargs)

    return AutoModelWrapper


for name, cls in modeling_auto.__dict__.items():
    if isinstance(cls, type) and name.startswith("AutoModel"):
        wrapped_cls = auto_model_wrapper_factory(cls)
        Model.register(
            "transformers::" + name + "::from_pretrained", constructor="from_pretrained"
        )(wrapped_cls)
        Model.register("transformers::" + name + "::from_config", constructor="from_config")(
            wrapped_cls
        )

try:

    def flax_auto_model_wrapper_factory(cls: type) -> Type[FlaxModel]:
        class AutoModelWrapper(cls, FlaxModel):  # type: ignore
            @classmethod
            def from_pretrained(
                cls, pretrained_model_name_or_path: str, config: Optional[Config] = None, **kwargs
            ) -> FlaxModel:
                return super().from_pretrained(
                    pretrained_model_name_or_path, config=config, **kwargs
                )

            @classmethod
            def from_config(cls, config: Config, **kwargs) -> FlaxModel:
                return super().from_config(config, **kwargs)

        return AutoModelWrapper

    for name, cls in modeling_flax_auto.__dict__.items():
        if isinstance(cls, type) and name.startswith("FlaxAutoModel"):
            wrapped_cls_ = flax_auto_model_wrapper_factory(cls)
            FlaxModel.register(
                "transformers::" + name + "::from_pretrained", constructor="from_pretrained"
            )(wrapped_cls_)
            FlaxModel.register(
                "transformers::" + name + "::from_config", constructor="from_config"
            )(wrapped_cls_)

except NameError:
    pass
