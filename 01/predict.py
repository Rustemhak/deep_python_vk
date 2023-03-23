"""Creating some model and function predict_message_mood"""


class SomeModel:
    """Some model from outside"""

    def predict(self, message: str) -> float:
        """
        :param message: some input message
        :return: some predict
        """
        # реализация не важна


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    """
    :param message: some message
    :param model: some model
    :param bad_thresholds: rating to which an unsatisfactory rating is given
    :param good_thresholds: rating with an excellent rating
    :return: message contains grade
    """
    if model is None:
        raise ValueError("model should be not a None")
    if bad_thresholds is None:
        raise ValueError("bad_thresholds should be not a None")
    if good_thresholds is None:
        raise ValueError("good_thresholds should be not a None")
    if bad_thresholds >= good_thresholds:
        raise ValueError(f"bad_thresholds ({bad_thresholds}) should be less"
                         f" than {good_thresholds} ({good_thresholds})")

    model_prediction = model.predict(message)
    if model_prediction > good_thresholds:
        message = "отл"
    elif model_prediction < bad_thresholds:
        message = "неуд"
    else:
        message = "норм"

    return message
