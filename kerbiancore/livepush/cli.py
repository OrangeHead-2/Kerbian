"""
LivePush CLI Management

- upload, promote, rollback, inspect, monitor
"""

import argparse
import sys
from kerbiancore.livepush.server import LivePushServer

def main():
    parser = argparse.ArgumentParser(description="KerbianCore LivePush CLI")
    parser.add_argument("cmd", choices=["upload", "promote", "rollback", "inspect", "monitor"], help="Command")
    parser.add_argument("--token", required=True, help="API token")
    parser.add_argument("--bundle", help="Bundle file path")
    parser.add_argument("--version", help="Version string")
    parser.add_argument("--storage", default="livepush_bundles", help="Bundle storage directory")
    parser.add_argument("--secret", default="changeme", help="Admin/secret key")
    parser.add_argument("--target", help="Target version for rollback/promote")
    args = parser.parse_args()

    server = LivePushServer(args.storage, args.secret.encode("utf-8"))

    if args.cmd == "upload":
        if not args.bundle or not args.version:
            print("Must specify --bundle and --version")
            sys.exit(1)
        server.upload_bundle(args.token, args.bundle, args.version)
        print(f"Uploaded version {args.version}")

    elif args.cmd == "rollback":
        if not args.target:
            print("Must specify --target")
            sys.exit(1)
        ok = server.rollback(args.token, args.target)
        print("Rollback to", args.target, "success" if ok else "failed")

    elif args.cmd == "inspect":
        latest = server.get_latest_version()
        print("Latest:", latest)

    elif args.cmd == "monitor":
        print("Monitoring not implemented in CLI (see monitor.py)")

    elif args.cmd == "promote":
        print("Promote not implemented in this version")

if __name__ == "__main__":
    main()