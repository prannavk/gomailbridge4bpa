# from app.zidoc_api.hf_service import hf_service
# from app.utils.logger import log

# def generate_status_analysis(stats: dict) -> str:
#     """Generates the status summary + LLM inference HTML block"""
#     total = stats.get("total", 0)
#     status_counts = stats.get("status_counts", {})
#     mestyp_counts = stats.get("mestyp_counts", {})
#     idoctp_counts = stats.get("idoctp_counts", {})

#     # Basic analytics summary (static content)
#     summary = f"""
#     <h3>1. iDoc Status Overview</h3>
#     <p>Total iDocs: <b>{total}</b></p>
#     <ul>
#     {''.join(f'<li>Status {k}: {v}</li>' for k, v in status_counts.items())}
#     </ul>
#     <p><b>Message Types:</b> {', '.join(f'{k} ({v})' for k, v in mestyp_counts.items())}</p>
#     <p><b>iDoc Types:</b> {', '.join(f'{k} ({v})' for k, v in idoctp_counts.items())}</p>
#     """

#     # LLM prompt
#     prompt = (
#         f"The system processed {total} iDocs. The status breakdown is: "
#         f"{dict(status_counts)}. Message types seen were {dict(mestyp_counts)}. "
#         f"iDoc types seen were {dict(idoctp_counts)}.\n\n"
#         f"Based on this breakdown, analyze what the common iDoc posting issues might be. "
#         f"Give a brief summary in HTML format for inclusion in an email." 
#     )

#     # try:
#     #     insight = hf_service.generate_text(prompt)
#     # except Exception as e:
#     #     insight = f"<p><i>LLM inference failed: {str(e)}</i></p>"

#     # return summary + f"<div>{insight}</div>"
#     try:
#         insight = hf_service.generate_text(prompt)
#         return summary + f"<div>{insight}</div>"
#     except Exception as e:
#         log(f"LLM inference failed in generate_status_analysis: {str(e)}")
#         return summary  # Only static analytics if LLM fails


# def generate_traffic_spike_insight(stats: dict) -> str:
#     """Generates time-based spike report + LLM inference"""
#     daily_counts = stats.get("daily_counts", {})
#     if not daily_counts:
#         return "<h3>2. iDoc Traffic Spike Insight</h3><p>No daily data available.</p>"

#     sorted_dates = sorted(daily_counts.items())
#     summary = """
#     <h3>2. iDoc Traffic Spike Insight</h3>
#     <ul>
#     """
#     for date, count in sorted_dates:
#         summary += f"<li>{date}: {count} iDocs</li>"
#     summary += "</ul>"

#     max_date, max_count = max(daily_counts.items(), key=lambda x: x[1])
#     prompt = (
#         f"Here is the iDoc traffic by day: {dict(sorted_dates)}.\n"
#         f"The highest volume was on {max_date} with {max_count} iDocs.\n"
#         f"What could be the reason for such a spike? Provide a short HTML-formatted explanation suitable for inclusion in a report."
#     )

#     try:
#         insight = hf_service.generate_text(prompt)
#         return summary + f"<div>{insight}</div>"
#     except Exception as e:
#         log(f"LLM inference failed in generate_traffic_spike_insight: {str(e)}")
#         return summary


# def generate_segment_error_focus(stats: dict) -> str:
#     """Generates segment usage and potential issues insight"""
#     segments = stats.get("segments", {})
#     samples = stats.get("segment_samples", {})

#     if not segments:
#         return "<h3>3. Segment Error Focus</h3><p>No segment data found.</p>"

#     summary = """
#     <h3>3. Segment Error Focus</h3>
#     <ul>
#     """
#     for segnam, count in segments.items():
#         summary += f"<li>{segnam}: {count} occurrences"
#         if samples.get(segnam):
#             example = samples[segnam][0][:100].strip()
#             summary += f" (e.g., '{example}')"
#         summary += "</li>"
#     summary += "</ul>"

#     prompt = (
#         f"Here are the iDoc segment types and their usage counts: {dict(segments)}.\n"
#         f"Some sample raw SDATA strings: { {k: v[0] for k, v in samples.items() if v} }.\n"
#         f"Which segments are most prone to causing errors and why? "
#         f"Suggest which segments to inspect more closely. Answer in HTML format."
#     )

#     try:
#         insight = hf_service.generate_text(prompt)
#         return summary + f"<div>{insight}</div>"
#     except Exception as e:
#         log(f"LLM inference failed in generate_segment_error_focus: {str(e)}")
#         return summary


# def generate_partner_mismatch_alerts(stats: dict) -> str:
#     """Highlights partner pairing anomalies"""
#     partners = stats.get("partners", {})

#     if not partners:
#         return "<h3>4. Partner Mismatch Alerts</h3><p>No partner combinations available.</p>"

