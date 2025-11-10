import sys
from console import Console
from player import PlayerReader, PlayerStats

def main():
    try:
        con = Console(PlayerReader, PlayerStats)
        con.mainloop()
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit(0)

if __name__ == '__main__':
    main()
