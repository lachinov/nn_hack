import torch
import numpy as np

from torch._six import container_abcs, string_classes, int_classes

default_collate_err_msg_format = (
    "default_collate: batch must contain tensors, numpy arrays, numbers, "
    "dicts or lists; found {}")

def default_collate(batch):
    r"""Puts each data field into a tensor with outer dimension batch size"""

    elem = batch[0]
    elem_type = type(elem)
    if isinstance(elem, torch.Tensor):
        out = None
        return torch.stack(batch, 0, out=out)
    elif isinstance(elem, np.ndarray):
        try:
            r = np.stack(batch)
        except ValueError:
            r = batch
        return r

    elif isinstance(elem, float):
        return np.array(batch, dtype=np.float32)
    elif isinstance(elem, int_classes):
        return np.array(batch)
    elif isinstance(elem, string_classes):
        return batch
    elif isinstance(elem, container_abcs.Mapping):
        return {key: default_collate([d[key] if key in d else None for d in batch]) for key in elem}
    else:
        return batch

    #raise TypeError(default_collate_err_msg_format.format(elem_type))


def inverse_collate(batch, idx):
    r"""Puts each data field into a tensor with outer dimension batch size"""

    elem_type = type(batch)
    if isinstance(batch, torch.Tensor):
        out = None
        return batch[idx]
    elif isinstance(batch, np.ndarray):
        return batch[idx]
    elif isinstance(batch, list):
        return batch[idx]
    elif isinstance(batch, container_abcs.Mapping):
        return {k: inverse_collate(v,idx) for k, v in batch.items()}

    raise TypeError(default_collate_err_msg_format.format(elem_type))