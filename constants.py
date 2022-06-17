INFO_MESSAGE: str = ('Тип тренировки: {training_type}; '
                     'Длительность: {duration:.3f} ч.; '
                     'Дистанция: {distance:.3f} км; '
                     'Ср. скорость: {speed:.3f} км/ч; '
                     'Потрачено ккал: {calories:.3f}.')
M_IN_KM: float = 1000
MIN_IN_H: float = 60
LEN_PADDLE: float = 1.38
LEN_STEP: float = 0.65
RUNNING_CALORIE_MULTIPLIER_COEFF: float = 18
RUNNING_CALORIE_DOWNGRADER_COEFF: float = 20
WALKING_CALORIE_WEIGHT_MULTIPLIER_COEFF: float = 0.035
WALKING_CALORIE_MEAN_SPEED_MULTIPLIER_COEFF: float = 0.029
SWIMMING_INCREASE_CALORIE_COEFF: float = 1.1
SWIMMING_CALORIE_MULTIPLIER_COEFF: float = 2
