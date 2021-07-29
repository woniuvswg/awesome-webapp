
import config_default, config_override, config

conf = config.merge(config_default.configs, config_override.configs)
c = config.toDict(conf)
print(c.session)

