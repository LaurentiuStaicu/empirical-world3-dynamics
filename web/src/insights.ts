import type {AppData,IndicatorKey,ScenarioKey,ScenarioRow} from './data';
import {coreSystemIndicators,indicatorOrder} from './catalog';

export const SCENARIOS:ScenarioKey[]=['original_bau','original_bau2','hybrid_2026'];
export const ALIGNMENT_INDICATORS:IndicatorKey[]=['population','industry_per_capita','food_per_capita','pollution_pressure','human_welfare'];
export const OUTLOOK_INDICATORS:IndicatorKey[]=['industry_total','industry_per_capita','food_per_capita','human_welfare','population','persistent_pollution_stock','resources_remaining_pct'];
export const HEADLINE_TURNING_POINT_INDICATORS:IndicatorKey[]=['industry_total','industry_per_capita','food_per_capita','human_welfare','population'];
export const SCENARIO_LABELS:Record<ScenarioKey,{en:string;ro:string}>={original_bau:{en:'Original BAU',ro:'BAU original'},original_bau2:{en:'Original BAU2',ro:'BAU2 original'},hybrid_2026:{en:'BAU Hybrid 2026',ro:'BAU Hibrid 2026'}};

export const INSIGHT_DEFINITIONS={
  version:'2.0.1',preregistered_before_product_calculation:true,
  peak:{rule:'first_global_maximum',ties:'earliest_year'},
  sustained_decline:{lookahead_years:10,non_increasing_steps_min:8,minimum_net_decline_fraction:0.05,search_starts_at_peak:true},
  severe_decline:{threshold_fraction_of_peak:0.80,persistence_years:5,persistence_fraction_of_peak:0.85,persistence_hits_min:4,label:'severe deterioration; not automatically collapse'},
  stabilization:{window_years:10,max_range_fraction_of_peak:0.05,max_net_change_fraction_of_peak:0.02},
  recovery:{threshold_fraction_of_peak:0.90,persistence_years:5,requires_prior_severe_decline:true},
  systemic_decline:{indicators:coreSystemIndicators,primary_quorum:3,primary_window_years:15,sensitivity_quorums:[2,3,4],sensitivity_windows_years:[10,15,20]},
  collapse_window:{indicators:coreSystemIndicators,severe_decline_required:true,primary_quorum:3,primary_window_years:20,sensitivity_quorums:[2,3,4],sensitivity_windows_years:[15,20,25]},
  headline_turning_points:{indicators:HEADLINE_TURNING_POINT_INDICATORS,excludes:['resources_remaining_pct','persistent_pollution_stock'],reason:'depletion/pollution stocks are still shown in cards but do not define the headline first production/welfare/demographic turning point'},
  timing_uncertainty:{p10_p90_event_timing_allowed:false,reason:'The published P10–P90 curves are pointwise quantiles, not coherent member trajectories. They cannot identify a distribution of peak or decline years.'},
  scenario_timing_range:{meaning:'range of event years across BAU, BAU2 and Hybrid where the event is identified; scenario sensitivity, not probability'},
  scenario_alignment:{metric:'sMAPE',aggregation:'equal_weight_mean_across_preregistered_indicators',overlap:'observed_years_only',interpretation:'descriptive_empirical_alignment_not_probability_or_forecast_skill'},
} as const;

export interface TrajectoryInsight{peakYear:number|null;peakValue:number|null;declineOnsetYear:number|null;severeDeclineYear:number|null;changeFromPeakPct:number|null;recoveryOrStabilization:{kind:'recovery'|'stabilization';year:number}|null;}
const value=(row:ScenarioRow,scenario:ScenarioKey):number|null=>row[scenario];
const usable=(rows:ScenarioRow[],scenario:ScenarioKey)=>rows.filter(r=>value(r,scenario)!==null).map(r=>({year:r.year,value:value(r,scenario)!}));

