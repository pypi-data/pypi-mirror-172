from pathlib import Path
from typing import List, Tuple

import torch
from torch.nn import Module

from nebullvm.base import DataType, InputInfo

FX_MODULE_NAME = "NebullvmFxModule"


def save_with_torch_fx(model: torch.nn.Module, path: Path):
    traced_model = torch.fx.symbolic_trace(model)
    traced_model.to_folder(path, FX_MODULE_NAME)


def load_with_torch_fx(
    path: Path, state_dict_name: str = "pruned_state_dict.pt"
):
    module_file = path / "module.py"
    with open(module_file, "r") as f:
        module_str = f.read()
    exec(module_str, globals())
    model = eval(FX_MODULE_NAME)()
    model.load_state_dict(torch.load(path / state_dict_name))
    return model


def get_outputs_sizes_torch(
    torch_model: Module, input_tensors: List[torch.Tensor]
) -> List[Tuple[int, ...]]:
    if torch.cuda.is_available():
        input_tensors = [x.cuda() for x in input_tensors]
        torch_model.cuda()
    with torch.no_grad():
        outputs = torch_model(*input_tensors)
        if isinstance(outputs, torch.Tensor):
            return [tuple(outputs.size())[1:]]
        else:
            return [tuple(output.size())[1:] for output in outputs]


def create_model_inputs_torch(
    batch_size: int, input_infos: List[InputInfo]
) -> List[torch.Tensor]:
    input_tensors = (
        torch.randn((batch_size, *input_info.size))
        if input_info.dtype is DataType.FLOAT
        else torch.randint(
            size=(batch_size, *input_info.size),
            low=input_info.min_value or 0,
            high=input_info.max_value or 100,
        )
        for input_info in input_infos
    )
    return list(input_tensors)


def run_torch_model(
    torch_model: torch.nn.Module,
    input_tensors: List[torch.Tensor],
    dtype: torch.dtype = torch.float32,
) -> List[torch.Tensor]:
    torch_model.eval()
    if torch.cuda.is_available():
        torch_model.cuda()
        if dtype != torch.half:
            input_tensors = (t.cuda() for t in input_tensors)
        else:
            input_tensors = (
                t.cuda().half() if t.dtype == torch.float32 else t.cuda()
                for t in input_tensors
            )
    with torch.no_grad():
        pred = torch_model(*input_tensors)
    if isinstance(pred, torch.Tensor):
        pred = [pred.cpu()]
    else:
        pred = [p.cpu() for p in pred]
    return pred
