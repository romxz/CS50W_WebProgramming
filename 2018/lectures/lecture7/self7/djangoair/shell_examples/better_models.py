from flights.models import Airport, Flight

jfk = Airport(code="JFK", city="New York City")
lhr = Airport(code="LHR", city="London")
jfk.save()
lhr.save()

f = Flight(origin=jfk, destination=lhr, duration=415)
f.save()

f.origin
# Returns <Airport: New York City (JFK)>

f.origin.code
# Returns 'JFK'

jfk.departures.all()
# Returns <QuerySet [<Flight: 1 - New York City (JFK) to London (LHR)>]>
