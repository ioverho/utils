import typing

import omegaconf
import pydantic

if typing.TYPE_CHECKING:
    import logging
    import pathlib


def print_config(args: omegaconf.DictConfig, logger: logging.Logger) -> None:
    """Logs the config file parsed using omegaconf.

    Args:
        args (DictConfig): the configuration object
        logger (logging.Logger): a logger for logging
    """
    logger.info("=" * 80)
    logger.info("CONFIG FILE:\n")
    if args.print_args:
        logger.info(omegaconf.OmegaConf.to_yaml(args, resolve=True))
    else:
        logger.info("Config file not printed.")
    logger.info("=" * 80 + "\n\n")


def save_config(
    args: omegaconf.DictConfig,
    results_dir: pathlib.Path,
    logger: typing.Optional[logging.Logger] = None,
) -> None:
    """Saves the config file parsed using omegaconf to some directory.

    Args:
        args (DictConfig): the configuration object
        results_dir (pathlib.Path): the location where the config is to be saved
        logger (logging.Logger): a logger for logging
    """
    config_yaml = omegaconf.OmegaConf.to_yaml(args, resolve=True)

    output_dir = (results_dir / "config.yaml").resolve()

    output_dir.write_text(config_yaml, encoding="utf8")

    if logger is not None:
        logger.info(f"Config saved to: {str(output_dir)}")


class BasePydanticConfig(pydantic.BaseModel):
    """A base class that enables conversion between omegaconf configs generated by hydra and pydantic models."""

    @classmethod
    def from_hydra(
        cls, config: omegaconf.DictConfig, logger: typing.Optional[logging.Logger]
    ) -> typing.Self:
        config_dict: typing.Dict[str, typing.Any] = omegaconf.OmegaConf.to_object(
            config
        )  # type: ignore

        # Collect the expected keys
        expected_keys: typing.Set[str] = set(cls.model_fields.keys())

        # Find which keys were not expected
        unused_parameters: typing.Set[str] = set(config_dict.keys()) - expected_keys

        # Warn if there are any unused keys
        if len(unused_parameters) > 0:
            if logger is not None:
                logger.warning(
                    f"When constructing '{cls.__name__}', did not use the following parameters: {set(unused_parameters)}"
                )

        # Instantiate the pydantic model using the omegaconf config
        instance: typing.Self = cls(
            **{k: v for k, v in config_dict.items() if k in expected_keys}
        )

        return instance
