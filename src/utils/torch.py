def set_deterministic() -> None:
    import torch  # type: ignore

    torch.backends.cudnn.determinstic = True  # type: ignore
    torch.backends.cudnn.benchmark = False  # type: ignore
    torch.use_deterministic_algorithms(True, warn_only=True)  # type: ignore
