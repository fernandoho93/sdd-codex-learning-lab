import unittest

from prompt_lab.providers import FakeProvider


class FakeProviderTests(unittest.TestCase):
    def test_same_prompt_always_produces_same_result(self) -> None:
        provider = FakeProvider()
        first = provider.generate("o que é SDD?")
        second = provider.generate("o que é SDD?")
        self.assertEqual(first, second)
        self.assertEqual("fake", first.provider)
        self.assertEqual("deterministic-study-v1", first.model)


if __name__ == "__main__":
    unittest.main()
