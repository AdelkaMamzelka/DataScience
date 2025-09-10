num_of_steps = 3  # число шагов для predict_random()
template = """
Report
We have made {num_observations} observations from tossing a coin: {num_tails} of them were tails and {num_heads} 
of them were heads. The probabilities are {probability_tails}% and {probability_heads}%, respectively. 
Our forecast is that in the next {num_steps} observations we will have: {forecast_tails} tails and {forecast_heads} heads.
"""