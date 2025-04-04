#include <iostream>
#include <string>
using namespace std;


class Ticket {
protected:
    string event_name;
    int price;

public:
    Ticket(const string& event, int ticketPrice)
        : event_name(event), price(ticketPrice) {}

    void displayDetails() {
        cout << "Event: " << event_name << endl;
        cout << "Price: $" << price << endl;
    }
};

class ConcertTicket : public Ticket {
public:
    ConcertTicket(const string& event, int ticketPrice)
        : Ticket(event, ticketPrice) {}
};


class MovieTicket : public Ticket {
public:
    MovieTicket(const string& event, int ticketPrice)
        : Ticket(event, ticketPrice) {}
};


class Booking : public ConcertTicket, public MovieTicket {
public:
    Booking(const string& concert, int concertPrice, const string& movie, int moviePrice)
        : ConcertTicket(concert, concertPrice), MovieTicket(movie, moviePrice) {}

    void displayBookingDetails() {
        cout << "Concert Details: " << endl;
        ConcertTicket::displayDetails();
        cout << endl;
        cout << "Movie Details: " << endl;
        MovieTicket::displayDetails();
    }
};

int main() {
    string concertName, movieName;
    int concertPrice, moviePrice;
    getline(cin, concertName);
    cin >> concertPrice;
    cin.ignore(); 
    getline(cin, movieName);
    cin >> moviePrice;
    cin.ignore();
    Booking booking(concertName, concertPrice, movieName, moviePrice);
    booking.displayBookingDetails();

    return 0;
}
