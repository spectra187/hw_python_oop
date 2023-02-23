from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Union, Type


@dataclass
class InfoMessage:
    """Класс-сообщение c подробностями о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.'
               )

    def get_message(self) -> str:
        """Возвращает объект-сообщение о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс. Содержит основные свойства и методы для тренировок."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Вычисляет пройденную дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Вычисляет среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """
        Вычисляет количество затраченных калорий. Метод вычисления уникален для
        каждой тренировки. Переопределяется в классах-наследниках.
        """
        raise not NotImplementedError(
            "метод get_spent_calories не переопределен у наследника")

    def show_training_info(self) -> InfoMessage:
        """Возвращает сообщение в виде экземпляра класса InfoMessage."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Описывает тренировку - Running."""
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18

    def get_spent_calories(self) -> float:
        """Возвращает затраченные калории для класса Running."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Описывает тренировку - SportsWalking."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    KMH_IN_MSEC: float = 0.278
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CM_IN_M = 100
    HOUR_IN_MINUT = 360

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Возвращает затраченные калории для тренировки SportsWalking."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Описывает тренировку - Swimming."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость для тренировки Swimming."""
        return (self.lenght_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Возвращает затраченные калории для тренировки Swimming."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(type_training: str, data: list) -> Training:
    """
    Считывает данные с датчика. Возвращает экземпляр класса Training.
    Переменная training_comparsion хранит соответствие аббревиатур тренировкам.
    """
    training_comparsion: Dict[str, Union[Swimming, Running, SportsWalking]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if type_training in training_comparsion:
        return training_comparsion[type_training](*data)
    raise KeyError(f'Нет данных о тренировке {type_training}.')


def output(training: Training) -> str:
    """Функция вывода данных в консоль."""
    message: InfoMessage = training.show_training_info()
    return message.get_message()


def main(training: Training) -> None:
    print(Training.show_training_info(training).get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
