from typing import Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __post_init__(self) -> None:
        """Переопределяет атрибуты"""
        self.training_type: str = f'Тип тренировки: {self.training_type}; '
        self.duration: str = f'Длительность: {self.duration:.3f} ч.; '
        self.distance: str = f'Дистанция: {self.distance:.3f} км; '
        self.speed: str = f'Ср. скорость: {self.speed:.3f} км/ч; '
        self.calories: str = f'Потрачено ккал: {self.calories:.3f}.'

    def get_message(self) -> str:
        """Выводит строку сообщения."""
        finaly_message: str = ''
        for message in asdict(self).values():
            finaly_message += message
        return finaly_message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
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
        raise NotImplementedError('I need to be implemented!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.__class__.__name__
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type=training_type, duration=self.duration,
                           distance=distance, speed=speed, calories=calories)


class Running(Training):
    """Тренировка: бег."""

    K_CALORIE_1: int = 18
    K_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        cal_per_speed: float = self.K_CALORIE_1 * mean_speed - self.K_CALORIE_2
        cal_per_weight: float = cal_per_speed * self.weight / self.M_IN_KM
        duration_in_min: float = self.duration * self.H_IN_MIN
        return cal_per_weight * duration_in_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_CALORIE_1: float = 0.035
    K_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        cal_per_weight_1: float = self.K_CALORIE_1 * self.weight
        mean_speed: float = self.get_mean_speed()
        cal_per_height: float = mean_speed ** 2 // self.height
        cal_per_speed: float = cal_per_height * self.K_CALORIE_2 * self.weight
        duration_in_min: float = self.duration * self.H_IN_MIN
        return (cal_per_weight_1 + cal_per_speed) * duration_in_min


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_CALORIE_1: float = 1.1
    K_CALORIE_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.length_pool * self.count_pool
        return distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed: float = self.get_mean_speed()
        return (mean_speed + self.K_CALORIE_1) * self.K_CALORIE_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_objects: Dict[str, Training] = {'RUN': Running,
                                          'WLK': SportsWalking,
                                          'SWM': Swimming
                                          }
    if workout_type in class_objects:
        return class_objects[workout_type](*data)
    else:
        raise ValueError('Incorrect type of workout received from sensors')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    message: str = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
