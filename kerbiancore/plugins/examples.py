from kerbiancore.plugins.ecosystem import Plugin, PluginManager

def say_hello(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

if __name__ == "__main__":
    mgr = PluginManager()
    hello_plugin = Plugin("hello", "1.0", "Simple hello plugin", "dev", say_hello)
    add_plugin = Plugin("adder", "1.0", "Adds two numbers", "dev", add)
    mgr.register(hello_plugin)
    mgr.register(add_plugin)
    print(mgr.run("hello", "World"))
    print(mgr.run("adder", 3, 4))
    print("All plugins:", mgr.list_plugins())