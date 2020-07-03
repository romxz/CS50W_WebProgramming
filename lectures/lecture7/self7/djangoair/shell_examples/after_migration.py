from flights.models import Flight, Passenger

f = Flight.objects.get(pk=1)
f
# Returns <Flight: 1 - New York City (JFK) to London (LHR)>

p = Passenger(first="Alice", last="Adams")
p.save()

p.flights.add(f)
p.flights.all()
# Returns <QuerySet [<Flight: 1 - New York City (JFK) to London (LHR)]>

f.passengers.all()
# Returns <QuerySet [<Passenger: Alice Adams>]>
