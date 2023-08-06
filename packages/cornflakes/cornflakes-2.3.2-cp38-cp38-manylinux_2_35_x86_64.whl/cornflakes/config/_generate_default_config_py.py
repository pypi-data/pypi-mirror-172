"""Module with function to generate automatically default-config module."""
import inspect
import os
import sysconfig

import cornflakes.config._default_config_template


def generate_default_config_py(cfg_class, template_cfg: str = "", target: str = None, default_cfg: str = ""):
    """Function to generate automatically default-config module."""
    if not target:
        target = f'{cfg_class.__name__.replace(".", "/")}/default.py'
    """Function that auto generates default config module from cfg_classes and default-ini-config."""
    if not os.path.exists(template_cfg) and hasattr(cfg_class, "default"):
        with open(template_cfg, "w") as file:
            file.write(cfg_class.default.crate_htw_logger_config().to_ini())

    config = {}
    config_list = []
    for cls_name, cls in inspect.getmembers(cfg_class):
        if inspect.isclass(cls) and cls_name != "default":
            if hasattr(cls, "from_ini"):
                config.update(cls.from_ini(template_cfg).popitem()[1])
            else:
                config.update({cls_name.lower(): cls()})  # configs that are not read as ini files
            config_list.append(cls_name)

    with open(cornflakes.config._default_config_template.__file__) as file:
        template = (
            file.read()
            .replace(
                "# import config",
                f"""from {cfg_class.__name__} import (
    {''',
    '''.join(config_list)}
    )""",
            )
            .replace(
                "pass",
                f"""{'''
    '''.join([f'{cfg_name}: {cfg.__class__.__name__} = None' for cfg_name, cfg in config.items()])}""",
                1,
            )
            .replace('default_cfg: str = ""', f'default_cfg: str = "{default_cfg}"')
            .replace(
                "pass",
                (f"""default_values = {config}
    default_values.update("""
                 """{key: value for key, value in 
                Config.from_ini(files=default_cfg, *args, **kwargs).popitem()[1].items() 
                if key in Config.__slots__}"""
                 """)
    return Config.from_ini(files=default_cfg, *args, **default_values)"""),
            )
        )
    with open(target, "w") as file:
        file.write(template)

    if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
        # fix format
        os.system(f"black {template_cfg} {target}")  # noqa: S605
