import sys
from analytics import Analytics, Research
from config import num_of_steps, template


def make_report(file_path):
    research = Research(file_path)
    data = research.file_reader(has_header=True)
    
    analytics = Analytics(data)
    counts = analytics.counts()
    fractions = analytics.fractions(*counts)
    forecast = analytics.predict_random(num_of_steps)
    
    report = template.format(
        num_observations=len(data),
        num_tails=counts[1],
        num_heads=counts[0],
        probability_tails=fractions[1],
        probability_heads=fractions[0],
        num_steps=num_of_steps,
        forecast_tails=forecast[0][1],
        forecast_heads=forecast[0][0]
    )
    
    analytics.save_file(report, "report", "txt")
    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./make_report.py data.csv")
        sys.exit(1)

    file_path = sys.argv[1]
    report = make_report(file_path)
    print(report)