#     summary = """
#     <h3>4. Partner Mismatch Alerts</h3>
#     <ul>
#     """
#     for pair, count in sorted(partners.items(), key=lambda x: x[1], reverse=True):
#         summary += f"<li>{pair}: {count} iDocs</li>"
#     summary += "</ul>"

#     prompt = (
#         f"Here are the sender-receiver partner combinations and their counts: {dict(partners)}.\n"
#         f"Which combinations look unusual or problematic? Which ones may need investigation due to frequent errors or volume spikes?\n"
#         f"Provide a brief HTML-formatted diagnostic summary."
#     )

#     try:
#         insight = hf_service.generate_text(prompt)
#         return summary + f"<div>{insight}</div>"
#     except Exception as e:
#         log(f"LLM inference failed in generate_partner_mismatch_alerts: {str(e)}")
#         return summary


# def generate_delay_summary(stats: dict) -> str:
#     """Highlights time gaps between CREDAT-CRETIM and UPDDAT-UPDTIM"""
#     delays = stats.get("delays", [])
#     if not delays:
#         return "<h3>5. Delay Summary</h3><p>No delay data available.</p>"

#     significant_delays = [d for d in delays if d.get("delay_seconds", 0) > 120]
#     summary = """
#     <h3>5. Delay Summary</h3>
#     <p>Below are iDocs with delay > 2 minutes between creation and last update:</p>
#     <ul>
#     """
#     for delay in significant_delays:
#         docnum = delay.get("DOCNUM")
#         secs = delay.get("delay_seconds")
#         created = delay.get("created")
#         updated = delay.get("updated")
#         summary += f"<li>DOCNUM {docnum}: Delay = {secs:.1f}s (Created: {created}, Updated: {updated})</li>"
#     summary += "</ul>"

#     prompt = (
#         f"Here are iDocs that showed long delays between creation and update: {significant_delays[:5]}.\n"
#         f"Explain possible reasons for such delays in SAP message processing. Give the answer in HTML format."
#     )

#     try:
#         insight = hf_service.generate_text(prompt)
#         return summary + f"<div>{insight}</div>"
#     except Exception as e:
#         log(f"LLM inference failed in generate_delay_summary: {str(e)}")
#         return summary


# def generate_status_analysis(stats: dict) -> str:
#     """Generates the status summary + LLM inference HTML block"""
#     pass

# def generate_traffic_spike_insight(stats: dict) -> str:
#     """Generates time-based spike report + LLM inference"""
#     pass

# def generate_segment_error_focus(stats: dict) -> str:
#     """Generates segment usage and potential issues insight"""
#     pass

# def generate_partner_mismatch_alerts(stats: dict) -> str:
#     """Highlights partner pairing anomalies"""
#     pass

# def generate_delay_summary(stats: dict) -> str:
#     """Highlights time gaps between CREDAT-CRETIM and UPDDAT-UPDTIM"""
#     pass

# FILE: zidoc_api/utils/point_generators.py
from app.zidoc_api.hf_service import hf_service
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from app.utils.logger import log, debug_bool
# from app.zidoc_api.api.zidoc_proxy import debug_bool

def clean_prompt_text(prompt: str) -> str:
    """Applies consistent length + structure trimming to boost speed"""
    return (
        prompt.strip() +
        "\n\nNote: Respond briefly in 3 to 7 HTML bullet points using <p> and <ul>. Avoid repetition."
    )

def generate_status_analysis(stats: dict) -> str:
    total = stats.get("total", 0)
    status_counts = stats.get("status_counts", {})
    mestyp_counts = stats.get("mestyp_counts", {})
    idoctp_counts = stats.get("idoctp_counts", {})

    summary = f"""
    <h3>1. iDoc Status Overview</h3>
    <p>Total iDocs: <b>{total}</b></p>
    <ul>
        {''.join(f'<li>Status {k}: {v}</li>' for k, v in status_counts.items())}
    </ul>
    <p><b>Message Types:</b> {', '.join(f'{k} ({v})' for k, v in mestyp_counts.items())}</p>
    <p><b>iDoc Types:</b> {', '.join(f'{k} ({v})' for k, v in idoctp_counts.items())}</p>
    """

    query = clean_prompt_text(
        f"The system processed {total} iDocs. The status breakdown is: {dict(status_counts)}. "
        f"Message types seen were {dict(mestyp_counts)}. iDoc types were {dict(idoctp_counts)}."
        f" What might this indicate about system health or common iDoc errors?"
        f"SideNote: For \"53\" iDoc status don't say it indicates a potential issue as I believe it means iDoc successfully posted. If all iDocs have 53 status, then in that case praise the developer who has made this possible"
    )
    insight = hf_service.generate_inference_text(query)
    log(f"1. \n\n {insight} \n\n", debug_bool)
    return summary + f"<div>{insight}</div>"


