"""The Odds API integration service."""
import httpx
from typing import List, Dict, Any
from datetime import datetime

from app.core.config import settings


class OddsAPIService:
    """Service for interacting with The Odds API."""

    def __init__(self):
        self.base_url = settings.ODDS_API_BASE_URL
        self.api_key = settings.ODDS_API_KEY

    async def get_sports(self) -> List[Dict[str, Any]]:
        """
        Get available sports from The Odds API.

        Returns:
            List of sports
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports",
                params={"apiKey": self.api_key}
            )
            response.raise_for_status()
            return response.json()

    async def get_odds(
        self,
        sport_key: str,
        regions: str = "us",
        markets: str = "h2h,spreads,totals",
        odds_format: str = "decimal"
    ) -> List[Dict[str, Any]]:
        """
        Get odds for a specific sport.

        Args:
            sport_key: Sport identifier
            regions: Regions for odds (us, uk, eu, au)
            markets: Betting markets (h2h, spreads, totals)
            odds_format: Format for odds (decimal, american)

        Returns:
            List of events with odds
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports/{sport_key}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": regions,
                    "markets": markets,
                    "oddsFormat": odds_format
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_event_odds(
        self,
        sport_key: str,
        event_id: str,
        regions: str = "us",
        markets: str = "h2h,spreads,totals"
    ) -> Dict[str, Any]:
        """
        Get odds for a specific event.

        Args:
            sport_key: Sport identifier
            event_id: Event identifier
            regions: Regions for odds
            markets: Betting markets

        Returns:
            Event with odds
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports/{sport_key}/events/{event_id}/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": regions,
                    "markets": markets,
                    "oddsFormat": "decimal"
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_scores(self, sport_key: str, days_from: int = 3) -> List[Dict[str, Any]]:
        """
        Get scores for completed and live events.

        Args:
            sport_key: Sport identifier
            days_from: Number of days from today to get scores

        Returns:
            List of events with scores
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sports/{sport_key}/scores",
                params={
                    "apiKey": self.api_key,
                    "daysFrom": days_from
                }
            )
            response.raise_for_status()
            return response.json()


# Singleton instance
odds_api_service = OddsAPIService()
