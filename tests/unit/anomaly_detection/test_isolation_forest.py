import unittest
import numpy as np
import pandas as pd
from anomaly_detection.models.isolation_forest import AnomalyDetector

class TestIsolationForest(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset for testing
        np.random.seed(42)
        self.normal_data = np.random.normal(0, 1, (100, 5))
        self.anomaly_data = np.random.normal(5, 1, (10, 5))
        self.test_data = np.vstack([self.normal_data, self.anomaly_data])
        self.feature_names = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5']
        self.df = pd.DataFrame(self.test_data, columns=self.feature_names)
        
        # Initialize the model
        self.model = AnomalyDetector()
        
    def test_model_initialization(self):
        """Test if the model initializes correctly"""
        self.assertFalse(self.model.is_fitted)
        self.assertIsNone(self.model.model)
        
    def test_model_fit(self):
        """Test if the model fits correctly"""
        self.model.fit(self.df, feature_names=self.feature_names)
        self.assertTrue(self.model.is_fitted)
        self.assertIsNotNone(self.model.model)
        
    def test_predict(self):
        """Test if the model predicts correctly"""
        self.model.fit(self.df, feature_names=self.feature_names)
        predictions = self.model.predict(self.df)
        
        # Check if predictions have the right shape
        self.assertEqual(len(predictions), len(self.df))
        
        # Check if predictions are binary (0 or 1)
        self.assertTrue(all(p in [0, 1] for p in predictions))
        
    def test_anomaly_score(self):
        """Test if the model calculates anomaly scores correctly"""
        self.model.fit(self.df, feature_names=self.feature_names)
        scores = self.model.anomaly_score(self.df)
        
        # Check if scores have the right shape
        self.assertEqual(len(scores), len(self.df))
        
        # Check if scores are between 0 and 1
        self.assertTrue(all(0 <= s <= 1 for s in scores))
        
    def test_save_load_model(self):
        """Test if the model can be saved and loaded correctly"""
        self.model.fit(self.df, feature_names=self.feature_names)
        
        # Save the model to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.joblib') as tmp:
            filepath = tmp.name
            self.model.save_model(filepath)
            
            # Load the model
            loaded_model = AnomalyDetector.load_model(filepath)
            
            # Check if the loaded model is fitted
            self.assertTrue(loaded_model.is_fitted)
            
            # Check if predictions from both models match
            original_preds = self.model.predict(self.df)
            loaded_preds = loaded_model.predict(self.df)
            np.testing.assert_array_equal(original_preds, loaded_preds)

if __name__ == '__main__':
    unittest.main()