"""
Module de monitoring pour les pipelines Spark
"""
import time
from typing import Dict, Any
from pyspark.sql import DataFrame, SparkSession
from datetime import datetime


class PipelineMonitor:
    """Classe pour monitorer les pipelines Spark"""
    
    def __init__(self, job_name: str):
        self.job_name = job_name
        self.start_time = time.time()
        self.metrics: Dict[str, Any] = {
            "job_name": job_name,
            "start_time": datetime.now().isoformat(),
        }
    
    def log_dataframe_stats(self, df: DataFrame, step: str) -> None:
        """Log les statistiques d'un DataFrame"""
        row_count = df.count()
        col_count = len(df.columns)
        
        print(f"\n{'='*60}")
        print(f"📊 STATISTIQUES - {step}")
        print(f"{'='*60}")
        print(f"🔢 Nombre de lignes    : {row_count:,}")
        print(f"📋 Nombre de colonnes  : {col_count}")
        print(f"📁 Colonnes            : {', '.join(df.columns)}")
        print(f"{'='*60}\n")
        
        self.metrics[f"{step}_row_count"] = row_count
        self.metrics[f"{step}_col_count"] = col_count
    
    def log_read_stats(self, df: DataFrame, source_path: str) -> None:
        """Log les stats de lecture"""
        print(f"\n📖 LECTURE depuis : {source_path}")
        self.log_dataframe_stats(df, "READ")
    
    def log_write_stats(self, row_count: int, output_path: str, format_type: str = "parquet") -> None:
        """Log les stats d'écriture"""
        elapsed = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print(f"✅ ÉCRITURE TERMINÉE")
        print(f"{'='*60}")
        print(f"📂 Destination         : {output_path}")
        print(f"📦 Format              : {format_type}")
        print(f"🔢 Lignes écrites      : {row_count:,}")
        print(f"⏱️  Durée totale        : {elapsed:.2f} secondes")
        print(f"{'='*60}\n")
        
        self.metrics["output_path"] = output_path
        self.metrics["format"] = format_type
        self.metrics["total_rows"] = row_count
        self.metrics["duration_seconds"] = round(elapsed, 2)
        self.metrics["end_time"] = datetime.now().isoformat()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retourne toutes les métriques collectées"""
        return self.metrics
    
    def print_summary(self) -> None:
        """Affiche un résumé final"""
        elapsed = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print(f"🎯 RÉSUMÉ DU JOB: {self.job_name}")
        print(f"{'='*60}")
        print(f"⏱️  Durée totale        : {elapsed:.2f}s")
        if "total_rows" in self.metrics:
            print(f"🔢 Lignes traitées     : {self.metrics['total_rows']:,}")
            throughput = self.metrics['total_rows'] / elapsed if elapsed > 0 else 0
            print(f"⚡ Débit               : {throughput:,.0f} lignes/sec")
        print(f"{'='*60}\n")
