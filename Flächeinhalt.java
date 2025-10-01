/** Berechnung des Flächeninhalts von geometrischen Formen mit:
    -super und super(), this, Klassenattribut, Klassenmethode
    */

class Flächeinhalt {
  public static void main(String[] args) {
    // Erstelle Instanzen der verschiedenen Form-Klassen:
    // ein Kreis mit Radius 5
    Kreis k = new Kreis(5);
    // ein Rechteck mit Länge 4 und Breite 6
    Rechteck r = new Rechteck(4, 5);
    // ein Dreieck mit Grundseite 8 und Höhe 5
    Dreieck d = new Dreieck(8,5);
    // Berechne und gebe die Flächeninhalte aus:
    System.out.println("--- Kreis ---\n  Flaecheinhalt: " + k.berechneFlaeche());
    System.out.println("\n--- Rechteck ---\n  Flaecheinhalt: " + r.berechneFlaeche());
    System.out.println("\n--- Dreieck ---\n  Flaecheinhalt: " + d.berechneFlaeche());
    
    // - Erstelle ein Klassenattribut anzahlFormen in Form, so dass bei jedem
    //   erstellten Form-Objekt diese Zahl um 1 erhöht wird.

    // - Erstelle eine Klassenmethode, die die Anzahl der erstellten Form-
    //   Instanzen zurückgibt, und rufe diese hier auf:
    System.out.println("\nEs wurden insgesamt " + Form.getanzahlFormen() + " Formen erstellt");
  }
}


    class Form {
  protected String name;

  private static int anzahlFormen;

  public Form(String name) {
    // weise den Inhalt des Parameter name dem Attribut name zu.
    this.name = name;
    anzahlFormen++;
  }

  public static int getanzahlFormen() {
    return anzahlFormen;
  }

  // Berechnung des Flächeninhalts (wird in abgeleiteten Klassen überschrieben)
  public double berechneFlaeche() {
    System.out.println("Berechnung der Flaeche fuer: " + name);
    return 0.0;  // Für eine allgemeine Form geben wir eine leere Fläche zurück
  }
}

class Kreis extends Form {
  private double radius;
  // Konstruktor, ruft den Konstruktor der Basisklasse mit super() auf
  public Kreis(double radius) {
    // Initialisiere name mit "Kreis" über Forms Konstruktor:
    super("Kreis");
    this.radius = radius;
  }
  // Überschreibt die Methode zur Berechnung des Flächeninhalts für einen Kreis
  public double berechneFlaeche() {
    // Rufe erst die Methode der Basisklasse auf
    super.berechneFlaeche();
    // Berechne dann A = π * r² (benutze Math.PI)
    double ret = Math.PI * radius * radius ;
    return ret;
  }
}

class Rechteck extends Form {
  private double laenge, breite;
  // Konstruktor, ruft den Konstruktor der Basisklasse mit super() auf
  public Rechteck(double laenge, double breite) {
    // Ini  tialisiere mit "Rechteck" über Forms Konstruktor:
    super("Rechteck");
    this.laenge = laenge;
    this.breite = breite;
  }
  // Überschreibt die Methode zur Berechnung des Flächeninhalts für ein Rechteck
  public double berechneFlaeche() {
    // Rufe die Methode der Basisklasse auf
    super.berechneFlaeche();
    // Berechne dann A = l * b
    double ret = laenge * breite;
    return ret;
  }
}

class Dreieck extends Form {
  private double grundseite, hoehe;
  // Konstruktor, ruft den Konstruktor der Basisklasse mit super() auf
  public Dreieck(double grundseite, double hoehe) {
    // Initialisiere mit "Dreieck" über Forms Konstruktor:
    super("Dreieck");
    this.grundseite = grundseite;
    this.hoehe = hoehe;
  }
  // Überschreibt die Methode zur Berechnung des Flächeninhalts für ein Dreieck
  public double berechneFlaeche() {
    // Rufe erst die Methode der Basisklasse auf
    super.berechneFlaeche();
    // Berechne dann A = 1/2 * g * h
    double ret = (grundseite * hoehe) / 2;
    return ret;
  }
}

