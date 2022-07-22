from dataclasses import dataclass, asdict
from typing import Union, Type

# В ТЗ указано писать именно в таком регистре.
# Если константы переводить в верхний регистр
# Код не проходит тесты
# AssertionError: У метода `__init__`
# класса `InfoMessage` должен быть параметр training_type.

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        """Возвращает строку с инфомацией о тренировке."""
        return self.INFO.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.calories = None
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Subclasses should implement this!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60
    MULTIPLIER_FOR_AVERAGE_SPEED: float = 18
    SUBTRACTED_FROM_AVERAGE_SPEED: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в беге."""
        return (
            (
                self.MULTIPLIER_FOR_AVERAGE_SPEED
                * self.get_mean_speed()
                - self.SUBTRACTED_FROM_AVERAGE_SPEED
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60
    MULTIPLIER_FOR_WEIGHT: float = 0.035
    MULTIPLIER_FOR_AVERAGE_SPEED_SPORTS_WALKING: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в ходьбе."""
        return (
            (
                self.MULTIPLIER_FOR_WEIGHT
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.MULTIPLIER_FOR_AVERAGE_SPEED_SPORTS_WALKING
                * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    M_IN_KM: float = 1000
    MULTIPLIER_FOR_AVERAGE_SPEED_SWIMMING: float = 1.1
    MULTIPLER_FOR_WEIGHT_SWIMMING: float = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.get_mean_speed()
                + self.MULTIPLIER_FOR_AVERAGE_SPEED_SWIMMING
            )
            * self.MULTIPLER_FOR_WEIGHT_SWIMMING
            * self.weight
        )

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_generator: dict[str, Type[
        Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout_generator:
        raise KeyError(
            'Invalid training type. '
            'Available types: {}'.format(', '.join(
                [workout_type for workout_type in workout_generator])
            )
        )

    if len(data) == 0:
        raise TypeError(
            'Data can not be null'
        )

    return workout_generator[workout_type](*data)


def main(training: Union[Training, Running, SportsWalking, Swimming]) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)