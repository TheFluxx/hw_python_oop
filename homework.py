from dataclasses import dataclass, asdict
from typing import Union, Type

import constants


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: str = constants.INFO_MESSAGE

    def get_message(self):
        """Возвращает строку с инфомацией о тренировке."""
        return self.info.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = constants.M_IN_KM
    LEN_STEP: float = constants.LEN_STEP

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
        return self.action * self.LEN_STEP / constants.M_IN_KM

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
    LEN_STEP: float = constants.LEN_STEP

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в беге."""
        return (
                (
                        constants.RUNNING_CALORIE_MULTIPLIER_COEFF
                        * self.get_mean_speed() - constants.RUNNING_CALORIE_DOWNGRADER_COEFF
                )
                * self.weight / constants.M_IN_KM * self.duration * constants.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = constants.LEN_STEP

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий в ходьбе."""
        return (
                (
                        constants.WALKING_CALORIE_WEIGHT_MULTIPLIER_COEFF
                        * self.weight + (self.get_mean_speed() ** 2 // self.height)
                        * constants.WALKING_CALORIE_MEAN_SPEED_MULTIPLIER_COEFF * self.weight
                )
                * self.duration * constants.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = constants.LEN_PADDLE

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                 + constants.SWIMMING_INCREASE_CALORIE_COEFF)
                * constants.SWIMMING_CALORIE_MULTIPLIER_COEFF * self.weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_generator: dict[str, Type[
        Union[Training]]] = {
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
    training: Union[Training] = workout_generator[workout_type](*data)
    return training


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
        