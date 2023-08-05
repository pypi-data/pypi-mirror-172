# Yaml config

The package gives object like access for config files in yaml format

## Using

`yaml_config` - root package.

### open_config

The function for configuration an object from a file.

The function accepts an unlimited number of arguments. Each argument is a path to the intended configuration file.
The function iterates through all paths in the order in which they were passed to the function. The config that was found first will be used. If the arguments run out and the file is not found, an error will be called.

The function returns the configuration as an python `dict`.

### cut_protocol

The function truncates the protocol at the passed url.

The function takes a url in string format as an argument.

The function returns clear domain without protocol.
