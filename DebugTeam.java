/** Ein Softwareprojekt hat verschiedene Teammitglieder, die auf Bugs reagieren.
    Es gibt eine Basisklasse Entwickler, und davon abgeleitet FrontendEntwickler,
    BackendEntwickler und ein Praktikant, alle mit einer eigenen Methode bearbeiteBug()
    */

class DebugTeam {
  public static void main(String[] args) {
    // Erstelle ein team von drei Entwickler: 1 FrontendEntwickler Anne,
    // 1 BackendEntwickler Bob, und 1 Praktikant mit leerem Name (""):
    FrontendEntwickler f = new FrontendEntwickler("Anne");
    BackendEntwickler b = new BackendEntwickler("Bob");
    Praktikant p = new Praktikant("");



    System.out.println("🐞 Ein Bug wurde entdeckt.\n");
    // Führe bearbeiteBug für jedes Teammitglied aus:

    f.bearbeiteBug();
    b.bearbeiteBug();
    p.bearbeiteBug();


  }
}


  class Entwickler {
  protected String name;
  public Entwickler(String name) {
    // weise den Inhalt des Parameter name dem Attribut name zu.
    this.name = name;
  }
  public void bearbeiteBug() {
    System.out.println(name + " sucht nach dem Bug...");
  }
}

class FrontendEntwickler extends Entwickler {
  public FrontendEntwickler(String name) {
    // Initialisiere name über Entwicklers Konstruktor
    super(name);
  }
  public void bearbeiteBug() {
    // Rufe die Methode der Basisklasse auf
    super.bearbeiteBug();
    System.out.println(name + ": 'Sieht im Browser gut aus.. Backend-Problem.'");
  }
}

class BackendEntwickler extends Entwickler {
  public BackendEntwickler(String name) {
    // Initialisiere name über Entwicklers Konstruktor. Füge das Präfix
    // "Backend" zum Namen hinzu:
    super("Backend" + name);
  }
  public void bearbeiteBug() {
    // Rufe die Methode der Basisklasse auf
    super.bearbeiteBug();
    System.out.println(name + ": 'Läuft auf meinem Rechner..'");
  }
}

class Praktikant extends Entwickler {
  public Praktikant(String name) {
    // Initialisiere name über Entwicklers Konstruktor. Kontrolliere, ob
    // 'name' leer ist (mit isEmpty()), und initialisiere mit den Namen
    // "Anonymous" wenn 'name' leer ist, sonnst mit 'name':
    super(name.isEmpty() ? "Anonymous" : name);

  }
  public void bearbeiteBug() {
    // Rufe die Methode der Basisklasse auf
    super.bearbeiteBug();
    System.out.println(name + ": 'Habe nichts auf StackOverflow gefunden.'");
  }
}