export function trajectoryInsight(rows:ScenarioRow[],scenario:ScenarioKey):TrajectoryInsight{
  const s=usable(rows,scenario);if(!s.length)return{peakYear:null,peakValue:null,declineOnsetYear:null,severeDeclineYear:null,changeFromPeakPct:null,recoveryOrStabilization:null};
  let peakIndex=0;for(let i=1;i<s.length;i++)if(s[i]!.value>s[peakIndex]!.value)peakIndex=i;const peak=s[peakIndex]!;
  let declineOnsetYear:number|null=null;for(let i=peakIndex;i+10<s.length;i++){let nonIncreasing=0;for(let j=i;j<i+10;j++)if(s[j+1]!.value<=s[j]!.value)nonIncreasing++;const net=(s[i]!.value-s[i+10]!.value)/Math.max(Math.abs(s[i]!.value),1e-12);if(nonIncreasing>=8&&net>=.05){declineOnsetYear=s[i]!.year;break;}}
  let severeDeclineYear:number|null=null;for(let i=peakIndex;i<s.length;i++){if(s[i]!.value>peak.value*.80)continue;const window=s.slice(i,i+5);if(window.length<5)break;if(window.filter(p=>p.value<=peak.value*.85).length>=4){severeDeclineYear=s[i]!.year;break;}}
  let event:TrajectoryInsight['recoveryOrStabilization']=null;
  if(severeDeclineYear!==null){const start=s.findIndex(p=>p.year>=severeDeclineYear);for(let i=start;i+4<s.length;i++)if(s.slice(i,i+5).every(p=>p.value>=peak.value*.90)){event={kind:'recovery',year:s[i]!.year};break;}}
  if(!event&&declineOnsetYear!==null){const start=s.findIndex(p=>p.year>=declineOnsetYear);for(let i=start;i+10<s.length;i++){const window=s.slice(i,i+11),vals=window.map(p=>p.value),range=(Math.max(...vals)-Math.min(...vals))/Math.max(Math.abs(peak.value),1e-12),net=Math.abs(window[window.length-1]!.value-window[0]!.value)/Math.max(Math.abs(peak.value),1e-12);if(range<=.05&&net<=.02){event={kind:'stabilization',year:window[0]!.year};break;}}}
  return{peakYear:peak.year,peakValue:peak.value,declineOnsetYear,severeDeclineYear,changeFromPeakPct:((s[s.length-1]!.value/peak.value)-1)*100,recoveryOrStabilization:event};
}

const smape=(observed:number,model:number):number=>observed===0&&model===0?0:(200*Math.abs(model-observed))/(Math.abs(model)+Math.abs(observed));
export interface AlignmentCell{indicator:IndicatorKey;scenario:ScenarioKey;smape:number|null;n:number;firstYear:number|null;lastYear:number|null;}
export interface AlignmentSummary{cells:AlignmentCell[];aggregate:Record<ScenarioKey,number|null>;best:ScenarioKey|null;}
export function scenarioAlignment(data:AppData):AlignmentSummary{
  const cells:AlignmentCell[]=[];for(const indicator of indicatorOrder)for(const scenario of SCENARIOS){const pairs=data.scenarios[indicator].filter(r=>r.observed!==null&&value(r,scenario)!==null);cells.push({indicator,scenario,smape:pairs.length?pairs.reduce((a,r)=>a+smape(r.observed!,value(r,scenario)!),0)/pairs.length:null,n:pairs.length,firstYear:pairs[0]?.year??null,lastYear:pairs[pairs.length-1]?.year??null});}
  const aggregate=Object.fromEntries(SCENARIOS.map(s=>{const vals=cells.filter(c=>c.scenario===s&&ALIGNMENT_INDICATORS.includes(c.indicator)&&c.smape!==null).map(c=>c.smape!);return[s,vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:null];})) as Record<ScenarioKey,number|null>;
  const ranked=SCENARIOS.filter(s=>aggregate[s]!==null).sort((a,b)=>aggregate[a]!-aggregate[b]!);return{cells,aggregate,best:ranked[0]??null};
}

