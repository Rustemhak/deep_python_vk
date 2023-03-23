"""Testing predict of some module"""
from unittest import TestCase
from unittest.mock import Mock

from predict import predict_message_mood


class TestPredictMessageMood(TestCase):
    """Tests for predict_message_mood function"""

    def test_predict_message_mood_model_param_ok(self):
        """Checking that the parameters match for predict mock
        and predict_message_mood"""
        income_message = "message_text"
        model = Mock()

        model.predict.return_value = 0.3
        predict_message_mood(income_message, model, 0.3, 0.85)

        predict_call_args, _ = model.predict.call_args_list[0]
        self.assertEqual(income_message, predict_call_args[0])

    def test_predict_message_mood_model_is_none_error(self):
        """Tests model parameter is None"""
        with self.assertRaises(ValueError) as context:
            predict_message_mood("message_text", model=None)

        self.assertEqual(ValueError, type(context.exception))
        self.assertEqual("model should be not a None", str(context.exception))

    def test_predict_message_mood_bad_thresholds_is_none_error(self):
        """Tests bad_thresholds parameter is None"""
        with self.assertRaises(ValueError) as context:
            predict_message_mood("message_text", "model", bad_thresholds=None)

        self.assertEqual(ValueError, type(context.exception))
        self.assertEqual("bad_thresholds should be not a None",
                         str(context.exception))

    def test_predict_message_mood_good_thresholds_is_none_error(self):
        """Tests good_thresholds parameter is None"""
        with self.assertRaises(ValueError) as context:
            predict_message_mood("message_text", "model", good_thresholds=None)

        self.assertEqual(ValueError, type(context.exception))
        self.assertEqual("good_thresholds should be not a None",
                         str(context.exception))

    def test_predict_message_mood_bad_not_less_good_error(self):
        """Tests bad_thresholds not less good_thresholds parameter"""
        with self.assertRaises(ValueError) as context:
            threshold_value = 0.5
            predict_message_mood("message_text", "model",
                                 bad_thresholds=threshold_value,
                                 good_thresholds=threshold_value)
        self.assertEqual(ValueError, type(context.exception))
        error_message = f"bad_thresholds ({threshold_value}) should be less" \
                        f" than {threshold_value} ({threshold_value})"
        self.assertEqual(error_message, str(context.exception))

    def test_predict_message_mood_good_value(self):
        """Tests good message from predict_message_mood"""
        model = Mock()

        predict_value = 0.85
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index = 0
        message = predict_message_mood(income_message, model, 0.3, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("отл", message)

        predict_value = 0.95
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("отл", message)

        predict_value = 0.85
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.85)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertNotEqual("отл", message)

    def test_predict_message_mood_ok_value(self):
        """Tests ok message from predict_message_mood"""
        model = Mock()

        predict_value = 0.8
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index = 0
        message = predict_message_mood(income_message, model, 0.3, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("норм", message)

        predict_value = 0.55
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("норм", message)

        predict_value = 0.3
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.85)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("норм", message)

        predict_value = 0.29
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.85)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertNotEqual("норм", message)

        predict_value = 0.86
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.85)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertNotEqual("норм", message)

    def test_predict_message_mood_bad_value(self):
        """Tests bad message from predict_message_mood"""
        model = Mock()

        predict_value = 0.29
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index = 0
        message = predict_message_mood(income_message, model, 0.3, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("неуд", message)

        predict_value = 0.1
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.2, 0.8)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertEqual("неуд", message)

        predict_value = 0.3
        income_message = f"message_text_{predict_value}"
        model.predict.return_value = predict_value
        predict_call_index += 1
        message = predict_message_mood(income_message, model, 0.3, 0.85)
        self.assertEqual(
            income_message,
            model.predict.call_args_list[predict_call_index][0][0]
        )
        self.assertNotEqual("отл", message)
