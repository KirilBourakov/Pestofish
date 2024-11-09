import unittest
from engine.tests.moves_tests import MovesTests
from engine.tests.generator_tests import GeneratorTests
from engine.tests.engine_result_tests import EngineResultTests
from engine.tests.engine_value_tests import EngineValueTests

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MovesTests))
    suite.addTest(unittest.makeSuite(GeneratorTests))
    suite.addTest(unittest.makeSuite(EngineResultTests))
    suite.addTest(unittest.makeSuite(EngineValueTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')