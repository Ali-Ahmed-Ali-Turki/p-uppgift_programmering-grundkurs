import random
import itertools
from tkinter import *
from tkinter import scrolledtext, messagebox, ttk

class Atom:
    """Representerar ett grundämne med dess grundläggande egenskaper.

    Attribut:
        beteckning: Kort beteckning (t.ex. 'H').
        namn: Fullständigt namn (t.ex. 'Väte').
        atomnummer: Atomens nummer i periodiska systemet.
        massa: Atomens relativa atommassa (float).
        period: Periodnummer i periodiska systemet eller None om okänt.
        grupp: Gruppnummer i periodiska systemet eller None om okänt.
    """
    def __init__(self, beteckning, namn, atomnummer, massa, period, grupp):
        self.beteckning = beteckning
        self.namn = namn
        self.atomnummer = atomnummer
        self.massa = massa
        self.period = period
        self.grupp = grupp

class PeriodiskaSystemet:
    """Håller och laddar en lista av Atom-objekt från två textfiler.

    Konstruktorn laddar data från filnamn och extra_filnamn och fyller attributet `atomer`.
    """
    def __init__(self, filnamn='avikt.txt', extra_filnamn='period_group.txt'):
        self.atomer = []
        self.läs_in_data(filnamn, extra_filnamn)

    def läs_in_data(self, filnamn, extra_filnamn):
        """Läser in atomdata från två filer och skapar Atom-objekt.

        Parametrar:
            filnamn: Sökväg till huvudfilen med beteckning, namn, atomnummer och massa.
            extra_filnamn: Sökväg till filen som kan innehålla period och grupp.
        Funktionen parar ihop rader från båda filer med zip_longest och lägger till varje Atom i self.atomer.
        """
        with open(filnamn, 'r', encoding="utf-8") as file1, \
             open(extra_filnamn, 'r', encoding="utf-8") as file2:
            for rad1, rad2 in itertools.zip_longest(file1, file2, fillvalue=""):
                komma_till_pukt = str.maketrans(",", ".")
                rad1 = rad1.rstrip("\n")
                rad2 = rad2.rstrip("\n")
                en_atom = (rad1 + " " + rad2).split()
                if len(en_atom) > 4:
                    atom = Atom(
                        beteckning=en_atom[0],
                        namn=en_atom[1],
                        atomnummer=int(en_atom[2]),
                        massa=float(en_atom[3].translate(komma_till_pukt)),
                        period=int(en_atom[4]),
                        grupp=int(en_atom[5])
                    )
                else:
                    atom = Atom(
                        beteckning=en_atom[0],
                        namn=en_atom[1],
                        atomnummer=int(en_atom[2]),
                        massa=float(en_atom[3].translate(komma_till_pukt)),
                        period=None,
                        grupp=None
                    )
                self.atomer.append(atom)

    def hitta_atom(self, sokterm):
        """Söker efter en atom utifrån namn eller beteckning och returnerar Atom-objekt eller None.

        Parametrar:
            sokterm: Sträng med antingen beteckning eller namn (case-insensitiv).
        Returnerar:
            Atom-objekt om träff finns, annars None.
        """
        for atom in self.atomer:
            if atom.beteckning.lower() == sokterm.lower() or atom.namn.lower() == sokterm.lower():
                return atom
        return None

