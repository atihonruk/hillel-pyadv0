from unittest.mock import patch, call

from io_func import archive_file

def test_archive_file():
    expected = [call('old/main.py')]
    with patch('os.rename') as rename:
        archive_file('main.py')
        assert rename.call_args_list == expected
