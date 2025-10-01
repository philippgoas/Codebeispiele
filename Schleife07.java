/**
 Implementiere ein Programm, das auf der Konsole ein großes X aus dem
 Zeichen X ausgibt, abhängig von der Variablen int size (size = 3, 4, ..., 10):
 size = 3:     size = 4:      size = 5:      etc.
   X X          X  X           X   X
    X            XX             X X
   X X           XX              X
                X  X            X X
                               X   X
  System.out.print('X');
  System.out.println();
 */

class Schleife07 {
  public static void main( String[] str ) {
    int size = 10;
    for (int i = 0; i < size; i++) {
      for (int j = 0; j < size; j++) {
        if (i==j || i + j == size - 1 ) {
          System.out.print("X");
        } else {
          System.out.print(" ");
        }
      }
    System.out.println();
    }
  }
}
