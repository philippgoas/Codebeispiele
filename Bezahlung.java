/** Beispiel: Zahlungsabwicklung mit Polymorphismus
    Schreibe die Methode 'bezahlen' in Zahlungsmethode so um, dass die
    Methoden 'bezahlen' der untergeordneten Klassen effizienter bzw.
    kürzer werden.
    */

// Abstrakte Basisklasse
class Bezahlung {
  static void zurKasse(Zahlungsmethode methode, double betrag) {
    methode.bezahlen(betrag);
  }
  public static void main(String[] args) {
    Zahlungsmethode methode = null;

    methode = new Kreditkarte();
    zurKasse(methode, 99.99);   // Ausgabe: Bezahlt: 99.99 Euro mit Kreditkarte.

    methode = new PayPal();
    zurKasse(methode, 49.99);   // Ausgabe: Bezahlt 49.99 Euro mit PayPal.

    methode = new Bitcoin();
    zurKasse(methode, 0.005);   // Ausgabe: Bezahlt 0.005 Euro mit Bitcoin.
  }
}


abstract class Zahlungsmethode {
  abstract String getName();
  
  void bezahlen(double betrag) {
    System.out.println("Bezahlt: " + betrag + "Euro mit " + getName() );
  }
}

// Abgeleitete Klasse: Kreditkarte
class Kreditkarte extends Zahlungsmethode {
  String getName() { return "Kreditkarte"; }
}

// Abgeleitete Klasse: PayPal
class PayPal extends Zahlungsmethode {
  String getName() { return "Paypal"; }
}

// Abgeleitete Klasse: Bitcoin
class Bitcoin extends Zahlungsmethode {
  String getName() { return "Bitcoin"; }
}