function clusteredWindow(years:number[],quorum:number,span:number):[number,number]|null{const sorted=[...years].sort((a,b)=>a-b);for(let i=0;i<sorted.length;i++){const j=i+quorum-1;if(j>=sorted.length)break;if(sorted[j]!-sorted[i]!<=span)return[sorted[i]!,sorted[j]!];}return null;}
export interface SystemWindow{primary:[number,number]|null;sensitivity:[number,number]|null;qualifyingDefinitions:number;totalDefinitions:number;}
export function systemicWindow(data:AppData,scenario:ScenarioKey,kind:'decline'|'collapse'):SystemWindow{
  const eventYears=coreSystemIndicators.map(k=>{const m=trajectoryInsight(data.scenarios[k],scenario);return kind==='decline'?m.declineOnsetYear:m.severeDeclineYear;}).filter((y):y is number=>y!==null);
  const primary=clusteredWindow(eventYears,3,kind==='decline'?15:20),qs=[2,3,4],spans=kind==='decline'?[10,15,20]:[15,20,25],ranges:Array<[number,number]>=[];let total=0;
  for(const q of qs)for(const span of spans){total++;const r=clusteredWindow(eventYears,q,span);if(r)ranges.push(r);}return{primary,sensitivity:ranges.length?[Math.min(...ranges.map(r=>r[0])),Math.max(...ranges.map(r=>r[1]))]:null,qualifyingDefinitions:ranges.length,totalDefinitions:total};
}

export interface TimingRange{range:[number,number]|null;years:Partial<Record<ScenarioKey,number>>;available:number;total:number;classification:'robust'|'moderate'|'sensitive'|'scenario-dependent'|'not-estimated';}
export function scenarioTimingRange(data:AppData,indicator:IndicatorKey,event:'peak'|'decline'|'severe'):TimingRange{
  const years:Partial<Record<ScenarioKey,number>>={};for(const scenario of SCENARIOS){const insight=trajectoryInsight(data.scenarios[indicator],scenario),year=event==='peak'?insight.peakYear:event==='decline'?insight.declineOnsetYear:insight.severeDeclineYear;if(year!==null)years[scenario]=year;}
  const values=Object.values(years);if(!values.length)return{range:null,years,available:0,total:SCENARIOS.length,classification:'not-estimated'};const range:[number,number]=[Math.min(...values),Math.max(...values)];if(values.length<SCENARIOS.length)return{range,years,available:values.length,total:SCENARIOS.length,classification:'scenario-dependent'};const span=range[1]-range[0];return{range,years,available:values.length,total:SCENARIOS.length,classification:span<=10?'robust':span<=20?'moderate':'sensitive'};
}

export interface OutlookRow{indicator:IndicatorKey;insight:TrajectoryInsight;peakRange:TimingRange;declineRange:TimingRange;severeRange:TimingRange;}
export interface ScenarioOutlook{scenario:ScenarioKey;rows:OutlookRow[];firstPeak:OutlookRow|null;firstDecline:OutlookRow|null;systemicDecline:SystemWindow;collapse:SystemWindow;}
export function buildScenarioOutlook(data:AppData,scenario:ScenarioKey):ScenarioOutlook{
  const rows=OUTLOOK_INDICATORS.map(indicator=>({indicator,insight:trajectoryInsight(data.scenarios[indicator],scenario),peakRange:scenarioTimingRange(data,indicator,'peak'),declineRange:scenarioTimingRange(data,indicator,'decline'),severeRange:scenarioTimingRange(data,indicator,'severe')}));
  const headline=rows.filter(r=>HEADLINE_TURNING_POINT_INDICATORS.includes(r.indicator));
  const firstPeak=[...headline].filter(r=>r.insight.peakYear!==null).sort((a,b)=>a.insight.peakYear!-b.insight.peakYear!)[0]??null;
  const firstDecline=[...headline].filter(r=>r.insight.declineOnsetYear!==null).sort((a,b)=>a.insight.declineOnsetYear!-b.insight.declineOnsetYear!)[0]??null;
  return{scenario,rows,firstPeak,firstDecline,systemicDecline:systemicWindow(data,scenario,'decline'),collapse:systemicWindow(data,scenario,'collapse')};
}
export interface ModelSummary{alignment:AlignmentSummary;}
export const buildModelSummary=(data:AppData):ModelSummary=>({alignment:scenarioAlignment(data)});
