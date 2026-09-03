from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.config import get_settings
from infrastructure.alpaca.client import AlpacaClients
from infrastructure.alpaca.broker import AlpacaBroker
from infrastructure.alpaca.options import AlpacaOptionProvider
from infrastructure.alpaca.market import AlpacaMarketDataProvider
from infrastructure.ai.factory import create_ai_service
from infrastructure.persistence.database import create_session_factory
from infrastructure.persistence.repositories.journal import SQLJournalRepository
from application.ai.service import AIResearchService
from application.dashboard.service import DashboardService
from application.options.chain import OptionChainService
from application.market.regime import RegimeDetector
from application.options.strategy import DefinedRiskStrategy
from application.portfolio.context import PortfolioContextService
from application.quant.scorer import QuantScorer
from application.risk.risk_kernel import DeterministicRiskKernel
from application.trading.decision import DecisionService
from application.trading.engine import TradingEngine
from application.trading.execution import ExecutionService
from application.trading.journal import JournalService
from application.trading.pipeline import TradingPipeline
from application.trading.runner import TradingRunManager
from presentation.api.dashboard import router as dashboard_router
from presentation.api.health import router as health_router
from presentation.api.trading import router as trading_router

settings=get_settings()
logger=logging.getLogger("alpha_commander")

@asynccontextmanager
async def lifespan(app:FastAPI):
    settings.validate_runtime()
    clients=AlpacaClients(settings.alpaca_api_key,settings.alpaca_api_secret,paper=True)
    broker=AlpacaBroker(clients)
    _,session_factory=create_session_factory(settings.database_url)
    journal=JournalService(SQLJournalRepository(session_factory))
    portfolio=PortfolioContextService(broker)
    ai=create_ai_service(settings)
    engine=TradingEngine(AlpacaMarketDataProvider(settings.alpaca_api_key,settings.alpaca_api_secret),RegimeDetector(),ai,QuantScorer(),OptionChainService(AlpacaOptionProvider(settings.alpaca_api_key,settings.alpaca_api_secret)),DefinedRiskStrategy(),DeterministicRiskKernel())
    pipeline=TradingPipeline(engine,DecisionService(),ExecutionService(broker),journal)
    app.state.environment=settings.environment; app.state.logger=logger; app.state.portfolio_context_service=portfolio
    app.state.trading_manager=TradingRunManager(pipeline)
    app.state.dashboard_service=DashboardService(portfolio,journal)
    yield

app=FastAPI(title="ALPHA COMMANDER",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["GET","POST","OPTIONS"],allow_headers=["Accept","Authorization","Content-Type","Origin","User-Agent","X-Requested-With","X-Client-Order-ID"],expose_headers=["Content-Type","X-Request-ID"],max_age=86400)
app.include_router(health_router); app.include_router(trading_router); app.include_router(dashboard_router)
