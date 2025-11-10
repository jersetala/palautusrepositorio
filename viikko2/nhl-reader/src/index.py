from console import Console
from player import PlayerReader, PlayerStats
from sys import exit

def main():
    try:
        con = Console(PlayerReader, PlayerStats)
        con.mainloop()
    except KeyboardInterrupt:
        print("\nQuitting...")
        exit(0)

if __name__ == '__main__':
    main()
