import logging

logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%f'
)

# Другие конфигурации
num_of_steps = 5
template = (
    "Number of observations: {num_observations}\n"
    "Number of heads: {num_heads}\n"
    "Number of tails: {num_tails}\n"
    "Probability of heads: {probability_heads:.2f}\n"
    "Probability of tails: {probability_tails:.2f}\n"
    "Forecast (steps): {num_steps}\n"
    "Forecast tails: {forecast_tails}\n"
    "Forecast heads: {forecast_heads}\n"
)

Telegram_URL = "https://api.telegram.org/bo<token>/sendMessage?chat_id=<...>&text="
