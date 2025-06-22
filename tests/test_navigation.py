import unittest
from kerbian.navigation.router import Router

class TestRouter(unittest.TestCase):
    def test_navigation_stack(self):
        router = Router()
        router.register("/home", lambda: "home")
        router.navigate("/home")
        self.assertEqual(len(router.stack), 1)
        router.register("/settings", lambda: "settings")
        router.navigate("/settings")
        self.assertEqual(len(router.stack), 2)
        router.go_back()
        self.assertEqual(len(router.stack), 1)