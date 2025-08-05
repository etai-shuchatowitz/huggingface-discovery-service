# Module huggingface-discovery-service 

Download Models from the Hugginface Repository onto your local machine.

### Configuration
The following attribute template can be used to configure this model:

```json
{
"local_dir": <string>,
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `local_dir`   | string | Optional  | Directory to download to (defaults to ~/.viam/models) |

#### Example Configuration

```json
{
  "local_dir": "."
}
```

### DoCommand

Required arguments:
1. model_name (str): the name of model to download from (ex. "microsoft/resnet-50")
2. model_type (str): the type of the model to download; can be "h5", "pytorch", or "safetensors"

By default if you pass these arguments the service looks in the repository for either
1. h5 -- "tf_model.h5"
2. pytorch -- "pytorch_model.bin"
3. safetensors -- "model.safetensors"

And accordingly it looks for a file called "config.json"

You can override these defaults by passing in the filenames directly:
1. model_filename (str): the explicit filename of the model to download.
2. config_filename (str): the explicit filename of the config to download.

#### Example DoCommand

```json
{
  "model_name": "microsoft/resnet-50",
  "model_type": "h5"
}
```
