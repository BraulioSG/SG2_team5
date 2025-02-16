from Factory import Factory

class Reporter:
    def __init__(self, factory: Factory) -> None:
        self._factory = factory

    def generate_report(self) -> None:
        mins = list()
        maxs = list()
        averages = list()
        print("")
        print("+-----------------------------+")
        print("|  RESULTS PRODUCTION LINES   |")
        print("+-----+-------+-------+-------+")
        print("| #ID |  MIN  |  MAX  |  AVG  |");
        print("+-----+-------+-------+-------+")
        
        for pl in self._factory.get_production_lines():
            minimum = pl.get_min_time()
            maximum = pl.get_max_time()
            average = pl.get_avg_time()
            print("| #%2d | %5.2f | %5.2f | %5.2f |" % (pl.get_id(), minimum, maximum, average))
            print("+-----+-------+-------+-------+")

            mins.append(minimum)
            maxs.append(maximum)
            averages.append(average)
    
        print("|TOTAL| %5.2f | %5.2f | %5.2f |" % (min(mins), max(maxs), sum(averages)/len(averages)))
        print("+-----+-------+-------+-------+")