class Träning:
    """Logik för övningar som använder ett PeriodiskaSystemet och en GUI-instans.

    Objektet håller träningsläge, antal försök, aktuell fråga och referenser till GUI och system.
    """
    def __init__(self, system, gui):
        """Initierar träningsobjektet.

        Parametrar:
            system: Instans av PeriodiskaSystemet som innehåller atomdata.
            gui: GUI-instans som används för att visa frågor och resultat.
        """
        self.system = system
        self.gui = gui
        self.försök_kvar = 3
        self.aktuell_lista = None
        self.rätt_atom = None
        self.återstående_atomer = None

    def starta_träning(self, träningstyp):
        """Startar en träningssession av angiven typ.

        Parametrar:
            träningstyp: Sträng som anger läge ('atomlista','atomnummer','beteckning','namn','massa','position').
        Funktionen initierar interna strukturer beroende på valt läge och visar första frågan eller listan.
        """
        self.träningstyp = träningstyp
        if träningstyp == 'atomlista':
            self.träna_på_alla_atomer()
        elif träningstyp == 'position':
            self.gui.position_läge()
            full_atom = [a for a in self.system.atomer if a.period is not None and a.grupp is not None]
            self.återstående_atomer = full_atom[:]
            self.ny_fråga()
        else:
            self.ny_fråga()

    def träna_på_alla_atomer(self):
        """Genererar och visar en textlista över alla atomer sorterade efter atomnummer.

        Listan skickas till GUI:t via gui.visa_alla_atomer.
        """
        atomlist = sorted(self.system.atomer, key=lambda x: x.atomnummer)
        text = ""
        for atom in atomlist:
            text += f"{atom.beteckning} | {atom.namn} | {atom.atomnummer} | {atom.massa} | {atom.period} | {atom.grupp}\n"
        self.gui.visa_alla_atomer(text)
        self.gui.visa_sökt_atom()

    def ny_fråga(self):
        """Förbereder och visar nästa fråga beroende på aktuellt träningsläge.

        Funktionen väljer slumpmässigt en Atom eller en lista av alternativ och anropar passande GUI-metod.
        """
        self.försök_kvar = 3
        if self.träningstyp == 'position':
            if not self.återstående_atomer:
                self.gui.tabell_ifylld()
                return
            self.rätt_atom = random.choice(self.återstående_atomer)
            self.gui.visa_position_fråga(f"Vilken period och grupp tillhör {self.rätt_atom.namn} ({self.rätt_atom.beteckning})")
        else:
            self.aktuell_lista = random.sample(self.system.atomer, 3)
            self.rätt_atom = random.choice(self.aktuell_lista)
            if self.träningstyp == 'atomnummer':
                self.gui.visa_fråga(f"Vilket atomnummer har {self.rätt_atom.namn} ({self.rätt_atom.beteckning})",
                                       [str(atom.atomnummer) for atom in self.aktuell_lista])
            elif self.träningstyp == 'beteckning':
                self.gui.visa_fråga(f"Vilken beteckning har {self.rätt_atom.namn}",
                                       [atom.beteckning for atom in self.aktuell_lista])
            elif self.träningstyp == 'namn':
                self.gui.visa_fråga(f"Vilket namn har grundämnet med beteckningen ({self.rätt_atom.beteckning})",
                                       [atom.namn for atom in self.aktuell_lista])
            elif self.träningstyp == 'massa':
                self.gui.visa_fråga(f"Vilken atommassa har {self.rätt_atom.namn} ({self.rätt_atom.beteckning})",
                                       [str(atom.massa) for atom in self.aktuell_lista])

    def checka_svar(self, val):
        """Kontrollerar svaret från användaren för icke-position-lägen och hanterar poäng/fel.

        Parametrar:
            val: Sträng som representerar användarens val (för position-delegation skickas detta vidare).
        Returnerar True vid korrekt svar, False annars.
        """
        if self.träningstyp == 'position':
            return self.checka_position_svar(val)
        else:
            rätt_svar = None
            if self.träningstyp == 'atomnummer':
                rätt_svar = str(self.rätt_atom.atomnummer)
            elif self.träningstyp == 'beteckning':
                rätt_svar = self.rätt_atom.beteckning
            elif self.träningstyp == 'namn':
                rätt_svar = self.rätt_atom.namn
            elif self.träningstyp == 'massa':
                rätt_svar = str(self.rätt_atom.massa)

            if val == rätt_svar:
                messagebox.showinfo("Rätt!", "Rätt Svar")
                self.ny_fråga()
                return True
            else:
                self.försök_kvar -= 1
                if self.försök_kvar > 0:
                    messagebox.showerror("Fel", f"Fel Svar. Försök kvar: {self.försök_kvar}")
                else:
                    messagebox.showerror("Fel", f"Inga fler försök. Rätt svar är {rätt_svar}")
                    self.gui.fråga_om_fortsätt()
                return False

    def checka_position_svar(self, svar):
        """Kontrollerar användarens svar för position-frågor (period, grupp) och uppdaterar tabellen.

        Parametrar:
            svar: Sträng i formatet 'period,grupp' (t.ex. '2,8').
        Returnerar True om korrekt, False annars; visar lämpliga meddelanden vid felformat eller slut på försök.
        """
        try:
            period, grupp = map(int, svar.split(','))
            if period == self.rätt_atom.period and grupp == self.rätt_atom.grupp:
                messagebox.showinfo("Rätt!", "Rätt Svar")
                self.återstående_atomer.remove(self.rätt_atom)
                self.gui.uppdatera_tabell(self.rätt_atom)
                self.ny_fråga()
                return True
            else:
                self.försök_kvar -= 1
                if self.försök_kvar > 0:
                    messagebox.showerror("Fel", f"Fel Svar. Försök kvar: {self.försök_kvar}")
                else:
                    messagebox.showerror("Fel", f"Inga fler försök. Rätt svar är Period: {self.rätt_atom.period}, Grupp: {self.rätt_atom.grupp}")
                    self.gui.uppdatera_tabell(self.rätt_atom)
                    self.återstående_atomer.remove(self.rätt_atom)
                    self.ny_fråga()
                return False
        except Exception:
            messagebox.showerror("Ogiltig", "Ange period och grupp som siffror, separerade med kommatecken (t.ex. 1,1)")
            return False

