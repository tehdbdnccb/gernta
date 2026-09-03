export interface AccountSnapshot{portfolio_value:number;buying_power:number;daily_pnl:number;open_risk:number;underlying_exposure:number;position_count:number}
export interface Position{symbol:string;qty:number;market_value:number;unrealized_pnl:number;avg_entry_price:number}
export interface PortfolioResponse{account:AccountSnapshot;positions:Position[]}
export interface JournalEntry{id:string;run_id:string;created_at:string;symbol:string;regime:string;thesis:string;score:number;risk_approved:boolean;executed:boolean;veto_reason:string|null;order_id:string|null;analysis:Record<string,unknown>}
