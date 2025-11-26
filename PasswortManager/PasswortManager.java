package PasswortManager;

import java.util.Scanner;
import java.io.*;


class PasswortManager {

    private static final String file_name = "passwoerter.txt";

    public static void main(String[] args) {
            Scanner scanner = new Scanner(System.in);
    

    while (true) {
        System.out.println("Waehle eine Option:");
        System.out.println("1. Passwort hinzufuegen");
        System.out.println("2. Passwort loeschen");
        System.out.println("3. Passwoerter sehen");
        System.out.println("4. Beenden");
        System.out.println("Auswahl: ");
    

    String auswahlnummer = scanner.nextLine();

    if (auswahlnummer.equals("1")) {
        passworthinzufuegen(scanner);
    } else if (auswahlnummer.equals("2")) {
        passwortloeschen(scanner);
    } else if (auswahlnummer.equals("3")) {
        allepasswoerter();
    } else if (auswahlnummer.equals("4")) {
        break;
    } else {
        System.out.println("Ungueltige Eingabe");
    }

}
}

    public static void passworthinzufuegen(Scanner scanner) {
        System.out.print("Dienst: ");
        String dienst = scanner.nextLine();
        System.out.print("Benutzername: ");
        String benutzername = scanner.nextLine();
        System.out.print("Passwort: ");
        String passwort = scanner.nextLine();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file_name))) {
            writer.write(dienst + " mit dem Benutzernamen'" + benutzername +  "' hat das Passwort: " + passwort);
        } catch (Exception e) {
            System.out.println("Ungueltige Eingabe: " + e.getMessage());
        }
    }

    private static void passwortloeschen(Scanner scanner) {
        System.out.print("Welcher Dienst soll geloescht werden?: ");
        String zuloeschenderdienst = scanner.nextLine();

        File inputFile = new File(file_name);
        File temp = new File("temp.txt");

        boolean found = false;

        try (
            BufferedReader br = new BufferedReader(new FileReader(inputFile));
            PrintWriter pw = new PrintWriter(new FileWriter(temp))
            ) {
                String line;
                while ((line = br.readLine()) != null) {
                    if (line.startsWith(zuloeschenderdienst)) {
                        found = true;
                        continue;
                    }
                    pw.println(line);
                }
            } catch (Exception e) {
                System.out.println("Fehler: " + e.getMessage());
                return;
            }

            if (!found) {
                System.out.println("Kein passender Eintrag.");
                temp.delete();
                return;
            }

            if (inputFile.delete()) {
                temp.renameTo(inputFile);
                System.out.println("Eintrag wurde geloescht!");
            } else {
                System.out.println("Originaldatei kann nicht ersetzt werden!");
            }
    }

    private static void allepasswoerter() {
        try (BufferedReader br = new BufferedReader(new FileReader(file_name))) {
            String line;
            
            while((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (Exception e) {
            System.out.println("Fehler: " + e.getMessage());
        }
    }

}