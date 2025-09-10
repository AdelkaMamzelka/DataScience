import sys
from analytics import Research

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./make_report.py data.csv")
        sys.exit(1)

    file_path = sys.argv[1]
    research = Research(file_path)
    
    try:
        data = research.file_reader(has_header=True)
        print(data)
        
        calculations = Research.Analytics(data)
        counts = calculations.counts(data)
        print(counts[0], counts[1])
        
        fractions = calculations.fractions(*counts)
        print(fractions[0], fractions[1])

        random_predictions = calculations.predict_random(3)
        print(random_predictions)

        last_prediction = calculations.predict_last()
        print(last_prediction)

        research.send_telegram_message("The report has been successfully created")
    except Exception as e:
        print(str(e))
        research.send_telegram_message("The report hasn’t been created due to an error")