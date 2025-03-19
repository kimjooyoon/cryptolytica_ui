import sys
import random
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# 상위 디렉토리 추가
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from shared.services.base_client import BaseApiClient
from shared.models.common_models import Portfolio, AnalysisResult

class PortfolioClient(BaseApiClient):
    """포트폴리오 데이터 API 클라이언트"""
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        """
        PortfolioClient 초기화
        
        Args:
            base_url: API 기본 URL
            api_key: API 키
            ws_url: WebSocket URL
        """
        super().__init__(base_url, api_key, ws_url)
    
    def get_portfolios(self) -> List[Dict[str, Any]]:
        """
        사용자의 포트폴리오 목록을 가져옵니다.
        
        Returns:
            List[Dict[str, Any]]: 포트폴리오 목록
        """
        try:
            # 실제 API 호출 대신 데모 데이터 생성
            portfolio_count = random.randint(2, 4)
            portfolios = []
            
            for i in range(portfolio_count):
                if i == 0:
                    name = "Main Portfolio"
                    risk_level = "balanced"
                elif i == 1:
                    name = "Long-term Investments"
                    risk_level = "conservative"
                else:
                    name = f"Investment Strategy {i}"
                    risk_level = random.choice(["aggressive", "balanced", "conservative"])
                
                # 총 가치 계산
                total_value = 10000 * (10 ** random.uniform(0, 1))
                initial_value = total_value * (1 - random.uniform(-0.2, 0.3))
                
                # 수익률 계산
                roi = (total_value - initial_value) / initial_value
                
                portfolio = {
                    "id": f"port_{i}",
                    "name": name,
                    "description": f"Portfolio for {risk_level} investment strategy",
                    "risk_level": risk_level,
                    "total_value": total_value,
                    "initial_value": initial_value,
                    "roi": roi,
                    "created_at": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                portfolios.append(portfolio)
            
            return portfolios
        except Exception as e:
            self.logger.error(f"포트폴리오 목록 가져오기 실패: {str(e)}")
            return []
    
    def get_portfolio_by_id(self, portfolio_id: str) -> Optional[Dict[str, Any]]:
        """
        특정 포트폴리오 정보를 가져옵니다.
        
        Args:
            portfolio_id: 포트폴리오 ID
            
        Returns:
            Optional[Dict[str, Any]]: 포트폴리오 정보
        """
        try:
            # 모든 포트폴리오 가져와서 필터링
            portfolios = self.get_portfolios()
            for portfolio in portfolios:
                if portfolio.get("id") == portfolio_id:
                    return portfolio
            return None
        except Exception as e:
            self.logger.error(f"포트폴리오 정보 가져오기 실패: {str(e)}")
            return None
    
    def get_portfolio_assets(self, portfolio_id: str) -> List[Dict[str, Any]]:
        """
        포트폴리오 내 자산 목록을 가져옵니다.
        
        Args:
            portfolio_id: 포트폴리오 ID
            
        Returns:
            List[Dict[str, Any]]: 자산 목록
        """
        try:
            # 기본 자산 목록
            standard_assets = [
                {"symbol": "BTC", "name": "Bitcoin", "allocation": 0.4, "price": 50000},
                {"symbol": "ETH", "name": "Ethereum", "allocation": 0.3, "price": 3000},
                {"symbol": "SOL", "name": "Solana", "allocation": 0.1, "price": 100},
                {"symbol": "ADA", "name": "Cardano", "allocation": 0.05, "price": 0.6},
                {"symbol": "DOT", "name": "Polkadot", "allocation": 0.05, "price": 8},
                {"symbol": "AVAX", "name": "Avalanche", "allocation": 0.05, "price": 30},
                {"symbol": "LINK", "name": "Chainlink", "allocation": 0.03, "price": 15},
                {"symbol": "MATIC", "name": "Polygon", "allocation": 0.02, "price": 0.8}
            ]
            
            # 포트폴리오별 다른 자산 구성
            if portfolio_id == "port_0":  # Main Portfolio
                assets = standard_assets
            elif portfolio_id == "port_1":  # Long-term Investments
                assets = [
                    {"symbol": "BTC", "name": "Bitcoin", "allocation": 0.5, "price": 50000},
                    {"symbol": "ETH", "name": "Ethereum", "allocation": 0.4, "price": 3000},
                    {"symbol": "SOL", "name": "Solana", "allocation": 0.1, "price": 100}
                ]
            else:
                # 임의의 자산 구성
                asset_count = random.randint(3, 6)
                assets = []
                remaining_allocation = 1.0
                
                for i in range(asset_count):
                    if i == asset_count - 1:
                        allocation = remaining_allocation
                    else:
                        allocation = min(remaining_allocation * random.uniform(0.1, 0.5), remaining_allocation)
                        remaining_allocation -= allocation
                    
                    coin = standard_assets[i % len(standard_assets)]
                    assets.append({
                        "symbol": coin["symbol"],
                        "name": coin["name"],
                        "allocation": allocation,
                        "price": coin["price"] * (1 + random.uniform(-0.05, 0.05))
                    })
            
            # 포트폴리오 기본 정보 가져오기
            portfolio = self.get_portfolio_by_id(portfolio_id)
            if not portfolio:
                return []
            
            # 자산별 가치 계산 및 추가 정보 추가
            total_value = portfolio.get("total_value", 10000)
            result = []
            
            for asset in assets:
                asset_value = total_value * asset["allocation"]
                quantity = asset_value / asset["price"]
                
                # 손익 계산 (랜덤 데이터)
                cost_basis = asset["price"] * (1 - random.uniform(-0.2, 0.2))
                profit_loss = (asset["price"] - cost_basis) * quantity
                profit_loss_percent = (asset["price"] - cost_basis) / cost_basis
                
                result.append({
                    "symbol": asset["symbol"],
                    "name": asset["name"],
                    "quantity": quantity,
                    "price": asset["price"],
                    "value": asset_value,
                    "allocation": asset["allocation"],
                    "cost_basis": cost_basis,
                    "profit_loss": profit_loss,
                    "profit_loss_percent": profit_loss_percent,
                    "last_updated": datetime.now().isoformat()
                })
            
            return result
        except Exception as e:
            self.logger.error(f"포트폴리오 자산 가져오기 실패: {str(e)}")
            return []
    
    def get_portfolio_performance(self, portfolio_id: str, period: str = "1m") -> Dict[str, Any]:
        """
        포트폴리오 성과 데이터를 가져옵니다.
        
        Args:
            portfolio_id: 포트폴리오 ID
            period: 기간 (1d, 1w, 1m, 3m, 1y, all)
            
        Returns:
            Dict[str, Any]: 성과 데이터
        """
        try:
            # 포트폴리오 기본 정보 가져오기
            portfolio = self.get_portfolio_by_id(portfolio_id)
            if not portfolio:
                return {"error": "포트폴리오를 찾을 수 없습니다."}
            
            # 기간에 따른 데이터 포인트 설정
            now = datetime.now()
            
            if period == "1d":
                start_time = now - timedelta(days=1)
                delta = timedelta(hours=1)
                points = 24
            elif period == "1w":
                start_time = now - timedelta(weeks=1)
                delta = timedelta(hours=6)
                points = 28
            elif period == "1m":
                start_time = now - timedelta(days=30)
                delta = timedelta(days=1)
                points = 30
            elif period == "3m":
                start_time = now - timedelta(days=90)
                delta = timedelta(days=3)
                points = 30
            elif period == "1y":
                start_time = now - timedelta(days=365)
                delta = timedelta(days=12)
                points = 30
            elif period == "all":
                # 포트폴리오 생성일 사용
                start_time = datetime.fromisoformat(portfolio.get("created_at", (now - timedelta(days=365)).isoformat()))
                days_diff = (now - start_time).days
                delta = timedelta(days=max(1, days_diff // 30))
                points = min(30, days_diff)
            else:
                start_time = now - timedelta(days=30)
                delta = timedelta(days=1)
                points = 30
            
            # 성과 데이터 생성
            performance_data = []
            current_value = portfolio.get("initial_value", 10000)
            target_value = portfolio.get("total_value", current_value * 1.2)
            
            # 시작부터 현재까지 적절한 성장/하락 곡선 생성
            for i in range(points):
                timestamp = start_time + (delta * i)
                
                # 목표값까지의 진행률 계산 (0~1)
                progress = i / (points - 1)
                
                # 약간의 랜덤 변동 추가 (목표값 근처에서 수렴)
                noise = random.uniform(-0.03, 0.03) * (1 - progress)
                value_at_point = current_value + (target_value - current_value) * (progress + noise)
                
                # 데이터 포인트 추가
                performance_data.append({
                    "timestamp": timestamp.isoformat(),
                    "value": value_at_point
                })
            
            # 다양한 지표 계산
            initial_value = performance_data[0]["value"]
            final_value = performance_data[-1]["value"]
            
            absolute_return = final_value - initial_value
            percent_return = absolute_return / initial_value
            
            # 변동성 계산 (간단한 표준편차 근사값)
            values = [point["value"] for point in performance_data]
            mean_value = sum(values) / len(values)
            variance = sum((x - mean_value) ** 2 for x in values) / len(values)
            volatility = variance ** 0.5 / mean_value  # 표준편차를 평균으로 나눔
            
            # 샤프 비율 계산 (간단한 근사값)
            risk_free_rate = 0.02  # 연간 2%
            sharpe_ratio = (percent_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            # 최대 손실폭 계산
            max_drawdown = 0
            peak_value = initial_value
            
            for point in performance_data:
                current_value = point["value"]
                peak_value = max(peak_value, current_value)
                drawdown = (peak_value - current_value) / peak_value
                max_drawdown = max(max_drawdown, drawdown)
            
            return {
                "portfolio_id": portfolio_id,
                "period": period,
                "performance_data": performance_data,
                "metrics": {
                    "initial_value": initial_value,
                    "final_value": final_value,
                    "absolute_return": absolute_return,
                    "percent_return": percent_return,
                    "volatility": volatility,
                    "sharpe_ratio": sharpe_ratio,
                    "max_drawdown": max_drawdown
                },
                "updated_at": now.isoformat()
            }
        except Exception as e:
            self.logger.error(f"포트폴리오 성과 데이터 가져오기 실패: {str(e)}")
            return {"error": str(e)}
    
    def optimize_portfolio(self, assets: List[Dict[str, Any]], risk_level: str = "balanced") -> Dict[str, Any]:
        """
        자산 목록을 기반으로 최적의 포트폴리오 배분을 계산합니다.
        
        Args:
            assets: 자산 목록 (심볼, 이름 등 포함)
            risk_level: 위험 수준 (conservative, balanced, aggressive)
            
        Returns:
            Dict[str, Any]: 최적화된 포트폴리오 데이터
        """
        try:
            if not assets:
                return {"error": "자산 목록이 비어 있습니다."}
            
            # 위험 수준에 따른 기본 배분 설정
            if risk_level == "conservative":
                # 안전자산 위주 (BTC, ETH 비중 높음)
                weights = {
                    "BTC": 0.5,
                    "ETH": 0.3,
                    "large_cap": 0.15,
                    "mid_cap": 0.05,
                    "small_cap": 0.0
                }
            elif risk_level == "aggressive":
                # 고위험 자산 비중 높음
                weights = {
                    "BTC": 0.2,
                    "ETH": 0.2,
                    "large_cap": 0.2,
                    "mid_cap": 0.3,
                    "small_cap": 0.1
                }
            else:  # balanced
                # 균형 잡힌 배분
                weights = {
                    "BTC": 0.35,
                    "ETH": 0.25,
                    "large_cap": 0.2,
                    "mid_cap": 0.15,
                    "small_cap": 0.05
                }
            
            # 자산 분류
            asset_categories = {
                "BTC": [],
                "ETH": [],
                "large_cap": [],  # Top 10
                "mid_cap": [],    # Top 10-50
                "small_cap": []   # Top 50+
            }
            
            for asset in assets:
                symbol = asset.get("symbol", "")
                if symbol == "BTC":
                    asset_categories["BTC"].append(asset)
                elif symbol == "ETH":
                    asset_categories["ETH"].append(asset)
                elif symbol in ["BNB", "SOL", "XRP", "ADA", "DOGE", "DOT", "AVAX"]:
                    asset_categories["large_cap"].append(asset)
                elif symbol in ["LINK", "MATIC", "UNI", "ATOM", "ALGO", "XLM"]:
                    asset_categories["mid_cap"].append(asset)
                else:
                    asset_categories["small_cap"].append(asset)
            
            # 각 카테고리 내에서 자산 배분
            allocated_assets = []
            
            for category, category_assets in asset_categories.items():
                if not category_assets:
                    continue
                
                category_weight = weights[category]
                asset_weight = category_weight / len(category_assets)
                
                for asset in category_assets:
                    allocated_assets.append({
                        "symbol": asset.get("symbol"),
                        "name": asset.get("name"),
                        "allocation": asset_weight,
                        "category": category
                    })
            
            # 예상 성과 지표 계산
            expected_return = 0
            expected_volatility = 0
            
            # 카테고리별 예상 수익률 및 변동성
            category_metrics = {
                "BTC": {"return": 0.15, "volatility": 0.65},
                "ETH": {"return": 0.25, "volatility": 0.75},
                "large_cap": {"return": 0.3, "volatility": 0.85},
                "mid_cap": {"return": 0.4, "volatility": 1.0},
                "small_cap": {"return": 0.5, "volatility": 1.2}
            }
            
            for category, weight in weights.items():
                if weight > 0:
                    expected_return += category_metrics[category]["return"] * weight
                    expected_volatility += category_metrics[category]["volatility"] * weight
            
            # 샤프 비율 계산
            risk_free_rate = 0.02
            sharpe_ratio = (expected_return - risk_free_rate) / expected_volatility if expected_volatility > 0 else 0
            
            return {
                "allocations": allocated_assets,
                "risk_level": risk_level,
                "metrics": {
                    "expected_return": expected_return,
                    "expected_volatility": expected_volatility,
                    "sharpe_ratio": sharpe_ratio
                },
                "updated_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"포트폴리오 최적화 실패: {str(e)}")
            return {"error": str(e)} 