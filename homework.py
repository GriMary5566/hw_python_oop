from typing import Dict, List, Type, ClassVar
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Выводит строку сообщения."""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

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
        return InfoMessage(
            training_type=training_type,
            duration=self.duration,
            distance=distance,
            speed=speed,
            calories=calories
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    K_CAL_SPEED: ClassVar[int] = 18
    K_CAL_CORR: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        cal_per_speed: float = self.K_CAL_SPEED * mean_speed - self.K_CAL_CORR
        cal_per_strain: float = cal_per_speed * self.weight / self.M_IN_KM
        duration_in_min: float = self.duration * self.MIN_IN_H
        return cal_per_strain * duration_in_min


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    K_CAL_WEIGH: ClassVar[float] = 0.035
    K_CAL_STRAIN: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_per_weight: float = self.K_CAL_WEIGH * self.weight
        mean_speed: float = self.get_mean_speed()
        height_strain: float = mean_speed ** 2 // self.height
        cal_per_strain: float = height_strain * self.K_CAL_STRAIN * self.weight
        duration_in_min: float = self.duration * self.MIN_IN_H
        return (cal_per_weight + cal_per_strain) * duration_in_min


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    K_CAL_SPEED: ClassVar[float] = 1.1
    K_CAL_STRAIN: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.length_pool * self.count_pool
        return distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        cal_per_speed: float = mean_speed + self.K_CAL_SPEED
        return cal_per_speed * self.K_CAL_STRAIN * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_objects: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in class_objects:
        raise ValueError('Incorrect type of workout received from sensors')
    return class_objects[workout_type](*data)


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
