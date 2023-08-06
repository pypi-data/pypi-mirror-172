try:
    from enumeration.ModelStatus import ModelStatus
    from enumeration.ModelState import ModelState
except:
    from queue_manager_api.api.src.enumeration.ModelStatus import ModelStatus
    from queue_manager_api.api.src.enumeration.ModelState import ModelState


DEFAULT_STATUS = ModelStatus.NOT_INFORMED
DEFAULT_STATE = ModelState.NOT_INFORMED
