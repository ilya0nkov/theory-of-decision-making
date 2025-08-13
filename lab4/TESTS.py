import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from simplex4 import get_resolutions


class TestJoke(unittest.TestCase):

    def init_table(self):
        table = [
            [2, 1, 0.4, -0.2, 0, 0, 0, 0.2, 0],
            [6, 0, 21/5, 0.4, -1, 0, 0, -0.4, 1],
            [4, 0, -0.4, 0.2, 0, 1, 0, -0.2, 1],
            [5, 0, 1, 0, 0, 0, 1, 0, 0],
                 ]


    @patch("code.get_joke")
    def test_len_joke(self, mock_get_joke):
        mock_get_joke.return_value = 'joke'
        self.assertEqual(get_resolutions(), 4)



if __name__ == "__main__":
    unittest.main()