/**
  Implementiere ein Java-Programm, das alle 11 möglichen Noten
  auflistet: 1,0 2,0 3,0 4,0 5,0 1,3 2,3 3,3 1,7 2,7 3,7

  Kann dieses Programm auch mit einer einzigen for-Schleife und
  einer einzigen if-Bedingung implementiert werden?

  Benutze System.out.println().
  */

class Schleife04 {
  public static void main( String[] str ) {
     for (int i = 0; i < 11; i++) {
            // Ganze Zahl: 1, 2, 3, 4, 5 (immer 1 + i/3)
            int ganz = 1 + i / 3;

            // Nachkomma: bei i%3 == 0 → ,0 / bei 1 → ,3 / bei 2 → ,7
            double note = ganz;
            if (i % 3 == 1) {
                note += 0.3;
            } else if (i % 3 == 2) {
                note += 0.7;
            }
            
            System.out.println(note);
        }


  }
}
