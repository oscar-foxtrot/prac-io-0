import unittest
import numpy as np

from antagonsitic_game.matrix_game import nash_equilibrium

class TestNash(unittest.TestCase):
    
    # Матрица из примера преподавателя практикума
    def test_1st_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[4, 0, 6, 2, 2, 1],
                [3, 8, 4, 10, 4, 4],
                [1, 2, 6, 5, 0, 0],
                [6, 6, 4, 4, 10, 3],
                [10, 4, 6, 4, 0, 9],
                [10, 7, 0, 7, 9, 8]]
                ))
        self.assertAlmostEqual(game_res[0], 151/31, places=5)
        np.testing.assert_array_almost_equal(
            game_res[1], np.array([0, 4/31, 3/31, 27/62, 21/62, 0]), decimal=4)
        np.testing.assert_array_almost_equal(
            game_res[2], np.array([0, 0, 257/372, 9/62, 55/372, 1/62]), decimal=4)
    
    
    # Матрица с [единственной] седловой точкой
    def test_2nd_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[6, 5],
                 [5, 4]]
                ))
        self.assertAlmostEqual(game_res[0], 5, places=5)
        np.testing.assert_array_almost_equal(game_res[1], 
                                                  np.array([1, 0]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([0, 1]), decimal=4)
        
    def test_3rd_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[-2, -1],
                 [1, 0]]
                ))
        self.assertAlmostEqual(game_res[0], 0, places=5)
        np.testing.assert_array_almost_equal(game_res[1], 
                                                  np.array([0, 1]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([0, 1]), decimal=4)
    
    
    def test_4th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[1, 0],
                 [1, 0]]
                ))
        self.assertAlmostEqual(game_res[0], 0, places=5)
        condition = np.allclose(game_res[1], np.array([0, 1]), rtol=1e-05) or \
            np.allclose(game_res[1], np.array([1, 0]), rtol=1e-05) or \
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([0, 1]), decimal=4)
        self.assertEqual(condition, True)
        
        
    def test_5th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[1, 2],
                 [3, 4],
                 [3, 4],
                 [2, 1]]
                ))
        self.assertAlmostEqual(game_res[0], 3, places=5)
        first_condition = np.allclose(game_res[1], 
                                      np.array([0, 1, 0, 0]), rtol=1e-05) or \
            np.allclose(game_res[1], np.array([0, 0, 1, 0]), rtol=1e-05) 
        self.assertEqual(first_condition, True)
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([1, 0]), decimal=4)


    # Матрица из примера 5.4 на 
    # с. 49 книги "Введение в теорию игр" - А.А. Васин, В.В. Морозов
    def test_6th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[1, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [0, 1, 0, 0, 1],
                [0, 0, 1, 1, 1]]
                ))
        self.assertAlmostEqual(game_res[0], 1/2, places=5)   
        condition_one = np.allclose(game_res[1], 
                                    np.array([1/2, 0, 0, 1/2]), rtol=1e-05) or \
            np.allclose(game_res[1], np.array([1/4, 1/4, 1/4, 1/4]), rtol=1e-05)
        condition_two = np.allclose(game_res[2], 
                                    np.array([1/2, 0, 0, 0, 1/2]), rtol=1e-05) or \
            np.allclose(game_res[2], np.array([0, 1/2, 0, 1/2, 0]), rtol=1e-05)
        self.assertEqual(condition_one, True)   
        self.assertEqual(condition_two, True) 
    
    
    # Матрица из примера 5.5 на 
    # с. 57 книги "Введение в теорию игр" - А.А. Васин, В.В. Морозов
    def test_7th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[2, 1, 0],
                [2, 0, 3],
                [-1, 3, -3]]
                ))
        self.assertAlmostEqual(game_res[0], 1, places=5)  
        condition = np.allclose(game_res[2], np.array([0, 2/3, 1/3]), rtol=1e-05) or \
            np.allclose(game_res[2], np.array([1/5, 3/5, 1/5]), rtol=1e-05)
        self.assertEqual(condition, True)   
        np.testing.assert_array_almost_equal(game_res[1], 
                                                  np.array([0, 2/3, 1/3]), decimal=4)
    
    
    # Камень-ножница-бумага
    def test_8th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[0, 1, -1],
                [-1, 0, 1],
                [1, -1, 0]]
                ))
        self.assertAlmostEqual(game_res[0], 0, places=5)  
        np.testing.assert_array_almost_equal(game_res[1], 
                                                  np.array([1/3, 1/3, 1/3]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([1/3, 1/3, 1/3]), decimal=4)
    
    
    # Матрица из примера 5.1 на 
    # с. 39 книги "Введение в теорию игр" - А.А. Васин, В.В. Морозов
    def test_9th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[3, 1, 5],
                [1, 3, 3],
                [2, 2, 1]]
                ))
        self.assertAlmostEqual(game_res[0], 2, places=5) 
        condition = np.allclose(game_res[1], np.array([1/2, 1/2, 0]), rtol=1e-05) or \
            np.allclose(game_res[1], np.array([1/6, 1/6, 2/3]), rtol=1e-05)
        self.assertEqual(condition, True)  
        np.testing.assert_array_almost_equal(game_res[2], 
                                                  np.array([1/2, 1/2, 0]), decimal=4)
    
    
    # Матрица из статьи http://bit.ly/49KnEc7
    # Конкуренция на рынке олигополии
    def test_10th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[10, -2, -4],
                [6, 3, -5],
                [-8, 4, 2],
                [3, -9, 7]]
                ))
        self.assertAlmostEqual(game_res[0], 9/23, places=5) 
        np.testing.assert_array_almost_equal(game_res[1], 
                                      np.array([0, 28/69, 8/23, 17/69]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                      np.array([16/69, 49/138, 19/46]), decimal=4)
        
        
    # Матрица из статьи http://bit.ly/49KnEc7
    # Антагонистические интересы налогоплательщиков и налоговых органов
    def test_11th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[8, 3, 4],
                [6, 5, 7],
                [4, 7, 6],
                [3, 10, 2]]
                ))
        self.assertAlmostEqual(game_res[0], 91/16, places=5) 
        np.testing.assert_array_almost_equal(game_res[1], 
                                      np.array([1/8, 11/16, 0, 3/16]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                      np.array([25/48, 19/48, 1/12]), decimal=4)
        
        
    # Матрица из статьи https://bit.ly/3SCxeHU - Presh Talwalkar
    # Blotto game
    def test_12th_game(self):
        game_res = nash_equilibrium(
            np.array(
                [[4, 0, 2, 1],
                [0, 4, 1, 2],
                [1, -1, 3, 0],
                [-1, 1, 0, 3],
                [-2, -2, 2, 2]]
                ))
        self.assertAlmostEqual(game_res[0], 14/9, places=5) 
        np.testing.assert_array_almost_equal(game_res[1], 
                                      np.array([4/9, 4/9, 0, 0, 1/9]), decimal=4)
        np.testing.assert_array_almost_equal(game_res[2], 
                                      np.array([1/30, 7/90, 8/15, 16/45]), decimal=4)
        
    
if __name__ == "__main__":
  unittest.main()