def generate_traffic_spike_insight(stats: dict) -> str:
    times = stats.get("times", [])
    spike_hours = stats.get("spike_hours", {})

    summary = f"""
    <h3>2. Traffic Spike Analysis</h3>
    <p>Total timestamps analyzed: <b>{len(times)}</b></p>
    <p><b>Peak Hours:</b> {', '.join(f'{k}: {v} iDocs' for k, v in spike_hours.items())}</p>
    """

    query = clean_prompt_text(
        f"We analyzed {len(times)} iDocs by timestamp. The peak hours and their counts were: {dict(spike_hours)}."
        f" What could this tell us about load, batch processing, or potential risk hours?"
    )
    insight = hf_service.generate_inference_text(query)
    log(f"2. \n\n {insight} \n\n", debug_bool)
    return summary + f"<div>{insight}</div>"


def generate_segment_error_focus(stats: dict) -> str:
    segment_counts = stats.get("segment_counts", {})
    suspect_segments = [k for k in segment_counts if k.upper() in {"E1EDK14", "E1EDP01", "E1EDK01"}]

    summary = f"""
    <h3>3. Segment Frequency Snapshot</h3>
    <p>Most common segments:</p>
    <ul>
        {''.join(f'<li>{seg}: {cnt}</li>' for seg, cnt in segment_counts.items())}
    </ul>
    <p><b>Suspicious segments observed:</b> {', '.join(suspect_segments) or 'None'}</p>
    """

    query = clean_prompt_text(
        f"Segment usage counts were: {dict(segment_counts)}. Segments like {', '.join(suspect_segments)} are frequent."
        f" Could any of these segments be causing errors or be misused in posting logic?"
    )
    insight = hf_service.generate_inference_text(query)
    log(f"3. \n\n {insight} \n\n", debug_bool)
    return summary + f"<div>{insight}</div>"


def generate_partner_mismatch_alerts(stats: dict) -> str:
    partners = stats.get("partner_types", {})
    missing_roles = [k for k, v in partners.items() if v == 0]

    summary = f"""
    <h3>4. Partner Role Anomalies</h3>
    <p>Partner types detected:</p>
    <ul>
        {''.join(f'<li>{ptype}: {count}</li>' for ptype, count in partners.items())}
    </ul>
    <p><b>Missing partner roles:</b> {', '.join(missing_roles) or 'None'}</p>
    """

    query = clean_prompt_text(
        f"The following partner types and counts were extracted: {dict(partners)}. "
        f"Roles with 0 frequency were: {', '.join(missing_roles)}."
        f" Are any of these critical roles (like AG, WE) missing, and what does their absence indicate?"
    )
    insight = hf_service.generate_inference_text(query)
    log(f"4. \n\n {insight} \n\n", debug_bool)
    return summary + f"<div>{insight}</div>"


def generate_delay_summary(stats: dict) -> str:
    max_delay = stats.get("max_delay_secs", 0)
    min_delay = stats.get("min_delay_secs", 0)
    avg_delay = stats.get("avg_delay_secs", 0)
    outlier_count = stats.get("outlier_delay_count", 0)

    summary = f"""
    <h3>5. CREDAT/UPDDAT Delay Analysis</h3>
    <ul>
        <li><b>Average Delay:</b> {avg_delay:.2f} seconds</li>
        <li><b>Maximum Delay:</b> {max_delay:.2f} seconds</li>
        <li><b>Minimum Delay:</b> {min_delay:.2f} seconds</li>
        <li><b>Outliers (very large delay):</b> {outlier_count}</li>
    </ul>
    """

    query = clean_prompt_text(
        f"iDoc posting delays (UPDDAT-UPDTIM vs. CREDAT-CRETIM) show an average of {avg_delay:.2f}s, max: {max_delay:.2f}s, "
        f"min: {min_delay:.2f}s, outliers: {outlier_count}."
        f" What could cause long delays in SAP iDoc flows and how can they be reduced?"
    )
    insight = hf_service.generate_inference_text(query)
    log(f"5. \n\n {insight} \n\n", debug_bool)
    return summary + f"<div>{insight}</div>"

def generate_all_points_parallel(stats: dict) -> list[str]:
    """Parallel execution of all 5 report points"""
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(generate_status_analysis, stats),
            executor.submit(generate_traffic_spike_insight, stats),
            executor.submit(generate_segment_error_focus, stats),
            executor.submit(generate_partner_mismatch_alerts, stats),
            executor.submit(generate_delay_summary, stats),
        ]
    #     insights = [f.result() for f in futures]
    # return "".join(insights)
    return [f.result() for f in futures]