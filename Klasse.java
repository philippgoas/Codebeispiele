class Klasse {
  public Klasse1 o1 = null;  // Klasse hat ein Objekt von Klasse1
  public Klasse2 o2 = null;  // Klasse hat ein Objekt von Klasse2
  Klasse() {
    // Erzeuge o1 und o2 als Attribute in Klasse, und
    o2 = new Klasse2(2.0);
    o1 = new Klasse1(o2);
    // verlinke o2 als Attribut in o1, so dass o2.a1 == o1.k2.a1:

  }
  public static void main(String[] s) {  // main ist eine Klassenmethode
    // Erzeuge ein Objekt von Klasse:
    Klasse k = new Klasse();

    System.out.println("o2.a1 = " + k.o2.a1);
    System.out.println("o1.k2.a1 = " + k.o1.k2.a1);
  }
}
class Klasse2 {
  public double a1 = 0.0;
  Klasse2(double a1) {
    this.a1 = a1;
    System.out.println("K2");
  }
}
class Klasse1 {
  private String a1 = "hi";
  public Klasse2 k2 = null;    // Klasse1 hat ein Objekt von Klasse2
  Klasse1(Klasse2 k2) {
    this.k2 = k2;
    System.out.println("K1");
  }
}