class GUI:
    """Grafiskt gränssnitt för att interagera med Träning-objektet och visa periodiska systemet.

    GUI-exponering sker via metoder som visar frågor, listor och uppdaterar tabellen.
    """
    def __init__(self, rot, träning):
        """Initierar GUI-komponenter och visar huvudmenyn.

        Parametrar:
            rot: Tk-root-fönstret.
            träning: Träning-instans som GUI:t kommer att styra.
        """
        self.rot = rot
        self.träning = träning
        self.nuvarande_frame = None
        self.periodiska_systemet_frame = None
        self.periodiska_systemet_labels = None
        self.fråga_frame = None
        self.visa_huvudmeny()

    def rensa_frame(self):
        """Rensar nuvarande frame och skapar ett nytt huvudframe där nya widgets placeras."""
        if self.nuvarande_frame:
            self.nuvarande_frame.destroy()
        self.nuvarande_frame = Frame(self.rot)
        self.nuvarande_frame.pack(pady=20)

    def rensa_fråga_frame(self):
        """Tar bort det specifika fråga-frame om det finns, så nytt fråga-frame kan skapas."""
        if self.fråga_frame:
            self.fråga_frame.destroy()
        self.fråga_frame = None

    def visa_huvudmeny(self):
        """Visar huvudmenyn med val för olika träningslägen och återställer periodiska systemets vy."""
        self.rot.title("Periodiska Systemet Träning")
        self.rensa_frame()
        self.återställ_periodiska_systemet()
        Label(self.nuvarande_frame, text="Välj träningsläge:", font=("Century Gothic", 14)).pack(pady=10)

        knappar = [
            ("1. Visa alla atomer", 'atomlista'),
            ("2. Träna på atomnummer", 'atomnummer'),
            ("3. Träna på atombeteckningar", 'beteckning'),
            ("4. Träna på atomnamn", 'namn'),
            ("5. Träna på atommassor", 'massa'),
            ("6. Träna på atompositioner", 'position'),
            ("7. Avsluta", 'lämna')
        ]

        for text, läge in knappar:
            ttk.Button(self.nuvarande_frame, text=text, command=lambda m=läge: self.välj_läge(m)).pack(pady=5)

    def återställ_periodiska_systemet(self):
        """Tar bort eventuell befintlig periodisk system-tabell från GUI:t och återställer referenser."""
        if self.periodiska_systemet_frame:
            self.periodiska_systemet_frame.destroy()
            self.periodiska_systemet_frame = None
            self.periodiska_systemet_labels = None

    def välj_läge(self, läge):
        """Anropas när användaren väljer ett menyalternativ; antingen avslutas programmet eller startar träning.
        Parametrar:
            läge: Sträng motsvarande träningsläge.
        """
        if läge == 'lämna':
            self.rot.quit()
        else:
            self.träning.starta_träning(läge)

    def visa_alla_atomer(self, text):
        """Visar en scrollbar-text med alla atomer (texten genereras av Träning.träna_på_alla_atomer)."""
        self.rensa_frame()
        Label(self.nuvarande_frame, text="Alla atomer:", font=("Century Gothic", 14)).pack(pady=10)
        st = scrolledtext.ScrolledText(self.nuvarande_frame, width=60, height=20)
        st.insert(INSERT, text)
        st.pack()
        ttk.Button(self.nuvarande_frame, text="Tillbaka till meny", command=self.visa_huvudmeny).pack(pady=10)

    def visa_sökt_atom(self):
        """Öppnar ett nytt fönster som låter användaren söka en atom efter namn eller beteckning."""

        sök_fönster = Toplevel(self.rot)
        sök_fönster.title("Sök atom")
        Label(sök_fönster, text="Ange ett grundämne (namn eller beteckning):").pack(pady=10)
        entry = ttk.Entry(sök_fönster)
        entry.pack()

        def sök():
            atom = self.träning.system.hitta_atom(entry.get().strip())
            if atom:
                info = f"{atom.beteckning} | {atom.namn} | {atom.atomnummer} | {atom.massa} | {atom.period} | {atom.grupp}"
                messagebox.showinfo("Atom Info", info)
            else:
                messagebox.showerror("Error", "Den sökta atomen finns inte")
            sök_fönster.destroy()
            self.träning.träna_på_alla_atomer()

        ttk.Button(sök_fönster, text="Sök", command=sök).pack(pady=10)

    def visa_fråga(self, fråga, alternativ):
        """Visar en flervalsfråga med knappar för varje alternativ.
        Parametrar:
            fråga: Textsträng med frågetext.
            alternativ: Lista med strängar som representerar val; vid klick skickas valet till träning.checka_svar.
        """
        self.rensa_frame()
        Label(self.nuvarande_frame, text=fråga, font=("Century Gothic", 12), wraplength=400).pack(pady=10)
        for i, opt in enumerate(alternativ, 1):
            ttk.Button(self.nuvarande_frame, text=f"{opt}", command=lambda o=opt: self.träning.checka_svar(o)).pack(pady=5)
        ttk.Button(self.nuvarande_frame, text="Avsluta", command=self.visa_huvudmeny).pack(pady=10)

    def skapa_periodiskt_system(self):
        """Skapar en tom visuell tabell (7x18) för periodiska systemets positioner och returnerar frame.

        Returnerar:
            tabell_frame: Frame som innehåller label-celler som senare kan uppdateras med beteckningar.
        """
        tabell_frame = Frame(self.nuvarande_frame)
        self.periodiska_systemet_labels = [[None for _ in range(18)] for _ in range(7)]
        for row in range(7):
            for col in range(18):
                label = Label(tabell_frame, text="", borderwidth=1, relief="solid", width=5, height=2, font=("Britannic Bold", 8))
                label.grid(row=row, column=col, padx=1, pady=1)
                self.periodiska_systemet_labels[row][col] = label
        for col in range(18):
            Label(tabell_frame, text=str(col+1), font=("Britannic Bold", 8)).grid(row=7, column=col)
        for row in range(7):
            Label(tabell_frame, text=str(row+1), font=("Britannic Bold", 8)).grid(row=row, column=18)
        return tabell_frame

    def position_läge(self):
        """Sätter upp vy för positionsträning genom att skapa och visa en tom periodisk tabell i GUI:t."""
        self.rensa_frame()
        self.periodiska_systemet_frame = self.skapa_periodiskt_system()
        self.periodiska_systemet_frame.pack(side=LEFT, padx=10)

    def visa_position_fråga(self, fråga):
        """Visar ett inmatningsfält för att svara med 'period,grupp' bredvid tabellen.

        Parametrar:
            fråga: Textsträng som beskriver vilken atom som ska positioneras.
        """
        self.rensa_fråga_frame()
        self.fråga_frame = Frame(self.nuvarande_frame)
        self.fråga_frame.pack(side=RIGHT, padx=10)
        Label(self.fråga_frame, text=fråga, font=("Century Gothic", 12), wraplength=400).pack(pady=10)
        Label(self.fråga_frame, text="Ange period,grupp (t.ex. 1,1):").pack()
        entry = ttk.Entry(self.fråga_frame)
        entry.pack()
        ttk.Button(self.fråga_frame, text="Svara", command=lambda: self.träning.checka_svar(entry.get().strip())).pack(pady=5)
        ttk.Button(self.fråga_frame, text="Avsluta", command=self.visa_huvudmeny).pack(pady=10)

    def uppdatera_tabell(self, atom):
        """Fyller i en cell i den periodiska tabellen med atomens beteckning om period och grupp finns.

        Parametrar:
            atom: Atom-objekt vars beteckning ska visas på rätt position i tabellen.
        """
        if atom.period is not None and atom.grupp is not None:
            row = atom.period - 1
            col = atom.grupp - 1
            if 0 <= row < 7 and 0 <= col < 18:
                self.periodiska_systemet_labels[row][col].config(text=atom.beteckning)

    def tabell_ifylld(self):
        """Visar ett meddelande när hela tabellen är ifylld och frågar användaren om de vill fortsätta."""
        messagebox.showinfo("Grattis!", "Du har fyllt i hela periodiska systemet!")
        self.fråga_om_fortsätt()

    def fråga_om_fortsätt(self):
        """Frågar användaren om de vill fortsätta och återställer eller avslutar beroende på svar och läge."""
        if self.träning.träningstyp == 'position' and not self.träning.återstående_atomer:
            if messagebox.askyesno("Fortsätt?", "Vill du fortsätta spela?"):
                full_atom = [a for a in self.träning.system.atomer if a.period is not None and a.grupp is not None]
                self.träning.återstående_atomer = full_atom[:]
                self.återställ_periodiska_systemet()
                self.position_läge()
                self.träning.ny_fråga()
            else:
                self.visa_huvudmeny()
        else:
            if messagebox.askyesno("Fortsätt?", "Vill du fortsätta spela?"):
                if self.träning.träningstyp == 'atomlista':
                    self.träning.träna_på_alla_atomer()
                else:
                    self.träning.ny_fråga()
            else:
                self.visa_huvudmeny()

def main():
    """Skapar huvudfönster, initierar PeriodiskaSystemet, Träning och GUI och startar huvudloopen."""
    rot = Tk()
    p_s = PeriodiskaSystemet()
    träning = Träning(p_s, None)
    gui = GUI(rot, träning)
    träning.gui = gui
    rot.mainloop()

if __name__ == '__main__':
    main()