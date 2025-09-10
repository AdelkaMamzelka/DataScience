#!/usr/bin/env python3

def contr_numbers():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    return list_of_tuples

def main():
    country_dict = {country: int(number) for country, number in contr_numbers()}
    sorted_countries = sorted(country_dict.keys(), key=lambda country: (-country_dict[country], country))
    #результат 
    for country in sorted_countries:
        print(country)

if __name__ == "__main__":
    main()