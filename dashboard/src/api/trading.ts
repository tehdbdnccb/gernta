import {api} from './client'; import type {JournalEntry,PortfolioResponse} from '../types/trading';
export const tradingApi={portfolio:async()=> (await api.get<PortfolioResponse>('/portfolio')).data,journal:async(limit=50)=> (await api.get<JournalEntry[]>('/journal',{params:{limit}})).data,analysis:async(id:string)=> (await api.get(`/trades/runs/${encodeURIComponent(id)}`)).data};
