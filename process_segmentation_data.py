"""
Customer Segmentation & Churn Risk ML Pipeline
Author: Ayush Kumar
"""

import os
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("SegmentationPipeline")


class CustomerSegmentationML:
    """Production Feature Engineering and K-Means Clustering Pipeline."""

    def __init__(self, data_path: str = "customer_segments.csv"):
        self.data_path = data_path
        self.df = None
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        self.pca = PCA(n_components=2, random_state=42)

    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Source file {self.data_path} not found.")
        logger.info(f"Loading customer segment dataset from {self.data_path}...")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} customer records.")
        return self.df

    def engineer_features(self) -> pd.DataFrame:
        logger.info("Executing log transformations and feature normalization...")
        # Handle skewness with log transformations
        self.df["Recency_Log"] = np.log1p(self.df["Recency"])
        self.df["Frequency_Log"] = np.log1p(self.df["Frequency"])
        self.df["Monetary_Log"] = np.log1p(np.maximum(self.df["Monetary"], 0))

        # Churn Probability Risk Index Rule: high recency + low frequency
        max_rec = self.df["Recency"].max() if self.df["Recency"].max() > 0 else 1
        rec_norm = self.df["Recency"] / max_rec
        freq_norm = 1.0 / (1.0 + self.df["Frequency"])
        self.df["Churn_Risk_Score"] = np.round((0.65 * rec_norm + 0.35 * freq_norm) * 100, 2)

        self.df["Churn_Risk_Category"] = pd.cut(
            self.df["Churn_Risk_Score"],
            bins=[-1, 35, 65, 100],
            labels=["Low Risk", "Medium Risk", "High Risk / Churned"]
        )
        return self.df

    def fit_clusters(self) -> pd.DataFrame:
        logger.info("Training K-Means (k=4) and executing PCA dimensionality reduction...")
        features = ["Recency_Log", "Frequency_Log", "Monetary_Log"]
        scaled_features = self.scaler.fit_transform(self.df[features])

        self.df["Cluster"] = self.kmeans.fit_predict(scaled_features)

        # Map cluster labels to business personas
        cluster_summary = self.df.groupby("Cluster")["Monetary"].mean()
        rank_map = {cluster: rank for rank, cluster in enumerate(cluster_summary.sort_values(ascending=False).index)}
        persona_names = {
            0: "VIP Champions",
            1: "Loyal High-Spenders",
            2: "Potential Loyalists",
            3: "At-Risk / Inactive"
        }
        self.df["ML_Cluster_Persona"] = self.df["Cluster"].map(rank_map).map(persona_names)

        # PCA Projection
        pca_coords = self.pca.fit_transform(scaled_features)
        self.df["PCA1"] = np.round(pca_coords[:, 0], 4)
        self.df["PCA2"] = np.round(pca_coords[:, 1], 4)

        logger.info(f"PCA Variance Explained: {self.pca.explained_variance_ratio_.sum() * 100:.2f}%")
        return self.df

    def save_enhanced_dataset(self, output_path: str = "customer_segments_enhanced.csv") -> None:
        self.df.to_csv(output_path, index=False)
        logger.info(f"Enhanced dataset exported to {output_path}")


if __name__ == "__main__":
    pipeline = CustomerSegmentationML()
    pipeline.load_data()
    pipeline.engineer_features()
    pipeline.fit_clusters()
    pipeline.save_enhanced_dataset()
