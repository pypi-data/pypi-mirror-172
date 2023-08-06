# SnapML Automatic Quantization Pipeline

## Installation:

    pip install git+ssh://git@github.sc-corp.net/Snapchat/snapml_auto_quantization.git --upgrade    

## Uninstallation:

    pip uninstall snapml_auto_quantization

## Exporting ONNX Models:

    torch.onnx.export(net, inputs, onnx_path, verbose=verbose,
                      input_names=input_names, output_names=output_names,
                      keep_initializers_as_inputs=True,
                      operator_export_type=
                      torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK,
                      opset_version=None)

## API Documenation

[Documentation](https://github.sc-corp.net/pages/Snapchat/snapml_auto_quantization/)
