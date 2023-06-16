class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )

    def display_message(self):
        """Вывести сообщение на экран."""
        print(self.get_message())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    LEN_STROKE = 1.38
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
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * self.MIN_IN_H
        mean_speed = self.get_mean_speed()
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * duration_minutes
        )
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration,
                           distance, speed, calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * self.MIN_IN_H
        mean_speed = self.get_mean_speed()
        calories = (
            (0.035 * self.weight + (mean_speed ** 2 / self.height))
            * 0.029 * self.weight * duration_minutes
        )
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration,
                           distance, speed, calories)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_OFFSET = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        duration_minutes = self.duration * self.MIN_IN_H
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / duration_minutes
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * 60
        mean_speed = self.get_mean_speed()
        calories = (
            (mean_speed + self.SPEED_OFFSET)
            * self.SPEED_MULTIPLIER
            * self.weight
            * duration_minutes
        )
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration,
                           distance, speed, calories)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    workout_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in workout_classes:
        workout_class = workout_classes[workout_type]
        return workout_class(*data)
    else:
        raise ValueError("Unknown workout type: {}".format(workout_type))


previous_message = None


def main(training: Training) -> None:
    """Главная функция."""
    global previous_message
    info_message = training.show_training_info()
    message = info_message.get_message()
    if message != previous_message:
        print(message)
        previous_message = message


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
