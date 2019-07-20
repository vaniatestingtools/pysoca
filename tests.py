import unittest
import testCoverage
#IMPORT YOUR CODE
import my_func
class TestMyFunctions(unittest.TestCase):
    def test_runner(self):
        self.assertEqual(my_func.insertionSort([1,2,3]), [1,2,3])

if __name__ == '__main__':
    unittest.main()