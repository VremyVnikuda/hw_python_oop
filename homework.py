from dataclasses import dataclass, asdict
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self):
        """Сообщение о тренировке"""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self, action: int, duration: float, weight: float):
        self.duration = duration
        self.weight = weight
        self.action = action

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration,
                           distance, speed, calories)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Метод get_spent_calories должен "
            "быть определен в дочерних классах."
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * self.MIN_IN_H
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * duration_minutes
        )
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    GRAVITY_CONSTANT = 0.035
    WEIGHT_CONSTANT = 100
    SPEED_CONSTANT = 0.029
    SPEED_CONVERSION_CONSTANT = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spid_m_s = self.get_mean_speed() * self.SPEED_CONVERSION_CONSTANT
        calories = (
            self.GRAVITY_CONSTANT * self.weight
            + (spid_m_s ** 2 / (self.height / self.WEIGHT_CONSTANT))
            * self.SPEED_CONSTANT * self.weight
        ) * self.duration * self.MIN_IN_H
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    KONST_1 = 1.1
    KONST_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        pool = self.length_pool * self.count_pool
        speed = pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self):
        calories = (
            (self.get_mean_speed() + self.KONST_1)
            * self.KONST_2
            * self.weight
            * self.duration
        )
        return calories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные, полученные от датчиков."""
    workout_classes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in workout_classes:
        return workout_classes[workout_type](*data)
    raise ValueError("Unknown workout type: {}".format(workout_type))


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
