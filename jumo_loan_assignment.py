import csv

# class for loans aggregation
class Loan:

    def __init__(self, msisdn, network, date, product, amount):
        self.msisdn = msisdn
        self.network = network
        self.date = date
        self.day = date.split("-")[0]
        self.month = date.split("-")[1]
        self.year = date.split("-")[2]
        self.product = product
        self.amount = float(amount)



class AggregatedLoan(Loan):

    def __init__(self, loan):
        Loan.__init__(self, loan.msisdn, loan.network, loan.date, loan.product,
                      loan.amount)
        self.count = 1
        self.aggregate = float(self.amount)

    def add_loan(self, amount):
        self.amount += amount
        self.count += 1
        self.aggregate = float(self.amount / self.count)

    def display_aggregate(self):
        return self.network + ", " + self.product + ", "  + str(self.month) + "," + str(
            self.aggregate) + "," + str(self.count)+ "," + str(self.amount)


#Method to get the sum of the loans
def aggregate_loans(loans):
   
    aggregate_loans = []
    for loan in loans:
        if len(aggregate_loans) > 0:
            found = False
            check = loan
            for aggregate in aggregate_loans:
                if aggregate.network == loan.network and aggregate.year == loan.year and aggregate.month == loan.month and aggregate.product == loan.product:
                    found = True
                    check = aggregate
            if found:
                check.add_loan(loan.amount)
            else:
                new_aggregate = AggregatedLoan(loan)
                aggregate_loans.append(new_aggregate)
        else:
            new_aggregate = AggregatedLoan(loan)
            aggregate_loans.append(new_aggregate)

    return aggregate_loans

loans = []

#open csv file in read mode
with open('Loans.csv', mode='r') as infile:
    reader = csv.reader(infile)
    infile.readline()
    loans = [
        Loan(row[0], row[1].replace("'", ""), row[2].replace("'", ""),
             row[3].replace("'", ""), row[4].replace("'", ""))
        for row in reader
    ]
    infile.close()


aggregated_loans = aggregate_loans(loans)

with open('output.csv', mode='w') as outfile:
    
    outfile.write("Network,Product,month,average,count,amount\n")
    
    for loan in aggregated_loans:
        outfile.write(loan.display_aggregate() + "\n")
    outfile.close()
