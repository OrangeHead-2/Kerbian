import sys

def main():
    print("KerbianCore CLI")
    print("Usage:")
    print("  kerbiancore version         # Show version")
    print("  kerbiancore help            # Show help")
    print("  kerbiancore test            # Run tests (example)")
    print("  kerbiancore plugins         # List plugins (example)")
    print("  kerbiancore build           # Build project (example)")
    from kerbiancore import version
    if len(sys.argv) < 2:
        print("No command given.")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "version":
        print(f"KerbianCore version: {version.__version__}")
    elif cmd == "help":
        print("See https://github.com/kerbiancore/kerbiancore for docs.")
    elif cmd == "test":
        print("Running sample tests...")
        # Here you might hook into kerbiancore.testing.core
    elif cmd == "plugins":
        print("Listing plugins...")
        # Here you might hook into kerbiancore.plugins.ecosystem
    elif cmd == "build":
        print("Build not implemented in CLI demo.")
    else:
        print("Unknown command:", cmd)
        sys.exit(2)