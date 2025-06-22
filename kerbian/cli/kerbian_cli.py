import click
from kerbian.cli.commands.init import init_project
from kerbian.cli.commands.build import build_project
from kerbian.cli.commands.run import run_app
from kerbian.cli.commands.bundle import bundle_app

@click.group()
def main():
    """Kerbian CLI - Cross-platform mobile framework for Python."""
    pass

@main.command()
@click.argument('path')
def init(path):
    """Initialize a new Kerbian project."""
    init_project(path)

@main.command()
def build():
    """Build the current Kerbian project."""
    build_project()

@main.command()
@click.option('--platform', type=click.Choice(['android', 'ios']), default='android')
def run(platform):
    """Run the Kerbian app on emulator/device."""
    run_app(platform)

@main.command()
def bundle():
    """Create a production-ready bundle."""
    bundle_app()

@main.command()
def doctor():
    """Check environment and dependencies for common issues."""
    # Diagnostic checks for Python version, dependencies, platform tools, etc.
    print("Checking environment...")
    # Add more diagnostics here

if __name__ == "__main__":
    main()