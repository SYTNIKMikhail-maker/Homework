







import pytest
from testing_to_test import even_odd,sum_all,time_of_day, calculate_total_textbook_cost

@pytest.mark.parametrize("number, expected", [
    (2, "even"),
    (4, "even"),
    (3, "odd"),
    (7, "odd"),
    (0, "even"),
])
def test_even_odd(number, expected):
    assert even_odd(number) == expected

@pytest.mark.parametrize("numbers, expected", [
    ((1, 2, 3), 6),
    ((0, 0, 0), 0),
    ((1.5, 2.5), 4.0),
    ((-1, 1), 0),
    ((10,), 10),
])
def test_sum_all(numbers, expected):
    assert sum_all(*numbers) == expected

from freezegun import freeze_time
from testing_to_test import even_odd, sum_all, time_of_day

@freeze_time("2026-01-01 03:00:00")
def test_time_of_day_night():
    assert time_of_day() == "night"

@freeze_time("2026-01-01 09:00:00")
def test_time_of_day_morning():
    assert time_of_day() == "morning"

@freeze_time("2026-01-01 14:00:00")
def test_time_of_day_afternoon():
    assert time_of_day() == "afternoon"

def test_calculate_total_textbook_cost(mocker):
    mocker.patch(
        "testing_to_test.get_book_price",
        side_effect = [10.0, 20.0, 30.0]
)
    result = calculate_total_textbook_cost([1, 2, 3])
    assert result == 60.0

