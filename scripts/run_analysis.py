from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CONFIG  # noqa: E402
from src.services.dashboard import DashboardService  # noqa: E402


if __name__ == "__main__":
    service = DashboardService(CONFIG)
    service.export_outputs()
    result = service.build(CONFIG.default_strategy)
    print("分析完成")
    print(f"样本量: {result['summary']['n']}")
    print(f"多重用药率: {result['summary']['polypharmacy_pct']}%")
    print(f"高营养不良风险率: {result['summary']['malnutrition_pct']}%")
    print(f"输出目录: {CONFIG.output_dir}")
